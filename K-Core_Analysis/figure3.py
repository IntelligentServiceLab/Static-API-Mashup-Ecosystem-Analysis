###制作API Coperation Network
import itertools

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import scipy
from pyecharts import options as opts
from pyecharts.charts import Graph
import random


# 导入输出图片工具
from pyecharts.render import make_snapshot
from snapshot_phantomjs import snapshot




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
    G = nx.Graph()
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

#随机产生一个颜色值
def random_color():
    colors1 = '0123456789ABCDEF'
    num = "#"
    for i in range(6):
        num += random.choice(colors1)
    return num


if __name__ == "__main__":
    coperationNetwork = create_coperation_networkx("datasets/Mashups.csv")
    # 其中自己做的网络图存在self loops 需要去掉之后在进行k核分析
    coperationNetwork.remove_nodes_from(list(nx.isolates(coperationNetwork)))
    nodes = dict(coperationNetwork.degree)
    nodes = sorted(nodes.items(), key=lambda e: e[1], reverse=True)
    nodes = dict(nodes)
    #取度值从大到小排序的前100个
    top50 = list(nodes.keys())
    top50 = top50[0:50]
    sub = nx.subgraph(coperationNetwork,top50)
    dot = sub.nodes
    #这里的sub.nodes的数据结构并非list而是加密了的 需要装换一下变为list
    dot = list(dot)
    edges = sub.edges
    edges = list(edges)

    #构建图
    dotlist = []
    for i in range(50):
        color = random_color()
        #这里利用itemStyle来控制节点的颜色
        dotlist.append({"name": dot[i], "symbolSize": int((nodes[dot[i]]/500*50)), "itemStyle": {'color': color}})


    edgeslist = []
    for j in edges:
        edgeslist.append({'source': j[0], 'target': j[1]})


    c = (
        #opts.InitOpts为基础设置
        Graph(init_opts=opts.InitOpts(
            width='1500px',    #宽度
            height='800px',    #高度
            bg_color="white"   #图片背景 不设置的话默认为黑色
        ))
        .add("", dotlist, edgeslist, repulsion=8000, layout='force')  # layout='force'或'circular'
        .set_global_opts(title_opts=opts.TitleOpts(title="Fig. 3 Visualization of the Web API Collaboration Network", pos_bottom=True))
    )

    #c.render("E:/IntelligentServiceLab/picture/k-core/p2_figure3.png",delay=2)
    # 输出保存为图片  delay为延迟截图
    make_snapshot(snapshot, c.render("graph.html"), "E:/IntelligentServiceLab/picture/k-core/p2_figure3.png", PNG_FORMAT = "png",delay=20)