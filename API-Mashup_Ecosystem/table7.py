import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt

APIs = pd.read_csv("datasets/APIs.csv")

#对目录进行切割
APIs['newcol'] = APIs['DevelopersName'].str.split("###")
#对切割的函数进行爆炸处理
APIs = APIs.explode('newcol')

numofdeveloper = APIs['newcol']

numofdeveloper = APIs['newcol'].value_counts()

top10 = numofdeveloper.head(10)
top10 = dict(top10)

labels = ['No', 'Provider', 'Number of APIs']
text = []
for i in range(10):
    text.append([i+1, list(top10.keys())[i], list(top10.values())[i]])

table = plt.table(cellText=text, colLabels=labels, loc='center', cellLoc='center', rowLoc='center')
table.scale(1, 2)
plt.axis("off")
table.auto_set_font_size(False)
table.set_fontsize(10)
plt.title("Table 7 Top 10 API developers with the largest number of APIs ")
plt.show()

