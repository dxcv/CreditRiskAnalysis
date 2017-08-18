
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

# 16中油01
# myfun.PastData("136164.SH")
#  11晨鸣债
# myfun.PastData("112031.SZ")
# 11太阳MTN1
# myfun.PastData("1182035.IB")
# 山鹰纸业
# myfun.PastData("600567.SH")
# 岳阳临纸
# myfun.PastData("600963.SH")
# 中闽能源
# myfun.PastData("600163.SH")
# 恒丰纸业
# myfun.PastData("600356.SH")
# 11金光MTN1
# myfun.PastData("1182098.IB")
# 11玖龙MTN1
# myfun.PastData("1182380.IB")
# 11白云CP02
# myfun.PastData("1181393.IB")
# 企业债：17临武舜发债
# myfun.PastData("q17081502.SH")
# 公司债：08中粮债
# myfun.PastData("112004.SZ")
# 短期融资券：16鞍钢SCP006
# myfun.PastData("011641006.IB")
# 中期票据：17招商蛇口MTN001
# myfun.PastData("031780001.IB")


ScoringCriterionTable = pd.read_excel("Table1.xlsx")
OtherScore = pd.read_excel("OtherScore.xlsx")

myfun.score(ScoringCriterionTable, OtherScore)

WeightTable = pd.read_excel("Table2.xlsx")
print(myfun.rate(WeightTable))








