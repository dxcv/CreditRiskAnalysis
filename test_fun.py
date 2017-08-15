
from BondRatingNew import *
from WindPy import w
import pandas as pd
w.start()

# BondRatingNew: the function to get the rate, including
# .PastData: raw data--> df_temp, get the data of each factor
# .score: df_temp--> df_score, get the score of each factor
# .rate: df_score--> df_rate, get the final rate of the bond

# RateFunNew: used in BondRatingNew.score, data-->score
# Table1.xlsx: the score criterion used in RateFunNew
# OtherScore.xlsx: other score

#Score2Rate: rate criterion, used in BondRatingNew.rate, score-->rate
#WeightTable.xlsx: used in BondRatingNew.rate, score-->rate


myfun = BondRatingNew()

myfun.PastData("136164.SH")
# myfun.PastData("112031.SZ")
# myfun.PastData("1182035.IB")
# myfun.PastData("600567.SH")
# myfun.PastData("600963.SH")
# myfun.PastData("600163.SH")
# myfun.PastData("600356.SH")

# myfun.PastData("1182098.IB")
# myfun.PastData("1182380.IB")
# myfun.PastData("136134.SH")
# myfun.PastData("1182035.IB")

ScoringCriterionTable = pd.read_excel("Table1.xlsx")
OtherScore = pd.read_excel("OtherScore.xlsx")

myfun.score(ScoringCriterionTable, OtherScore)

WeightTable = pd.read_excel("Table2.xlsx")
print(myfun.rate(WeightTable))








