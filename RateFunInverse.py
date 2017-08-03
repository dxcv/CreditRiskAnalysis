def RateFunInverse(Data, ScoringCriterion):
    Score = Data
    Score[Data<=ScoringCriterion[0]] = 5.5
    Score[(Data<=ScoringCriterion[1]) & (Data>ScoringCriterion[0])] = 5
    Score[(Data<=ScoringCriterion[2]) & (Data>ScoringCriterion[1])] = 4.5
    Score[(Data<=ScoringCriterion[3]) & (Data>ScoringCriterion[2])] = 4
    Score[(Data<=ScoringCriterion[4]) & (Data>ScoringCriterion[3])] = 3.5
    Score[(Data<=ScoringCriterion[5]) & (Data>ScoringCriterion[4])] = 3
    Score[(Data<=ScoringCriterion[6]) & (Data>ScoringCriterion[5])] = 2.5
    Score[(Data<=ScoringCriterion[7]) & (Data>ScoringCriterion[6])] = 2
    Score[(Data<=ScoringCriterion[8]) & (Data>ScoringCriterion[7])] = 1.5
    Score[(Data<=ScoringCriterion[9]) & (Data>ScoringCriterion[8])] = 1
    Score[(Data<=ScoringCriterion[10]) & (Data>ScoringCriterion[9])] = 0.5
    Score[(Data<=ScoringCriterion[11]) & (Data>ScoringCriterion[10])] = 0
    Score[(Data<=ScoringCriterion[12]) & (Data>ScoringCriterion[11])] = -0.5
    Score[(Data>ScoringCriterion[12])] = -1.5


    return Score
