import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt



#读取数据
data = pd.read_csv("datasets/Mashups.csv")
#对目录进行切割
data['newcol'] = data['categories'].str.split("###")
#对切割的函数进行爆炸处理
data = data.explode('newcol')
#对API的目录进行统计
API_categories_sort = data['newcol'].value_counts(ascending=False)
#取其中排名前十的API目录
APIoftop10 = API_categories_sort.head(10)

#绘制表格
labels = ('No.', 'Mashup category', 'Number of Mashups')
text = []
for i in range(10):
    text.append([str(i+1), APIoftop10.index[i], APIoftop10[i]])
table = plt.table(cellText=text, colLabels=labels, loc='center', cellLoc='center',rowLoc='center')
table.scale(1,2)
plt.axis("off")
table.auto_set_font_size(False)
table.set_fontsize(10)
plt.title("The top 10 popular mashup categories")
plt.show()


