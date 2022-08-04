import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.figure
from matplotlib import ticker
from networkx import Graph
import networkx as nx
import scipy




def create_coperation_networkx(filepath):
    '''
    从csv文件中将数据装换为协作网络图
    :param filepath:文件路径
    :return: 所得的图
    '''
    #读取mashup文件
    data = pd.read_csv(filepath)
    #将mashup中的相关API部分进行切割爆炸然后获取不相同的API列表，那么这个列表就是我们的节点
    # 对相关的api进行切割
    data['newcol'] = data['related_apis'].str.split("###")
    #newcol进行保存也就是节点之间存在的边
    coperation = data['newcol']
    #对coperation进行数据处理将空值删除掉
    coperation = coperation.fillna('None')
    # 对切割的newcol进行爆炸处理
    data = data.explode('newcol')
    #制作节点,将newcol单独提取出来进行数据清洗删去所有重复的行
    newcol = data['newcol']
    newcol.duplicated()
    nodes = newcol.drop_duplicates()
    #把nodes的空值去掉
    nodes = nodes.fillna('None')
    #转为list
    nodes = list(nodes)
    #建立没有边的图
    G = Graph()
    G.add_nodes_from(nodes)
    #对于还没有爆炸处理的newcol,那么比如['A','B','C']就称他们之间有连接的边,对图添加边，其中判断如果有边则权值加1，无边就之间加
    #其中难点就是对于['A','B','C']中要判断三组边 该如何去表示
    for i in range(coperation.size):
        #对coperation每个元素制作边,其中这里面coperation数据存在NAN，此时要进行处理
        Totaledge = itertools.combinations(coperation[i], r=2)          #这里用组合函数
        Totaledge = list(Totaledge)
        for j in range(len(Totaledge)):
            #如果图中存在该边,该边其权值
            edge = Totaledge[j]
            if G.has_edge(edge[0], edge[1]):
                edgedata = G.get_edge_data(edge[0],edge[1])
                G.add_edge(edge[0], edge[1], weight = (edgedata["weight"]+1))
            #如果图中不存在该边,添加边然后设置权值为1
            else:
                G.add_edge(edge[0], edge[1], weight = 1)
    return G

if __name__ == "__main__":
    coperationGraph = create_coperation_networkx("datasets/Mashups.csv")
    #获取图的边的权值
    weights = nx.get_edge_attributes(coperationGraph,"weight")
    #对weights按值排序
    weights_order = sorted(weights.items(), key=lambda x: x[1], reverse=True)
    top10ofweight = weights_order[0:10]
    collabels = ['No.', 'API 1', 'API 2', 'Number of coperation times']
    text = []
    for i in range(len(top10ofweight)):
        text.append([i+1, top10ofweight[i][0][0], top10ofweight[i][0][1], top10ofweight[i][1]])
    table = plt.table(cellText=text, colLabels=collabels, loc='center', cellLoc='center', rowLoc='center')
    table.scale(1, 2)
    plt.axis("off")
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    plt.title("Table 9 The top 10 web API pairs in mashup creation")
    plt.show()
