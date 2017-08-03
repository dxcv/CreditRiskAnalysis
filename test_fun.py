from BondRating import *
from WindPy import w
import pandas as pd
from datetime import *
w.start()
myfun = BondRating()
df = pd.read_excel("Table1.xlsx")
myfun.PastData("136164.SH")
print(myfun.score(df))

# print(a)
#
# print(df[15:16][2.5])
#
# print(a > np.array(df[15:16][2.5])*100)
# print(a < np.array(df[15:16][3]*100))
# a1 = a > np.array(df[15:16][2.5])*100
# a2 = a < np.array(df[15:16][3]*100)
# b = a
# b[(a > np.array(df[15:16][2.5])*100) & (a < np.array(df[15:16][3]*100))] = 2.5
# print(b)

