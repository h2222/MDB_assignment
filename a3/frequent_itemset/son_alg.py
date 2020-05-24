# coding = utf-8

import os
from random import sample
from multiprocessing import Pool, cpu_count
from functools import partial

class SONAlg:
    def __init__(self, rate, thresh):
        self.rate = rate
        self.thresh = thresh
        self.cpu_num = cpu_count()
        self.sample = None


    # set number of blocks. Generally, we think that the number of block equal to the number of CPU cores
    def split_block(self, path='./data_path'):
        process_size = [0]
        process_sl = []

        # compute the size of block. For example, there are 1000 data,  we split data as 5 blocks, so 1 block has 200 data
        f = open(path, 'r', encoding='utf-8')
        num = len(f.readlines())
        part = num // self.cpu_num
        final = num % self.cpu_num
        process_size += [part]*self.cpu_num + [final]
        
        # set begin and end position. For example, [0, 200) [200, 300) ... [800, 1000)
        for i in range(len(process_size)):
            if process_size[i] != process_size[-1]:
                process_size[i+1] += process_size[i]

        for i in range(len(process_size))[:-1]:
            start = process_size[i]
            end = process_size[i+1]
            process_sl += [(start, end)]
        del f
        return process_sl


    def sample_data(self, se, path='./data_path'):        
        s = []
        total = 0
        remain = 0
        with open(path, encoding='utf-8') as f:
            #  splite data as block
            for line in f.readlines()[se[0]:se[1]]:
                line2 = [i for i in map(int, line.split(' ')[:-1])]
                num = int(len(line2)*self.rate)
                num = 1 if num < 1 else num
                ss =list(sample(line2, num))
                s.append(ss)

            print('{0} - {1} sample complete, data is {2}, Process ID:{3}'.format(se[0], se[1], path, os.getpid()))
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

                if can <= tid:
                    if not can in itemset:
                        itemset[can] = 1
                    else:
                        itemset[can] += 1
        
        numItems = float(len(D))
        retList = []
        supportData = {}
        i = 0        

        for k in itemset:
            support = itemset[k] / numItems
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

        return retList


    def apriori(self, sample, path='data_path', less_sample_test=False):

        if less_sample_test:
            sample = [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]
        
        self.sample = list(map(set, sample))
        C1 = self.createC1(self.sample)
        L1, supportData=self.filter(self.sample, C1, self.thresh) 
        L = [L1]
        k = 2

        while(len(L[k-2]) > 0):
            Ck = self.apriori_gen(L[k-2], k)
            Lk, supk = self.filter(self.sample, Ck, self.thresh)
            supportData.update(supk)
            L.append(Lk)
            k += 1
        
        print('good run SRA, Process ID:{}'.format(os.getpid()))
        return L[:-1]



    def run(self, path='default', save_to='default'):
        
        if os.path.exists(save_to):
            os.remove(save_to)
        open(save_to, 'w', encoding='utf-8-sig')
        
        p = Pool(self.cpu_num)
        # get splited block 
        process_sl = self.split_block(path=path)        
        print(process_sl)

        # based on the beign and end position to get spliting data
        sample_data_v2 = partial(self.sample_data, path=path)
        son_r = p.map(sample_data_v2, process_sl)

        # because the last sample size is smaller than other's, we add last block add to other blocks.
        son_r[-2] += son_r[-1]
        son_r = son_r[:-1]
        p.close()

        # Simple Randomized Alg (Map1)
        p2 = Pool(self.cpu_num)
        apriori_v2 = partial(self.apriori, path=path, less_sample_test=False)
        multi_sra_r = p2.map(apriori_v2, son_r)  
        p2.close()
        

        # Reduce 1
        map1 = set()
        for block in multi_sra_r:
            for item in block:
                for i in item:           
                        map1.add(i)
        map2 = list(map1)
        print('results from different parts'+'========'*20, ' \n', map2, '\n', '========'*20)

        # total data, (0, -1) mean begin to end
        total = self.sample_data(se=(0, -1), path=path)
        total = list(map(set, total))

        # Map2 + Reduce 2
        Lk, supk = self.filter(total, map2, self.thresh)
        print('final result '+'========='*20, '\n', supk)

        # save_result
        with open(save_to, 'a', encoding='utf-8-sig') as f:
            for i in Lk:
                print(set(i))
                f.write(str(set(i))+'\r')


    
if __name__ == "__main__":

    p, n, fs = next(os.walk('./dataset'))
    dataset = [p +'/'+f for f in fs if not '.gz' in f]
    
    #               0       1           2       3       4       5       6
    # dataset = [chess,  connect,  mushroom,   pumsb,  pumsb,  T10,    T40  ]
    for data in dataset[5:6]:  # set the dataset that you want to test 
        rr = 0
        rate = 0.1
        print('dataset:', data)
        son = SONAlg(rate=rate, thresh=0.1)
        son.run(data, save_to='./result/result_son_{0}_{1}_.txt'.format(rr, rate))
        rr += 1