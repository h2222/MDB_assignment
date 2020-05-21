import numpy as np
from numpy import *
import matplotlib.pyplot as plt
import pandas as pd

names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
dataSet = pd.read_csv('iris.data', names=names)

dataSet['class'][dataSet['class']=='Iris-setosa']=0
dataSet['class'][dataSet['class']=='Iris-versicolor']=1
dataSet['class'][dataSet['class']=='Iris-virginica']=2

def distEclud(arrayA,arrayB):
    d = arrayA - arrayB
    # 同纬度相减, 最后求和
    # 例子: [[1, 2],[3, 4]] - [[5, 6], [7, 8]]
    #       [[1-5, 2-6], [3-7, 4-8]]
    #       ([[-4, -4], [-4, -4]])^2
    #        [[16, 16], [16, 16]]
    #        [32, 32]
    #        64
    distance = np.sum(np.power(d,2))
    return distance

def randCent(dataSet,k):
    m=dataSet.shape[0]
    centroidsIndex=[]
    dataIndex=list(range(m)) # 0到m-1的list(表示数据的index)

    for i in range(k):# k为分类数
        randIndex=random.randint(0,len(dataIndex)) # 0到m之间的随机数
        centroidsIndex.append(dataIndex[randIndex]) # 随机选取三个聚心的index, 存入
        del dataIndex[randIndex] # 释放
    centroids = dataSet.iloc[centroidsIndex] # 抓取centroids数据,shap为[3, 2]
    return mat(centroids) # 返回矩阵 centroids[3, 2]

def kMeans(dataSet, k):
    # 大小
    m = dataSet.shape[0]
    clusterAssment = mat(zeros((m,2)))# 大小与dataset一致的0矩阵[size, 2]
    centroids = randCent(dataSet, k)# centroids[3, 2]
 
    clusterChanged = True
    iterTime=0

    while clusterChanged:   
        clusterChanged = False # 如果聚类改变,停止while         
 
        for i in range(m): # 循环数据data

            minDist = np.inf; minIndex = -1 #最大距离+inf, 最小距离centroids的index

            for j in range(k): # 循环分类
                
                # 计算各个centroids 到 每个数据的距离(计算为shape:[1, 2] - [1, 2])
                # 返回值
                distJI = distEclud(centroids[j,:],dataSet.values[i,:])

                if distJI < minDist: # 如果当前centroids小于最小距离(初始化为+inf)
                    minDist = distJI # 当前距离设置为最小距离
                    minIndex = j     # 当前centroids的index设置为min index

            # clusterAssement, 初始化为 shape为[size, 2]的 0 矩阵
            # 如果 centroids的index在clusterAseement中找不到
            # 继续while大循环, 如果找到了 clusterchanged就是true
            # 注意, 这里要求每一个数据的centroids的idx都不改变, 才能是clusterChanged为
            # false, 即完成聚类
            if clusterAssment[i,0] != minIndex:
                clusterChanged = True
            
            # 当前数据对应k个centroids, 对于有最小距离的centroids, 将它的index存入clusters
            # 最后得得到的结果是每一个点都会被分配一个centroids的index, 相同index的数据为
            # 同一个聚类
            print('+++',clusterAssment.shape)
            clusterAssment[i,:] = minIndex,minDist**2 

        for cent in range(k):  # 循环拿取分类
            
            # matrix.A 方法, 将matirx -> nd.array
            # 例: [[1, 2, 3],
            #      [2, 3, 4],
            #      [3, 4, 5]]   Matrix
            # Matrix.A  --> nd.array
            # clusterAssement 为每一个数据选择的centroids的index组成的array
            # 拿取当前分类点的ptsInClust
            ptsInClust = dataSet.iloc[nonzero(clusterAssment[:,0].A==cent)[0]]
            print('k:'+str(cent),type(ptsInClust))

            # 根据聚类情况, 更新centroids
            centroids[cent,:] = mean(ptsInClust, axis=0) 
    return centroids, clusterAssment

def datashow(dataSet,k,centroids,clusterAssment):  
    from matplotlib import pyplot as plt
    num,dim=shape(dataSet)  
    marksamples=['or','ob','og','ok','^r','^b','<g'] 
    for i in range(num):
        markindex=int(clusterAssment[i,0])
 
        plt.plot(dataSet.iat[i,0],dataSet.iat[i,1],marksamples[markindex],markersize=5)
     
    markcentroids=['o','*','^']
    label=['0','1','2']
    c=['red','blue','green']
    for i in range(k):
        plt.plot(centroids[i,0],centroids[i,1],markcentroids[i],markersize=15,label=label[i],c=c[i])
        plt.legend(loc = 'upper left')
    plt.xlabel('sepal length')  
    plt.ylabel('sepal width') 
   
    plt.title('k-means cluster result')      
    plt.show()

if __name__=='__main__':
    datamat=dataSet.loc[:, ['sepal-length','sepal-width']]
    k=3 
    mycentroids,clusterAssment=kMeans(datamat,k)
    print(mycentroids.shape, clusterAssment.shape)
    datashow(datamat,k,mycentroids,clusterAssment)

