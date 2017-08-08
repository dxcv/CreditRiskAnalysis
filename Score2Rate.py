import numpy as np
import pandas as pd

# df_score: the final score of the bond
# output: the final rate of the bond
def Score2Rate(df_score):
    rate = np.empty(df_score.shape).astype('str')
    for i in range(0, df_score.size):
        if df_score.iloc[i] > 4.2:
            rate[i] = "A"
        elif df_score.iloc[i] > 4:
            rate[i] = "B1"
        elif df_score.iloc[i] > 3.7:
            rate[i] = "B2"
        elif df_score.iloc[i] > 3.5:
            rate[i] = "B3"
        elif df_score.iloc[i] > 3.2:
            rate[i] = "C1"
        elif df_score.iloc[i] > 2.9:
            rate[i] = "C2"
        elif df_score.iloc[i] > 2.6:
            rate[i] = "C3"
        elif df_score.iloc[i] > 2.3:
            rate[i] = "D1"
        elif df_score.iloc[i] > 2:
            rate[i] = "D2"
        elif df_score.iloc[i] > 1.7:
            rate[i] = "D3"
        elif df_score.iloc[i] > 1.4:
            rate[i] = "E1"
        elif df_score.iloc[i] > 1.1:
            rate[i] = "E2"
        elif df_score.iloc[i] > 0.8:
            rate[i] = "E3"
        else:
            rate[i] = "F"

    return rate