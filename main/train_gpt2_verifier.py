from transformers import set_seed, GPT2Config, GPT2Tokenizer, GPT2ForSequenceClassification
import os
import pandas as pd
from torch.utils.data import Dataset
import matplotlib.pyplot as plt
import seaborn as sns
import torch
from tqdm import tqdm
from torch.utils.data import DataLoader, random_split
from transformers import AdamW, get_cosine_schedule_with_warmup, TrainingArguments, Trainer
from sklearn.metrics import classification_report, f1_score, accuracy_score, precision_score, recall_score
import argparse
import evaluate
import pdb
import numpy as np

set_seed(42) 

class TrajectoryDataset(Dataset):
    def __init__(self, train=True, train_file=None, val_file=None):
        super().__init__()
        self.train = train
        self.data = pd.read_csv(train_file if train else val_file)
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, index):
        record = self.data.iloc[index]
        text = record['transition']
        if self.train:
            return {'text': text, 'label': record['label']}
        else:
            return {'text': text, 'label': record['label']}
    

class Gpt2ClassificationCollator(object):
    def __init__(self, tokenizer, max_seq_len=1000):
        self.tokenizer = tokenizer
        self.max_seq_len = max_seq_len
        
    def __call__(self, sequences):
        texts = [sequence['text'] for sequence in sequences]
        labels = [int(sequence['label']) for sequence in sequences]
        inputs = self.tokenizer(text=texts,
                                return_tensors='pt',
                                padding=True,
                                truncation=True,
                                max_length=self.max_seq_len)
        inputs.update({'labels': torch.tensor(labels)})
        
        return inputs

def compute_metrics(eval_preds):
    logits, labels = eval_preds
    predictions = np.argmax(logits, axis=-1)
    print(predictions)
    print(labels)
    # pdb.set_trace()
    return {'accuracy': accuracy_score(labels, predictions), 'f1': f1_score(labels, predictions), 
            'precision': precision_score(labels, predictions), 'recall': recall_score(labels, predictions) }

def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--pretrained_model_path', default='gpt2')
    parser.add_argument('--train_file')
    parser.add_argument('--val_file')
    parser.add_argument('--per_device_train_batch_size', type=int, default=8)
    parser.add_argument('--num_train_epochs', type=int)
    parser.add_argument('--learning_rate', type=float, default=1e-5)
    parser.add_argument('--output_dir')

    args = parser.parse_args()

    pretrained_model_path = args.pretrained_model_path
    model_config = GPT2Config.from_pretrained(pretrained_model_path, num_labels=2) # Binary Classification
    model = GPT2ForSequenceClassification.from_pretrained(pretrained_model_path, config=model_config)

    tokenizer = GPT2Tokenizer.from_pretrained(pretrained_model_path)
    tokenizer.padding_side = "right"
    tokenizer.pad_token = tokenizer.eos_token

    model.resize_token_embeddings(len(tokenizer))
    model.config.pad_token_id = model.config.eos_token_id


    train_dataset = TrajectoryDataset(train=True, train_file=args.train_file)
    eval_dataset = TrajectoryDataset(train=False, val_file=args.val_file)
    
    gpt2classificationcollator = Gpt2ClassificationCollator(tokenizer=tokenizer)

    training_args = TrainingArguments(
        output_dir=args.output_dir,
        overwrite_output_dir=False,
        do_train=True,
        do_eval=True,
        evaluation_strategy="steps",
        per_device_train_batch_size=args.per_device_train_batch_size,
        per_device_eval_batch_size=32,
        gradient_accumulation_steps=1,
        learning_rate=args.learning_rate,
        num_train_epochs=args.num_train_epochs,
        warmup_steps=20,
        logging_dir=os.path.join(args.output_dir, 'tb_logs'),
        logging_steps=20,
        eval_steps=500,
        save_steps=500,
        save_total_limit=2,
        metric_for_best_model='f1',
        greater_is_better=True
    )
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        data_collator=gpt2classificationcollator,
        tokenizer=tokenizer,
        compute_metrics=compute_metrics
         
    )
    trainer.train()


if __name__ == '__main__':
    main()
