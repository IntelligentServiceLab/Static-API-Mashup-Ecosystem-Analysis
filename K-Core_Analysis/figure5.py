###制作API Coperation Network
import itertools

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from networkx import Graph
import networkx as nx
import scipy
import warnings

warnings.filterwarnings('error')




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
    coperationNetwork = create_coperation_networkx("datasets/Mashups.csv")
    #其中自己做的网络图存在self loops 需要去掉之后在进行k核分析
    coperationNetwork.remove_edges_from(nx.selfloop_edges(coperationNetwork))
    k0 = nx.k_core(coperationNetwork,0)
    k1 = nx.k_core(coperationNetwork, 1)
    k3 = nx.k_core(coperationNetwork, 3)
    k6 = nx.k_core(coperationNetwork, 6)
    k12 = nx.k_core(coperationNetwork, 12)
    k18 = nx.k_core(coperationNetwork, 18)
    k21 = nx.k_core(coperationNetwork, 21)
    k24 = nx.k_core(coperationNetwork, 24)
    k26 = nx.k_core(coperationNetwork, 26)

    kcore = [k0, k1, k3, k6, k12, k18, k21, k24, k26]
    anotation = ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)', '(g)', '(h)', '(i)']

    #得出每个节点的度将其
    for i in range(1,10):
        d = dict(nx.degree(kcore[i-1]))
        x = list(range(max(d.values()) + 1))
        y = [j for j in nx.degree_histogram(kcore[i-1])]


        try:
            x = np.log10(x)
            y = np.log10(y)
        except Warning:
            print("logx中x不能为0")
        # x = np.nan_to_num(x)
        # y = np.nan_to_num(y)

        #去掉x, y中的inf值
        dictxy = dict(zip(x,y))
        for key in list(dictxy.keys()):
            if dictxy.get(key)==-np.inf or key==-np.inf:
                del dictxy[key]

        x = list(dictxy.keys())
        y = list(dictxy.values())

        # 对散点图进行拟合
        z1 = np.polyfit(x, y, 1)
        k = '%.4f' % z1[0]
        b = '%.4f' % z1[1]
        formula = 'y = %sx + %s' % (k,b)

        ax = plt.subplot(3, 3, i)
        if i>=1 and i<=3:
            ax.set_ylim(0,3)
            ax.text(0.3, 2, formula)
            ax.text(2.5, 2.5, anotation[i-1])
            if i==1:
                ax.set_ylabel("lgN")
        if i>=4 and i<=6:
            ax.set_ylim(0,2)
            ax.set_yticks([0, 0.5, 1, 1.5, 2])
            ax.text(0.3, 1.5, formula)
            ax.text(2.5, 1.6, anotation[i-1])
            if i==4:
                ax.set_ylabel("lgN")
        if i>=7 and i<=9:
            ax.set_ylim(0,1)
            ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1])
            ax.text(0.2, 0.7, formula)
            ax.text(2.5, 0.8, anotation[i-1])
            if i==7:
                ax.set_ylabel("lgN")
            ax.set_xlabel("lgK")
        ax.set_xlim(0,3)
        ax.scatter(x, y, s=10)
        ynew = []
        for k in x:
            ynew.append(z1[0] * k + z1[1])
        ax.plot(x, ynew, 'r')
    plt.show()