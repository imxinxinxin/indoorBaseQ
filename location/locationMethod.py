import math
import numpy as np
from scipy.stats import norm
from tool import*

def kNNEstimation(trnRss, tstRss, trnCrd, k,distanceType,loss):
    """实现KNN方法

    Args:
        samples (ndarray): 训练集样本
        query (ndarray): 测试集样本
        positions (ndarray): 训练集样本的位置
        k (Number): 最近邻个数

    Returns:
        prediction (ndarray): 预测位置坐标
    """
    samplRows = trnRss.shape[0]#训练集RP数目
    queryRows = tstRss.shape[0]#测试集RP数目
    prediction = np.zeros([queryRows, 2])#空矩阵存储预测坐标
    if loss!=0:
        base=math.pow(10,1/(10*loss))#底数Q

    if k > samplRows:
        k = samplRows

    for i in range(queryRows):#遍历每一个测试点进行预测
        repQuery = np.tile(tstRss[i, :], (samplRows, 1))#第i个测试点的rss数据行，复制训练RP数个，以方便统一同训练集矩阵进行计算

        if distanceType==0:#曼哈顿
            Distance=np.sum(np.abs(trnRss - repQuery), axis=1)

        elif distanceType==1:#底数曼哈顿
            baseNp = np.full((np.shape(trnRss)), base)
            baseTra = np.power(baseNp, trnRss)
            baseTst = np.power(baseNp, repQuery)
            Distance = np.sum(np.abs(baseTra - baseTst), axis=1)

        else:
            print("参数无效，请检查距离计算方法")

        idx = np.argsort(Distance)[0:k]  # 前k小值的索引
        val = Distance[idx]  # 取出前k小的值

        pos = trnCrd[idx, :]
        if val[0] == 0:  # 若存在某训练集样本与测试集样本的欧氏距离为0，则预测位置为该训练集样本的位置
            prediction[i, :] = pos[0, :]
        else:
            prediction[i, :] = np.mean(pos, axis=0)#坐标均值即为预测坐标

    return prediction




def wkNNEstimation(trnRss, tstRss, trnCrd, k,distanceType,loss):
    """实现WKNN方法

    Args:
        samples (ndarray): 训练集样本
        query (ndarray): 测试集样本
        positions (ndarray): 训练集样本的位置
        k (Number): 最近邻个数

    Returns:
        prediction (ndarray): 预测位置坐标
    """
    samplRows = trnRss.shape[0]#训练集RP数目
    queryRows = tstRss.shape[0]#测试集RP数目
    prediction = np.zeros([queryRows, 2])#空矩阵存储预测坐标
    rpVote = {}#rp分数用来进行邻近选择

    if loss!=0:
        base=math.pow(10,1/(10*loss))#底数Q

    # if k > samplRows:
    #     k = samplRows

    for i in range(queryRows):#遍历每一个测试点进行预测
        repQuery = np.tile(tstRss[i, :], (samplRows, 1))#第i个测试点的rss数据行，复制训练RP数个，以方便统一同训练集矩阵进行计算

        if distanceType==0:#曼哈顿
            Distance=np.sum(np.abs(trnRss - repQuery), axis=1)

        elif distanceType==1:#底数曼哈顿
            baseNp = np.full((np.shape(trnRss)), base)
            baseTra = np.power(baseNp, trnRss)
            baseTst = np.power(baseNp, repQuery)
            Distance = np.sum(np.abs(baseTra - baseTst), axis=1)

        else:
            print("参数无效，请检查距离计算方法")

        # rpVote是从小到大分数排序后的rp序号及对应分数，rp_point只是默认按顺序每个rp的分数。
        for rpi, dis in enumerate(Distance):
            rpVote["rp" + str(rpi)] = dis
        rpVote = OrderedDict(sorted(rpVote.items(), key=lambda d: d[1]))
        # 获取到k个高权重rp，rp序号序列
        k,idx=get_k(rpVote, Distance)

        if k<4:
            k=3
            idx = np.argsort(Distance)[0:k]


        # 形成权重weight = w + coor
        w = 1 / (Distance + 1e-8)
        w = np.reshape(w, (np.shape(w)[0], 1))
        weight = np.hstack((w, trnCrd))[idx, :]
        weight[:, 0] = weight[:, 0] / np.sum(weight[:, 0], 0)

        val=Distance[idx]
        pos = trnCrd[idx, :]
        if val[0] == 0:  # 若存在某训练集样本与测试集样本的欧氏距离为0，则预测位置为该训练集样本的位置
            prediction[i, :] = pos[0, :]
        else:
            prediction[i, :] = [np.sum(weight[:, 0]*weight[:, 1]),np.sum(weight[:, 0]*weight[:, 2])]#坐标均值即为预测坐标

    return prediction