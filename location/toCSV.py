import numpy as np
import pandas as pd
import os


def saveNdarryToCsv(n_array,path):
    '''

    Args:
        n_array (ndarray): 要存储的n维numpy数组
        path (string): 存储路径（包含文件名）

    Returns:

    '''
    dfCrd = pd.DataFrame(n_array)
    dfCrd.to_csv(path, sep=',', header=0, index=0)
    print("文件已存储，路径为："+path)
    return