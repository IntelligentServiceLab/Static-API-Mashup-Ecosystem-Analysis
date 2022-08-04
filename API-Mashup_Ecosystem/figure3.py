import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt

#主要别分制作柱状图的x,y轴
#x = [1,2,3,4,5,>=6]
x = ['1','2','3','4','5','≥6']
y = []

#读取数据对api部分进行分割

data = pd.read_csv("datasets/Mashups.csv")
data['newcol'] = data['related_apis'].str.split("###")
data = data.explode('newcol')
#统计mashup列  其中获得到的result 他的标签为mashup 值为api数
result = data['mashups_name'].value_counts(ascending=False)

#统计result中值分别=1 =2 =3 ...的mashup数
result_1 = (result==1)
y.append(result_1.sum())
result_2 = (result==2)
y.append(result_2.sum())
result_3 = (result==3)
y.append(result_3.sum())
result_4 = (result==4)
y.append(result_4.sum())
result_5 = (result==5)
y.append(result_5.sum())
result_6 = (result>=6)
y.append(result_6.sum())

plt.bar(x, y)

for a, b, i in zip(x, y, range(len(x))):  # zip 函数
    plt.text(a, b + 10, "%d" % y[i], ha='center', fontsize=10)  # plt.text 函数
plt.title("Figure 3 Distribution of the number of APIs used by each mashup")
plt.xlabel("Number of APIs used")
plt.ylabel("Number of Mashup")
plt.show()