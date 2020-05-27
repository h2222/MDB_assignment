# coding = utf-8

import os
import pandas as pd
from random import sample
from multiprocessing import Pool, cpu_count
from functools import partial

class SONAlg:
    def __init__(self, split_num, rate):
        self.rate = rate
        self.cpu_num = cpu_count()
        self.sample = None
        self.split_num = split_num
        self.data_size = None

    # set number of blocks. Generally, we think that the number of block equal to the number of CPU cores
    def split_block(self, path='./data_path', split_num = 0):
        process_size = [0]
        process_sl = []

        df = pd.read_csv(path, header=None, encoding='utf-8-sig')
        self.data_size = len(df)

        # split block
        split_size = self.data_size // split_num
        remain = self.data_size % split_num
        process_sl = [[i, i+split_size] for i in range(0, self.data_size, split_size)]        
        # add remain data
        process_sl[-1][1] += remain
        return process_sl


    def sample_data(self, se, path='./data_path', rate=1):        
        s = []
        total = 0
        remain = 0

        # split block
        df = pd.read_csv(path, header=None, encoding='utf-8-sig')
        if se != None:
            df = df.loc[se[0]:se[1]]

        # simpling
        # df = df.sample(frac=rate)

        ss = []
        for _, x in df.iterrows():
            s = list(x)[0].strip().split(' ')
            s = list(map(int, s))
            ss.append(s)
        if se != None:
            print('the chuck between {0} - {1}, data is {2}, Process ID:{3}'.format(se[0], se[1], path, os.getpid()))
        return ss

    
    def createC1(self, dataset):
        C1 = []
        for transaction in dataset:
            for item in transaction:
                if not [item] in C1:
                    C1.append([item])
        C1 = sorted(C1)
        return list(map(frozenset, C1))


    def filter(self, D, Ck):
        itemset = {}
        for tid in D:
            for can in Ck:

                if can <= tid:
                    if not can in itemset:
                        itemset[can] = 1
                    else:
                        itemset[can] += 1
        
        numItems = float(len(D))
        retList = []
        supportData = {}
        i = 0        
        bp =  self.split_num / self.data_size

        for k in itemset:
            support = itemset[k] / numItems

            # if support > (1/ bp)*bp*minsupport:
            supportData[k] = support
                # retList += [k]
            i += 1            
        
        supportData  = dict(sorted(supportData.items(), key=lambda  x: x[1], reverse=True))
        supportData_v2 = {}
        for _, k in zip(range(7), supportData):
            supportData_v2[k] = supportData[k]
            retList += [k]

        return retList, supportData_v2


    def apriori_gen(self, Lk, k):
        retList = []
        lenLk = len(Lk)

        for i in range(lenLk):
            for j in range(i+1, lenLk):
                L1 = list(Lk[i])[:k-2]
                L2 = list(Lk[j])[:k-2]
                L1.sort(); L2.sort()
                if L1 == L2:
                    retList.append(Lk[i] | Lk[j])

        return retList


    def apriori(self, sample, path='data_path', less_sample_test=False):

        if less_sample_test:
            sample = [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]
        
        self.sample = list(map(set, sample))
        C1 = self.createC1(self.sample)
        L1, supportData=self.filter(self.sample, C1) 
        L = [L1]
        k = 2

        while(len(L[k-2]) > 0):
            Ck = self.apriori_gen(L[k-2], k)
            Lk, supk = self.filter(self.sample, Ck)
            supportData.update(supk)
            L.append(Lk)
            k += 1
        
        print('good run Apriori, Process ID:{}'.format(os.getpid()))
        return L[:-1]



    def run(self, path='default', save_to='default'):
        
        if os.path.exists(save_to):
            os.remove(save_to)
        open(save_to, 'w', encoding='utf-8-sig')
        
        p = Pool(self.cpu_num)
        # get splited block 
        process_sl = self.split_block(path=path, split_num=self.split_num)        
        print(len(process_sl))

        # based on the beign and end position to get spliting data
        sample_data_v2 = partial(self.sample_data, path=path, rate=self.rate)
        son_r = p.map(sample_data_v2, process_sl)

        # because the last sample size is smaller than other's, we add last block add to other blocks.
        if len(son_r[-1]) < (len(son_r[-2]) / 2):
            son_r[-2] += son_r[-1]
            son_r = son_r[:-1]
        p.close()

        # run Apriori in different chuck
        p2 = Pool(self.cpu_num)
        apriori_v2 = partial(self.apriori, path=path, less_sample_test=False)
        multi_sra_r = p2.map(apriori_v2, son_r)  
        p2.close()

        # collect candidate itemset from different chuck
        map1 = set()
        for block in multi_sra_r:
            for item in block:
                for i in item:           
                        map1.add(i)
        map2 = list(map1)
        print('results from different parts'+'========'*20, ' \n', map2, '\n', '========'*20)

        # save_result
        with open(save_to, 'a', encoding='utf-8-sig') as f:
            for i in map2:
                f.write(str(set(i))+'\r')


    
if __name__ == "__main__":

    p, n, fs = next(os.walk('./dataset'))
    dataset = [p +'/'+f for f in fs if not '.gz' in f]
    
    #               0       1           2       3       4       5       6
    # dataset = [chess,  connect,  mushroom,   pumsb,  pumsb,  T10,    T40  ]
    rr = 'T40'
    rate = 1 # fixed 1
    if not os.path.exists('./result/'+rr):
        os.mkdir('./result/'+rr)
    save_path = './result/'+rr+'/result_son_{0}_{1}_.txt'.format(rr, rate)
    
    for data in dataset[6:] :  # set the dataset that you want to test 
        son = SONAlg(rate=rate,  split_num=10)
        son.run(data, save_to=save_path)