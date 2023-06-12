import seaborn as sns
import json
import matplotlib.pyplot as plt
import pandas as pd

sns.set_theme()
if __name__ == '__main__':
    df = pd.DataFrame({
        'Temperature': [0.2, 0.5, 0.8, 1.1], 
        'GRR': [0.475, 0.665, 0.675, 0.615], 
        'BTR': [0.005, 0.05, 0.06, 0.065]
    })
    ax = sns.lineplot(df, x='Temperature', y='GRR', label='GRR', marker='o', markersize=10)
    ax = sns.lineplot(df, x='Temperature', y='BTR', label='BTR', marker='o', markersize=10)
  
    ax.set(xlabel='Temperature', ylabel='Rate')
    plt.xlim(0, 1.2)
    plt.ylim(-0.05, 1.0)
    plt.show()
    
# if __name__ == '__main__':
    
#     df = pd.DataFrame({'no_plans': [1,8,16,25], 'generator+verifier': [0.255, 0.53, 0.61, 0.655], 'generator':[0.255, 0.37, 0.375, 0.375]})
#     ax = sns.lineplot(df, x='no_plans', y='generator+verifier', label='generator+verifier', marker='o', markersize=10)
#     ax = sns.lineplot(df, x='no_plans', y='generator', label='generator', marker='o', markersize=10)
#     ax.set(xlabel='Number of attempts', ylabel='Goal reaching rate')
#     # plt.xlim(0, 1.2)
#     # plt.ylim(0, 1.0)
#     plt.show()
