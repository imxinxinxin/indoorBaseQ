import seaborn as sns
import numpy as np
from readFile import *
from pandas import Series, DataFrame
sns.set()

datasetName='park'#不同大小的数据集名称
monthNumber=[1,2,3]#使用哪几个月的数据进行计算
#monthNumber=[1]
trnAmountInOneMonth=4#单月训练数据rss文件数
tstAmountInOneMonth=8#单月测试数据rss文件数

floor=3
nowPath = os.path.abspath(os.path.join(os.getcwd(), ".."))

metricMean=np.zeros((16, len(monthNumber)))

for month in monthNumber:

    allTrnCrd, allTrnRss, allTstCrd, allTstRss = readOneMonth(trnAmountInOneMonth, tstAmountInOneMonth, nowPath,
                                                               datasetName, month,floor)
    #allTrnRss, allTrnCrd = preRmse(allTrnRss, allTrnCrd)
    #allTstRss, allTstCrd = preRmse(allTstRss, allTstCrd)



    # AP_r = getAP_r(allTrnRss)
    # AP_list, ap_mat_list = r2list(AP_r, 80)
    # allTrnRss = allTrnRss[:, ap_mat_list]


    allTrnRssS=allTrnRss.flatten().astype(int)
    L = filter(lambda x: x!=100, allTrnRssS)
    L = [i for i in L]
    plt.title('park'+str(month))  # 添加标题
    sns.distplot(L, fit=norm, kde=False)

    plt.show()

    print(np.count_nonzero((-100 < allTrnRssS) & (allTrnRssS < -80)))

    print("完成")
