import pandas as pd 
import argparse 
from tqdm import tqdm
import argparse
import logging
from transformers import set_seed, GPT2Config, GPT2Tokenizer, GPT2ForSequenceClassification


import numpy as np
import pandas as pd
import torch

from transformers import (
    CTRLLMHeadModel,
    CTRLTokenizer,
    GPT2LMHeadModel,
    GPT2Tokenizer,
    OpenAIGPTLMHeadModel,
    OpenAIGPTTokenizer,
    TransfoXLLMHeadModel,
    TransfoXLTokenizer,
    XLMTokenizer,
    XLMWithLMHeadModel,
    XLNetLMHeadModel,
    XLNetTokenizer,
)


logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

MAX_LENGTH = int(10000)  # Hardcoded max length to avoid infinite loop

MODEL_CLASSES = {
    "gpt2": (GPT2LMHeadModel, GPT2Tokenizer),
    "ctrl": (CTRLLMHeadModel, CTRLTokenizer),
    "openai-gpt": (OpenAIGPTLMHeadModel, OpenAIGPTTokenizer),
    "xlnet": (XLNetLMHeadModel, XLNetTokenizer),
    "transfo-xl": (TransfoXLLMHeadModel, TransfoXLTokenizer),
    "xlm": (XLMWithLMHeadModel, XLMTokenizer),
}

# Padding text to help Transformer-XL and XLNet with short prompts as proposed by Aman Rusia
# in https://github.com/rusiaaman/XLNet-gen#methodology
# and https://medium.com/@amanrusia/xlnet-speaks-comparison-to-gpt-2-ea1a4e9ba39e
PREFIX = """In 1991, the remains of Russian Tsar Nicholas II and his family
(except for Alexei and Maria) are discovered.
The voice of Nicholas's young son, Tsarevich Alexei Nikolaevich, narrates the
remainder of the story. 1883 Western Siberia,
a young Grigori Rasputin is asked by his father and a group of men to perform magic.
Rasputin has a vision and denounces one of the men as a horse thief. Although his
father initially slaps him for making such an accusation, Rasputin watches as the
man is chased outside and beaten. Twenty years later, Rasputin sees a vision of
the Virgin Mary, prompting him to become a priest. Rasputin quickly becomes famous,
with people, even a bishop, begging for his blessing. <eod> </s> <eos>"""


def set_seed(args):
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    if args.n_gpu > 0:
        torch.cuda.manual_seed_all(args.seed)


#
# Functions to prepare models' input
#


def prepare_ctrl_input(args, _, tokenizer, prompt_text):
    if args.temperature > 0.7:
        logger.info("CTRL typically works better with lower temperatures (and lower top_k).")

    encoded_prompt = tokenizer.encode(prompt_text, add_special_tokens=False)
    if not any(encoded_prompt[0] == x for x in tokenizer.control_codes.values()):
        logger.info("WARNING! You are not starting your generation from a control code so you won't get good results")
    return prompt_text


def prepare_xlm_input(args, model, tokenizer, prompt_text):
    # kwargs = {"language": None, "mask_token_id": None}

    # Set the language
    use_lang_emb = hasattr(model.config, "use_lang_emb") and model.config.use_lang_emb
    if hasattr(model.config, "lang2id") and use_lang_emb:
        available_languages = model.config.lang2id.keys()
        if args.xlm_language in available_languages:
            language = args.xlm_language
        else:
            language = None
            while language not in available_languages:
                language = input("Using XLM. Select language in " + str(list(available_languages)) + " >>> ")

        model.config.lang_id = model.config.lang2id[language]
        # kwargs["language"] = tokenizer.lang2id[language]

    # TODO fix mask_token_id setup when configurations will be synchronized between models and tokenizers
    # XLM masked-language modeling (MLM) models need masked token
    # is_xlm_mlm = "mlm" in args.model_name_or_path
    # if is_xlm_mlm:
    #     kwargs["mask_token_id"] = tokenizer.mask_token_id

    return prompt_text


def prepare_xlnet_input(args, _, tokenizer, prompt_text):
    prefix = args.prefix if args.prefix else args.padding_text if args.padding_text else PREFIX
    prompt_text = prefix + prompt_text
    return prompt_text


def prepare_transfoxl_input(args, _, tokenizer, prompt_text):
    prefix = args.prefix if args.prefix else args.padding_text if args.padding_text else PREFIX
    prompt_text = prefix + prompt_text
    return prompt_text


PREPROCESSING_FUNCTIONS = {
    "ctrl": prepare_ctrl_input,
    "xlm": prepare_xlm_input,
    "xlnet": prepare_xlnet_input,
    "transfo-xl": prepare_transfoxl_input,
}


def adjust_length_to_model(length, max_sequence_length):
    if length < 0 and max_sequence_length > 0:
        length = max_sequence_length
    elif 0 < max_sequence_length < length:
        length = max_sequence_length  # No generation bigger than model size
    elif length < 0:
        length = MAX_LENGTH  # avoid infinite loop
    return length

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--domain')
    parser.add_argument('--action_model_path', default='gpt2')
    parser.add_argument('--plans_file')
    parser.add_argument('--num_trajectories_to_consider', type=int)
    parser.add_argument('--batch_size', type=int)
    args = parser.parse_args()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    action_model_path = args.action_model_path
    action_model_config = GPT2Config.from_pretrained(action_model_path, num_labels=2) # Binary Classification
    action_model = GPT2ForSequenceClassification.from_pretrained(action_model_path, config=action_model_config)

    tokenizer = GPT2Tokenizer.from_pretrained(action_model_path)
    tokenizer.padding_side = "right"
    tokenizer.pad_token = tokenizer.eos_token

    action_model.resize_token_embeddings(len(tokenizer))
    action_model.config.pad_token_id = action_model.config.eos_token_id
    action_model.to(device)

    for i in tqdm(range(0, 200), desc='instances'):
        df = pd.read_csv(f'../results/{args.domain}/{i}.csv')
        plans = df['trajectories']
        action_model_preds = []
        goal_model_preds = []
        for j in tqdm(range(args.num_trajectories_to_consider), desc='plans'):
            plan = eval(plans[j])
            error_in_plan = False
            action_model_inputs = []
            # breakpoint()
            for transition in plan[1:]:
                action_model_inputs.append(f'STATE:\n{transition.split("STATE:")[1].split("NEXT ")[0].strip()}')
            
            
            all_logits = []
            inputs = tokenizer(action_model_inputs, return_tensors="pt", padding=True)
            for k in range(0, inputs['input_ids'].shape[0], args.batch_size):    
                logits = action_model(
                    inputs['input_ids'][k:min(k+args.batch_size, inputs['input_ids'].shape[0])].to(action_model.device),
                )['logits']
                all_logits.extend(logits.argmax(dim=-1).tolist())
            verdict_reached = False
            action_model_preds.append(all_logits)
            
        pd.DataFrame({
            'action_model_preds': action_model_preds,
        }).to_csv(f'../results/{args.domain}/{i}_pred.csv', index=False)

if __name__ == '__main__':
    
    main()
