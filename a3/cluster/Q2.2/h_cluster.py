# coding=utf-8


'''
层次聚类
 implement hierarchical cluster with a list of data [1, 2, 3....]
'''

from itertools import combinations
import numpy as np
from random import randint

def hcluster(data=[1,4,9,16,25,36,49,64,81], cluster={}, centroid_list=[]):

    # 出递归条件, data长度 小于 2, 两聚类中心就停
    if len(data) <= 2:
        return data, cluster, centroid_list

    result = []
    min_d = np.inf # 初始化, c1 c2 为距离最短的两个点, mid_d他们之间的最短距离
    c1 = -99
    c2 = -99
    for x, y in combinations(data, 2): # 循环一下, 算一下距离, 找 c1 c2
        distance = np.abs(x - y)
        if distance < min_d:
            min_d = distance
            c1 = x
            c2 = y
    
    centroid = np.mean([c1, c2]) # 算中心, 并且把每次的中心储储起来
    centroid_list.append(centroid)


    # 建立一个空聚类, 第一次里面啥都没有, 建立一个新cluster, 并且把c1 c2 添加进去
    # 因为聚类的类别绝对不能重复, 所以采样hash法来, 实现
    if cluster == {}:
        cluster['C'+str(hash(centroid))] = []
        cluster['C'+str(hash(centroid))] += [c1]
        cluster['C'+str(hash(centroid))] += [c2]
    else:
        # 后面有聚类了, 判断一下c1 c2是不是中心点,  
        # 分几种情况
        # 1, c1 为中心, c2不是, 把c2并入c1的聚类中
        # 2, c2 为中心点, c1不是, 把c1并入c2的聚类中
        # 3, c1 c2 都不是中心点, 直接建立一个新聚类把c1 c2放进去
        # 这样做有一个缺点, 不能实现聚类融合, 就是如果c1 c2 分别是两个聚类的中心, 边界会挤压但不会融合
        c1_cen = c1 in centroid_list
        c2_cen = c2 in centroid_list
        keys = cluster.keys()
        for k in list(keys):
            if c1_cen and not c2_cen:
                cluster[k] += [c2]
            elif c2_cen and not c1_cen:
                cluster[k] += [c1]
            elif not c1_cen and not c2_cen:
                cluster['C'+str(hash(centroid))] = []
                cluster['C'+str(hash(centroid))] += [c2]
                cluster['C'+str(hash(centroid))] += [c1]

    # 从data 中移除 c1 和 c2 并添加 中心, 制作新的数据
    data.remove(c1)
    data.remove(c2)
    data.append(centroid)
    print('good')

    # 递归新数据, 聚类收集字典 和 中心点 list 一块得递归
    result, cluster, centroid_list = hcluster(data=data, cluster=cluster, centroid_list=centroid_list)
    
    return result, cluster, centroid_list    

if __name__ == "__main__":
    r, c, l = hcluster()

    print(r) # 最终聚类中心
    print(c) # 聚类字典
    print(l) # 每次的中心点

