import pandas as pd
import matplotlib.pyplot as plt

Mashups = pd.read_csv("datasets/Mashups.csv")

#对Mashup相关API进行切割
Mashups['newcol'] = Mashups['related_apis'].str.split("###")
#对切割的函数进行爆炸处理
Mashups = Mashups.explode('newcol')


numofApi = Mashups['newcol']
numofApi = numofApi.value_counts(ascending=False)

#得到的结果
numofApi = numofApi.value_counts()

#这里的键值对就是我们x y的值
numofApi = dict(numofApi)

#对字典按键排序
numofApi = sorted(numofApi.items(),key=lambda x:x[0])

numofApi = dict(numofApi)

# #出去字典中值重复的键值对
# func = lambda z:dict([(x, y) for y, x in z.items()])
# result = func(func(numofApi))


result = sorted(numofApi.items(), key=lambda  x:x[0])
result = dict(result)


x = list(result.keys())
y = list(result.values())


#画图部分
ax = plt.gca()
# 此处为刻度不均匀，切记!!!用symlog而非log
ax.set_xlim(0, 10000)
ax.set_xscale('symlog')
ax.set_xticks([0, 10, 100, 1000, 10000])
ax.set_ylim(1, 10000)
ax.set_yscale('symlog')
ax.set_yticks([1, 10, 100, 1000, 10000])
ax.set_xlabel("Frequency of Uses")
ax.set_ylabel("Number of WAPIs")
ax.scatter(x, y, 20)
ax.plot(x, y, color=(0, 0, 0))
ax.annotate("(1,880)", xy=(1, 880), xytext=(1, 3000), arrowprops=dict(arrowstyle= '->'))
ax.annotate("(2075,1)", xy=(2075, 1), xytext=(2100, 5), arrowprops=dict(arrowstyle= '->'))
ax.set_title("Fig. 1. The accumulative distribution of the utilization rate of Web APIs")
plt.show()
