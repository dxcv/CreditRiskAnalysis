import numpy as np
import pandas as pd

def RateFunSpecial(DF, ScoringCriterion):
    Score = np.empty(DF.shape)

    #find if the score criterion is increased
    if ScoringCriterion.iloc[0] > ScoringCriterion.iloc[1]:
        for i in range(0, DF.size):
            if DF.iloc[i] < 0:
                Score[i] = -1.5
            elif DF.iloc[i] >= ScoringCriterion.iloc[0]:
                Score[i] = 5.5
            elif DF.iloc[i] >= ScoringCriterion.iloc[1]:
                Score[i] = 5
            elif DF.iloc[i] >= ScoringCriterion.iloc[2]:
                Score[i] = 4.5
            elif DF.iloc[i] >= ScoringCriterion.iloc[3]:
                Score[i] = 4
            elif DF.iloc[i] >= ScoringCriterion.iloc[4]:
                Score[i] = 3.5
            elif DF.iloc[i] >= ScoringCriterion.iloc[5]:
                Score[i] = 3
            elif DF.iloc[i] >= ScoringCriterion.iloc[6]:
                Score[i] = 2.5
            elif DF.iloc[i] >= ScoringCriterion.iloc[7]:
                Score[i] = 2
            elif DF.iloc[i] >= ScoringCriterion.iloc[8]:
                Score[i] = 1.5
            elif DF.iloc[i] >= ScoringCriterion.iloc[9]:
                Score[i] = 1
            elif DF.iloc[i] >= ScoringCriterion.iloc[10]:
                Score[i] = 0.5
            elif DF.iloc[i] >= ScoringCriterion.iloc[11]:
                Score[i] = 0
            elif DF.iloc[i] >= ScoringCriterion.iloc[12]:
                Score[i] = -0.5
            else:
                Score[i] = -1.5
    else:
        for i in range(0, DF.size):
            if DF.iloc[i] < 0:
                Score[i] = -1.5
            elif DF.iloc[i] <= ScoringCriterion.iloc[0]:
                Score[i] = 5.5
            elif DF.iloc[i] <= ScoringCriterion.iloc[1]:
                Score[i] = 5
            elif DF.iloc[i] <= ScoringCriterion.iloc[2]:
                Score[i] = 4.5
            elif DF.iloc[i] <= ScoringCriterion.iloc[3]:
                Score[i] = 4
            elif DF.iloc[i] <= ScoringCriterion.iloc[4]:
                Score[i] = 3.5
            elif DF.iloc[i] <= ScoringCriterion.iloc[5]:
                Score[i] = 3
            elif DF.iloc[i] <= ScoringCriterion.iloc[6]:
                Score[i] = 2.5
            elif DF.iloc[i] <= ScoringCriterion.iloc[7]:
                Score[i] = 2
            elif DF.iloc[i] <= ScoringCriterion.iloc[8]:
                Score[i] = 1.5
            elif DF.iloc[i] <= ScoringCriterion.iloc[9]:
                Score[i] = 1
            elif DF.iloc[i] <= ScoringCriterion.iloc[10]:
                Score[i] = 0.5
            elif DF.iloc[i] <= ScoringCriterion.iloc[11]:
                Score[i] = 0
            elif DF.iloc[i] <= ScoringCriterion.iloc[12]:
                Score[i] = -0.5
            else:
                Score[i] = -1.5

    return Score