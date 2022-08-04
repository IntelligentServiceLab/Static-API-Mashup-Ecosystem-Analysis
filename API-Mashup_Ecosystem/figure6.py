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
    apicoperationNetwork = create_coperation_networkx("datasets/Mashups.csv")
    #去掉孤立节点
    apicoperationNetwork.remove_nodes_from(list(nx.isolates(apicoperationNetwork)))
    d = dict(nx.degree(apicoperationNetwork))
    x = list(range(max(d.values())+1))
    y = nx.degree_histogram(apicoperationNetwork)
    dic_xy = dict(zip(x,y))
    func = lambda z:dict([(x, y) for y, x in z.items()])
    result = func(func(dic_xy))
    resultcopy = result.copy()
    # z2 = np.polyfit(list(result.keys()),list(result.values()),1)
    # result.pop(452)
    # result.pop(453)
    for item in result.items():
        if item[0]>=100:
            resultcopy.pop(item[0])
    x = list(resultcopy.keys())
    y = list(resultcopy.values())

    fig = plt.figure(figsize=(7,6))
    ax = plt.gca()
    #此处为刻度不均匀，切记!!!用symlog而非log
    ax.set_xlim(0, 70)
    #ax.set_xscale('log')
    #x.set_xticks([0, 10, 100, 1000])
    ax.set_ylim(0, 250)
    #ax.set_yscale('log')
    #ax.set_yticks([0, 10, 100, 1000])
    # x = np.log10(x)
    # y = np.log10(y)
    ax.scatter(x, y, s=20)
    z1 = np.polyfit(x, y, 1)
    ynew = []
    for i in x:
        ynew.append(z1[0]* i + z1[1])
    # power_x = np.power(10,x)
    # power_y = np.power(10,ynew)
    ax.plot(x, ynew, 'r')
    ax.legend(labels =['original values','polyfit values'] , loc = 'upper right')
    ax.set_title("Figure 6 Degree distribution of web APIs in the API cooperation network")
    ax.set_xlabel("Node degree")
    ax.set_ylabel("The number of nodes")
    plt.show()