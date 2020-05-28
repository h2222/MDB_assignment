# coding = utf-8

import os
from random import sample
import pandas as pd



class SimpleRondomAlg:
    def __init__(self, rate, thresh):
        self.rate = rate
        self.thresh = thresh


    def sample_v2(self, path='./data_path', rate=0.01):
        df =pd.read_csv(path, header=None, encoding='utf-8-sig')
        # shuffle data and sampling data
        df = df.sample(frac=rate).reset_index(drop=True)
        
        ss = []
        for i, x in df.iterrows():
            s = list(x)[0].split(' ')[:-1]
            s = list(map(int, s))
            ss.append(s)
        return ss


    
    def createC1(self, dataset):
        C1 = []
        for transaction in dataset:
            for item in transaction:
                if not [item] in C1:
                    C1.append([item])
        C1 = sorted(C1)
        return list(map(frozenset, C1))


    def filter(self, D, Ck, minsupport):
        
        itemset = {}
        for tid in D:
            for can in Ck:
                # if len(Ck[0]) > 1:
                #     print(can, '\n', tid)
                if can <= tid:
                    if not can in itemset:
                        itemset[can] = 1
                    else:
                        itemset[can] += 1
        
        retList = []
        supportData = {}
        numItems = float(len(D))
        i = 0
        # if len(Ck[0])>1:
        #     print('+=+'*20)
        #     print(itemset)
        #     print('+=+'*20)

        for k in itemset:
            support = itemset[k] / numItems
            # filtering
            if support >= (minsupport/100):    ## 修改thresh hold 规则
                retList += [k]
                supportData[k] = support
            i += 1

        supportData  = dict(sorted(supportData.items(), key=lambda  x: x[1], reverse=True))        
        # supportData_v2 = {}
        # for _, k in zip(range(int(i)), supportData):
        #     supportData_v2[k] = supportData[k]
        #     retList += [k]

        return retList, supportData


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

        print(retList)
        return retList
        

    def run(self, path='data_path', less_sample_test=False):
        
        if not less_sample_test:
            sample = self.sample_v2(path=path, rate=self.rate)
            print(sample[:10])
            # print('sample size:', len(sample))
        else:   
            sample = [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]
        
        sample = list(map(set, sample))
        C1 = self.createC1(sample)
        L1, supportData=self.filter(sample, C1, self.thresh) 
        L = [L1]
        k = 2

        print('=+='*20)
        print(len(C1[0]), ':',supportData)

        while(len(L[k-2]) > 0):
            Ck = self.apriori_gen(L[k-2], k)
            if len(Ck) != 0:
                print('=+='*50)
                print(len(Ck[0]), ':',supportData)
            Lk, supk = self.filter(sample, Ck, self.thresh)
            supportData.update(supk)
            L.append(Lk)
            k += 1

        return L, supportData


            
if __name__ == "__main__":

    p, n, fs = next(os.walk('./dataset'))
    dataset = [p +'/'+f for f in fs if not '.gz' in f]

    ## params    
    rr = 'chess'
    rate=0.1
    thresh = 96

    #               0       1           2       3       4            5       6
    # dataset = [chess,  connect,  mushroom,   pumsb,  pumsb_star,  T10,    T40  ]
    for data in dataset[0:1]:
        print('dataset:', data)
        sra = SimpleRondomAlg(rate=rate, thresh=thresh)

        L, supportData = sra.run(data, less_sample_test=False)
        print('-'*50)
        print(L[:-1])
        print('-'*50)
         
        # save result
        save_to = './result/'+rr+'/result_sra_{}_{}_.txt'.format(rr, rate)
        if os.path.exists(save_to):
            os.remove(save_to)
            open(save_to, 'w', encoding='utf-8-sig')
        
        with open(save_to, 'a', encoding='utf-8-sig') as f:
            for x in L[:-1]:
                for i in x:
                    f.write(str(set(i))+'\r')
        del sra