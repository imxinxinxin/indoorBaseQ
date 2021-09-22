import numpy as np
import seaborn as sns
from readFile import *

datasetName='longterm620'#不同大小的数据集名称
#monthNumber=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]#使用哪几个月的数据进行计算
monthNumber=[1]
trnAmountInOneMonth=15#单月训练数据rss文件数
tstAmountInOneMonth=5#单月测试数据rss文件数

floor=3
nowPath = os.path.abspath(os.path.join(os.getcwd(), ".."))

metricMean=np.zeros((16, len(monthNumber)))

for month in monthNumber:

    allTrnCrd, allTrnRss, allTstCrd, allTstRss = readOneMonth(trnAmountInOneMonth, tstAmountInOneMonth, nowPath,
                                                               datasetName, month,floor)

    print(allTrnRss.shape[0]*allTrnRss.shape[1])
    print(allTstRss.shape[0]*allTstRss.shape[1])
    metricMean[0,monthNumber.index(month)]=np.mean(allTrnRss)
    metricMean[1,monthNumber.index(month)]=np.mean(allTstRss)

    metricMean[2,monthNumber.index(month)]=np.std(allTrnRss, ddof=1)
    metricMean[3,monthNumber.index(month)]=np.std(allTstRss, ddof=1)

    metricMean[4, monthNumber.index(month)] =np.sum(allTrnRss==100)
    metricMean[5, monthNumber.index(month)] = np.sum(allTstRss==100)

    metricMean[6, monthNumber.index(month)] =np.sum(allTrnRss<-80)
    metricMean[7, monthNumber.index(month)] = np.sum(allTstRss<-80)

    metricMean[8, monthNumber.index(month)] =np.sum(allTrnRss<-70)
    metricMean[9, monthNumber.index(month)] = np.sum(allTstRss<-70)

    metricMean[10, monthNumber.index(month)] =np.sum(allTrnRss<-60)
    metricMean[11, monthNumber.index(month)] = np.sum(allTstRss<-60)

    metricMean[12, monthNumber.index(month)] =np.sum(allTrnRss<-50)
    metricMean[13, monthNumber.index(month)] = np.sum(allTstRss<-50)

    metricMean[14, monthNumber.index(month)] =np.sum(allTrnRss<-40)
    metricMean[15, monthNumber.index(month)] = np.sum(allTstRss<-40)

errorPath = os.path.join(nowPath, 'dataset', datasetName, 'sum100.csv')
# saveNdarryToCsv(metricMean, errorPath)  # 保存误差