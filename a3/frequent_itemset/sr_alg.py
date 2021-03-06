# coding = utf-8

import os, sys
from random import sample



class SimpleRondomAlg:
    def __init__(self, rate, thresh):
        self.rate = rate
        self.thresh = thresh

    def sample(self, path='./data_path'):
        s = []
        with open(path, encoding='utf-8') as f:
            for line in f.readlines():
                # pre-preparing
                line2 = [i for i in map(int, line.split(' ')[:-1])]
                # total * (toal * rate) = num
                num = int(len(line2)*self.rate)
                # sample
                # if num < 1 , set the sample number to 1
                num = 1 if num < 1 else num
                ss = list(sample(line2, num))
                s.append(ss)
        # relase memory
        # print(sys.getsizeof(f.readlines()))
        del f
        return s

    
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
            # if support >= (minsupport/100):    ## 修改thresh hold 规则
                # retList += [k]
            supportData[k] = support
            i += 1

        supportData  = dict(sorted(supportData.items(), key=lambda  x: x[1], reverse=True))        
        supportData_v2 = {}
        for _, k in zip(range(int(i*minsupport)), supportData):
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

        # print(retList)
        return retList
        

    def run(self, path='data_path', less_sample_test=False):
        
        if not less_sample_test:
            sample = self.sample(path=path)
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
    
    print(dataset[5])
    rr = 40
    #               0       1           2       3       4       5       6
    # dataset = [chess,  connect,  mushroom,   pumsb,  pumsb,  T10,    T40  ]
    for data in dataset[6:]:
        rate=0.01
        print('dataset:', data)
        sra = SimpleRondomAlg(rate=rate, thresh=0.1)
        L, supportData = sra.run(data, less_sample_test=False)
        print('-'*50)
        print(L[:-1])
        print('-'*50)
         
        # save result
        save_to = './result/T40/result_sra_{}_{}_.txt'.format(rr, rate)
        if os.path.exists(save_to):
            os.remove(save_to)
            open(save_to, 'w', encoding='utf-8-sig')
        
        with open(save_to, 'a', encoding='utf-8-sig') as f:
            for x in L[:-1]:
                for i in x:
                    f.write(str(set(i))+'\r')

        rr += 1
        del sra