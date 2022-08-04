import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt

#读取数据
data = pd.read_csv("datasets/Mashups.csv")
#对目录进行切割
data['newcol'] = data['related_apis'].str.split("###")
#对切割的函数进行爆炸处理
data = data.explode('newcol')

num_Mashup_per_api = data['newcol']
num_Mashup_per_api = num_Mashup_per_api.value_counts(ascending=False)

num_Mashup_per_api = num_Mashup_per_api.value_counts()
#这里的键值对就是我们x y的值
num_Mashup_per_api = dict(num_Mashup_per_api)

#对字典按键排序
num_Mashup_per_api = sorted(num_Mashup_per_api.items(), key=lambda x:x[0])

num_Mashup_per_api = dict(num_Mashup_per_api)

result = sorted(num_Mashup_per_api.items(), key=lambda  x:x[0])
result = dict(result)


x = list(result.keys())
y = list(result.values())

#画图部分
ax = plt.gca()
# 此处为刻度不均匀，切记!!!用symlog而非log
ax.set_xscale('symlog')
ax.set_xticks([1, 10, 100, 1000])
ax.set_yscale('symlog')
ax.set_yticks([1, 10, 100, 1000])
ax.set_xlabel("Number of Mashups per API")
ax.set_ylabel("Number of APIs")
ax.scatter(x, y, 20)
ax.plot(x, y, color=(0, 0, 0))
ax.set_title("Figure2  The cumulative distribution of number of mashups per API")
ax.annotate("(1,880)", xy=(1, 880), xytext=(1, 3000), arrowprops=dict(arrowstyle= '->'))
ax.annotate("(2075,1)", xy=(2075, 1), xytext=(2100, 5), arrowprops=dict(arrowstyle= '->'))
plt.show()



