import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame

APIs = pd.read_csv("datasets/APIs.csv")
Mashups = pd.read_csv("datasets/Mashups.csv")
sdk = pd.read_csv("datasets/SDKs.csv")
copy = Mashups.copy()


NumofAPI = APIs['APIName'].nunique()
Numofmashups = Mashups['mashups_name'].nunique()

#对APIs目录进行切割
APIs['newcol'] = APIs['Categories'].str.split("###")
#对切割的函数进行爆炸处理
APIs = APIs.explode('newcol')

#对Mashup目录进行切割
Mashups['newcol'] = Mashups['categories'].str.split("###")
#对切割的函数进行爆炸处理
Mashups = Mashups.explode('newcol')

copy['newcol'] = copy['related_apis'].str.split("###")
copy = copy.explode('newcol')

TotalAPIbyMashup = copy['newcol'].nunique()
#计算每一个mashup所使用的平均api数量
AverageofApipermashup = '%.2f' % (len(copy['newcol'])/Numofmashups)



TotalAPIproviders = sdk['SDK Provider'].nunique()



#统计APIs不同的category
NumofAPIcate = APIs['newcol'].nunique()

#统计Mashup不同的category
Numofmashupscate = Mashups['newcol'].nunique()




#绘制表格
label = ['Property', 'Value']

text = [['Number of mashups', Numofmashups],
        ['Number of web APIs', NumofAPI],
        ['Number of Web API providers', TotalAPIproviders],
        ['Number of Web APIs used by all Mashups', TotalAPIbyMashup],
        ['Average number of Web APIs used per Mashup',AverageofApipermashup]]

table = plt.table(cellText=text, colLabels=label, loc='center', cellLoc='center',rowLoc='center')
table.scale(1,2)
plt.axis("off")
table.auto_set_font_size(False)
table.set_fontsize(10)
plt.title("Table Ⅲ.  STATISTICAL PROPERTIES OF THE DATASET")
plt.show()