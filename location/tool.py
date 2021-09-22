import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import os
import re
import math
import csv
from scipy import stats
from scipy.stats import norm
from collections import OrderedDict

def n2s(num):
    '''
    将数字转为字符串，0-9转为01/02/03的形式
    Args:
        num (int):数字

    Returns:
        (string)
    '''
    if num<10:
        return '0' + str(num)
    else:
        return str(num)

def getFloorData(data,floor):
    if floor==3:
        filterData=data[0:int(data.shape[0]/2),:]
    elif floor ==5:
        filterData = data[int(data.shape[0] / 2):, :]
    elif floor==1:
        filterData=data
    return filterData

def customError(estimationPos, actualPos):
    """
    计算预测位置与实际位置之间的误差
    Args:
        estimationPos (ndarray): 预测位置
        actualPos (ndarray): 实际位置

    Returns:
        e (ndarray): 返回误差，不保持二维特性，是一个一维数组，长度=tstRP数。
    """
    e = np.sqrt(np.sum(np.square(estimationPos - actualPos), axis=1))#a[i,0]+a[i,1]+...
    return e


#rmse均值方差剔除粗大误差
def preRmse(rss,crd):
    rss[rss==100]=-105

    row=int(rss.shape[0])



#1.剔除粗大误差，这里的均值只是用来辅助计算。
    meanRss =[0] * row
    for i in range(0,row,10):
        mean=np.mean(rss[i:i + 10, :], 0)
        if i==0:
            meanRss=mean
        else:
            meanRss=np.vstack((meanRss, mean))
    # v 残差矩阵
    v = [0] * row
    for i in range(row):
        _v = (rss[i] - meanRss[i // 10]) ** 2
        if i == 0:
            v = _v
        else:
            v = np.vstack((v, _v))

 # sigma 均方根误差矩阵
    sigma = [0] * row

    for i in range(0, row, 10):
        _sigma = np.sqrt(0.2 * np.sum(v[i:i + 10, :], 0))
        if i == 0:
            sigma = _sigma
        else:
            sigma = np.vstack((sigma, _sigma))
 # 误差大于三倍均方误差可视为异常值
    three_sigma = 3 * sigma

    v = np.sqrt(v)
    # 同残差作比较
    fv = [0] * row
    for i in range(row):
        _v = v[i] - three_sigma[i // 10]
        if i == 0:
            fv = _v
        else:
            fv = np.vstack((fv, _v))
    # v < 3 * simga 保留 存为1
    fv[fv >= 0] = 0
    fv[fv < 0] = 1
    # 得到一个01矩阵对RSS进行过滤
    f_rss = fv * rss
    where_are_nan = np.isnan(f_rss)
    f_rss[where_are_nan] = -105

#2.粗大误差剔除之后，真正的均值处理
    final_rss = [0] * row
    count = [0] * row
    for i in range(0, row, 10):
        _f_rss = np.sum(f_rss[i:i + 10, :], 0)
        #fcount=(f_rss>-105)
        _count = np.sum(fv[i:i + 10, :], 0)
        if i == 0:
            final_rss = _f_rss
            count = _count
        else:
            final_rss = np.vstack((final_rss, _f_rss))
            count = np.vstack((count, _count))
    final_rss = final_rss / count



#新的均值处理方法
    # final_rss = [0] * row
    # count = [0] * row
    # for i in range(0, row, 6):
    #
    #     _f_rss = f_rss[i:i + 6, :].sum(0)/(f_rss[i:i + 6, :] != -105).sum(0)
    #     if i == 0:
    #         final_rss = _f_rss
    #     else:
    #         final_rss = np.vstack((final_rss, _f_rss))


    #final_rss[final_rss<-105]=-105
    #final_rss[final_rss > -1] = -105
    # 找到值为0的数据用-105替代
    where_are_nan = np.isnan(final_rss)
    final_rss[where_are_nan] = -105

    final_crd=crd[0::10,:]

    #where_are_nan = np.isnan(f_rss)
    #f_rss[where_are_nan] = -105

    return final_rss,final_crd


def getAP_r(allTrnRss):
    trn_rp = allTrnRss.shape[0]  # 训练集RP数目288
    trn_ap=allTrnRss.shape[1]#AP620
    allTrnRssCopy=allTrnRss.copy()

    allTrnRssCopy[allTrnRssCopy==100]=-105
    mean=allTrnRssCopy.copy()
    sum=np.max(mean,0)

    p_rss=allTrnRssCopy.copy()
    p_rss[p_rss != -105] = 1
    p_rss[p_rss == -105] = 0

    p_sum = np.sum(p_rss, 0)
    ap_rss = (sum + 105) / 105

    p_sum = p_sum / trn_rp
    p_sum[p_sum <= 0.05] = 0

    p = p_sum
    p[p == 1] = 101
    p = 1 / (1 - p)
    p[p == 1] = 0
    p[p == -0.01] = 100
    ap_p = p

    AP_r = {}
    for i in range(trn_ap):
        AP_r["AP" + str(i)] = ap_rss[i] * ap_p[i]
    # sort 升序排序
    AP_r = OrderedDict(sorted(AP_r.items(), key=lambda d: d[1], reverse=True))

    return AP_r

def r2list(AP_r,APCount):
    tag = 0
    ap_list = []
    ap_mat_list = []
    for key in AP_r.keys():
        tag = tag + 1
        if tag >APCount:
            break
        else:
            ap_list.append(key)
            ap_mat_list.append(int(key[2:]))
    return ap_list, ap_mat_list

#根据某种规则，获取最终参与定位的邻近AP序号。
#输入：从小到大分数排序后的rp序号及对应分数、默认按顺序每个rp的分数。
#输出:所选AP数目和序号列表。
def get_k(dis, rp_mat):
    """
    :param dis:
    :param rp_mat:
    :return:
    """
    # 小于1的则全选 大于1排除

    # ①字典
    temp = {}
    k_list = []
    mini_dis = 0
    tag = 0
    for k, v in dis.items():
        tag = tag + 1
        if tag == 1:
            mini_dis = v
            temp[k] = v
        else:
            if v <= 2 * mini_dis:
                temp[k] = v

    sum = 0
    out_k = 1
    extra = {}
    tag1 = 0
    mini = 0
    for k, v in temp.items():
        tag1 = tag1 + 1
        if tag1 == 1:
            mini = temp[k]
            k_list.append(int(k[2:]))
            continue
        extra[k] = temp[k] - mini
        sum = sum + extra[k]
    if tag1 == 1:
        return out_k, k_list
    else:
        avg = sum / (tag1 - 1)

    for k in extra.keys():
        if extra[k] <= 0.666*avg:
            out_k = out_k + 1
            k_list.append(int(k[2:]))
    # out_k = 3 if out_k > 3 else out_k
    return out_k, k_list