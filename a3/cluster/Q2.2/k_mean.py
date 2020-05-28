#coding=utf-8

import pandas as pd
import numpy as np
from numpy import mat, zeros, power, sum, nonzero, mean
from random import randint


distance = lambda x, y: sum(power(x-y, 2))


class Kmean:
    
    def __init__(self):
        self.data = None
        self.size = 0
        self.data_cls = 0 # data with labels
        self.cls = 0 # labels
        self.centroids = []

    def load(self, path='iris.data', keep=['sepal-length', 'sepal-width']):
        n = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
        c = {'Iris-setosa':0, 'Iris-versicolor':1, 'Iris-virginica':2}
        df = pd.read_csv(path, names=n)
        for i in c:
            df.loc[df['class'] == i, 'class'] = c[i]
        data = df.loc[:, keep] 
        return data


    def initialize(self, data, clss):
        self.cls = clss
        self.size = len(data)
        self.data_cls = mat(zeros((self.size, 2))) # clusterAssment
        
        data_idx = [i for i in range(self.size)]
        idx_randint = [randint(0, self.size) for i in range(self.cls)]
        idx_centroids = [data_idx[i] for i in idx_randint]
        self.centroids = mat(self.data.iloc[idx_centroids])


    def kmean_alg(self):
        
        RUN = True
        while RUN:
            RUN = False
            for i in range(self.size):
                MINDSTS = np.inf
                MINIDX = -99
                # lopping class to find mini distance
                for j in range(self.cls):
                    dsts = distance(self.centroids[j,:], self.data.values[i,:])
                    print(dsts)
                    if dsts < MINDSTS:
                        MINDSTS = dsts
                        MINIDX = j
                
                self.data_cls[i, :] = MINIDX, power(MINDSTS, 2)

            # re-centralize the centroids
            for c in range(self.cls):
                middle = None
                middle = self.data.iloc[nonzero(self.data_cls[:,0].A==c)[0]]
                self.centroids[c, :] = mean(middle, axis=0)
                RUN = True if self.data_cls[i, 0] != MINIDX else False
        print('good')
    

    def datashow(self):  
        from matplotlib import pyplot as plt
        num,dim=self.data.shape
        print(self.data)
        marks_l=['*r','>g','+b','ok','^r','^b','<g'] 
        for i in range(self.size):
            mark=int(self.data_cls[i,0])
            plt.plot(self.data.iat[i,0], self.data.iat[i,1], marks_l[mark], markersize=5)
        
        markcentroids=['o','*','^']
        label=['0','1','2']
        c=['red','green','blue']

        for i in range(self.cls):
            plt.plot(self.centroids[i,0], self.centroids[i,1],markcentroids[i],markersize=10,label=label[i],c=c[i])
            plt.legend(loc = 'best') 
    
        plt.title('k-means cluster') 
        plt.savefig('k-mean')     
        plt.show()


    def run(self, path, keep, clss=3):
        self.data = self.load(path=path, keep=keep)
        self.initialize(data=self.data, clss=clss)
        self.kmean_alg()
        self.datashow()
        print(type(self.centroids))




if __name__ == "__main__":
    cluster = Kmean()
    cluster.run(path='./iris.data', keep=['sepal-length', 'sepal-width'])



   
    



