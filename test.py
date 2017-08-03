from WindPy import w
from datetime import *
from nan_to_0 import *

w.start()

import numpy as np
import pandas as pd





a = pd.read_excel("Table1.xlsx")
print(a[0:1][5.5])
print(a[5.5][1])
print(np.array(a[15:16])[0])
print(np.array(a)[15])


