import numpy as np

#将空值转换为0，方便加减运算
#若所有为0，跳过打分输出nan
def nan_to_0(x):
    where_are_nan = np.isnan(x)
    x[where_are_nan] = 0

    return x




