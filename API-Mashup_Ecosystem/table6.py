import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame


data = pd.read_csv("datasets/Mashups.csv")

#对相关的api进行切割
data['newcol'] = data['related_apis'].str.split("###")
#对切割的newcol进行爆炸处理
data = data.explode('newcol')

api_sta = data['newcol'].value_counts(ascending=False)
top10ofAPIinMashup = api_sta.head(10)


#绘制表格
labels = ('No.', 'API name', 'Number of mashups')
text = []
for i in range(10):
    text.append([str(i+1), top10ofAPIinMashup.index[i], top10ofAPIinMashup[i]])
table = plt.table(cellText=text, colLabels=labels, loc='center', cellLoc='center',rowLoc='center')
table.scale(1,2)
plt.title("Table 6 The top 10 popular APIs in mashup creation")
table.auto_set_font_size(False)
table.set_fontsize(8)
plt.axis('off')
plt.show()
