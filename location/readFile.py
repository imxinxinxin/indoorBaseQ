import os
import re
from locationMethod import*
from tool import*
from toCSV import *


def readOneMonth(trnAmountInOneMonth, tstAmountInOneMonth,nowPath,datasetName,month,floor):


    for i in range(1,trnAmountInOneMonth+1):
        trnRssFile = 'trn' + n2s(i) + 'rss.csv'
        trnRssPath = os.path.join(nowPath, 'dataset', datasetName, n2s(month), trnRssFile)
        trnCrdFile = 'trn' + n2s(i) + 'crd.csv'
        trnCrdPath = os.path.join(nowPath, 'dataset', datasetName, n2s(month), trnCrdFile)
        if i==1 :
            trnRss = getFloorData(np.loadtxt(trnRssPath, delimiter=","),floor)

            trnCrd = getFloorData(np.loadtxt(trnCrdPath, delimiter=",",usecols=(0,1)),floor)
        else:
            # 读取训练集
            trnRss = np.concatenate((trnRss, getFloorData(np.loadtxt(trnRssPath, delimiter=","),floor)))
            # 读取训练集坐标
            trnCrd = np.concatenate((trnCrd, getFloorData(np.loadtxt(trnCrdPath, delimiter=",",usecols=(0,1)),floor)))

    for j in range(1,tstAmountInOneMonth+1):
        tstRssFile = 'tst' + n2s(j) + 'rss.csv'
        tstRssPath = os.path.join(nowPath, 'dataset', datasetName, n2s(month), tstRssFile)
        tstCrdFile = 'tst' + n2s(j) + 'crd.csv'
        tstCrdPath = os.path.join(nowPath, 'dataset', datasetName, n2s(month), tstCrdFile)
        if j==1:
            tstRss=getFloorData(np.loadtxt(tstRssPath, delimiter=","),floor)
            tstCrd=getFloorData(np.loadtxt(tstCrdPath, delimiter=",",usecols=(0,1)),floor)
        else:
            # 读取测试集
            tstRss = np.concatenate((tstRss,getFloorData(np.loadtxt(tstRssPath, delimiter=","),floor)))
            # 读取测试集坐标
            tstCrd = np.concatenate((tstCrd, getFloorData(np.loadtxt(tstCrdPath, delimiter=",",usecols=(0,1)),floor)))


    return trnCrd,trnRss,tstCrd,tstRss



def readAllMonth(trnAmountInOneMonth, tstAmountInOneMonth, nowPath,datasetName, monthNumber,floor):
    if len(monthNumber)==0:
        print("请勿输入空的月份序列")
    elif len(monthNumber)==1:
        trnCrd,trnRss,tstCrd,tstRss=readOneMonth(trnAmountInOneMonth, tstAmountInOneMonth, nowPath, datasetName, monthNumber[0],floor)
    else:
        trnCrd, trnRss, tstCrd, tstRss = readOneMonth(trnAmountInOneMonth, tstAmountInOneMonth, nowPath, datasetName,monthNumber[0],floor)
        for month in monthNumber[1:]:
            trnCrd2, trnRss2, tstCrd2, tstRss2=readOneMonth(trnAmountInOneMonth, tstAmountInOneMonth, nowPath, datasetName,monthNumber[0],floor)
            trnCrd=np.concatenate((trnCrd,trnCrd2))
            trnRss = np.concatenate((trnRss, trnRss2))
            tstCrd = np.concatenate((tstCrd, tstCrd2))
            tstRss = np.concatenate((tstRss, tstRss2))


    return trnCrd, trnRss, tstCrd, tstRss