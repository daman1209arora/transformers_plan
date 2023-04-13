import pandas as pd


def is_valid(plan):
    pass
    
def main():
    
    num_total_traj = 0
    num_accepted_traj = 0
    num_accepted_and_valid_traj = 0
    
    for i in range(500):
        trajs = pd.read_csv(f'../results/{i}.csv')['trajectories']
        preds = pd.read_csv(f'../results/{i}_pred.csv')['prediction']
        
        accepted_traj = None
        for j in range(min(len(trajs), len(preds))):
            pred = eval(preds[j])
            traj = eval(trajs[j])
            bad_step = False
            for k in range(40):
                if pred[k] == 0:
                    bad_step = True
                    break
                if "GOAL REACHED" in traj[k+1]:
                    accepted_traj = traj[:k+1]
                    break 
            if accepted_traj:
                break            
        # breakpoint()
        if accepted_traj is not None:
            if is_valid(accepted_traj):
                num_accepted_and_valid_traj += 1
            num_accepted_traj += 1
            
        num_total_traj += 1
    
if __name__ == '__main__':
    main()