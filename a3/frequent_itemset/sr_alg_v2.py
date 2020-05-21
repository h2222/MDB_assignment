# coding=utf-8
import os
from sr_alg import SimpleRondomAlg



def createC1(dataset):
    C1 = []
    for transaction in dataset:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    C1 = sorted(C1)
    # fronzenset as key, stable(do not have .add .remove func)
    return list(map(frozenset, C1))



def scanD(D, Ck, minSupport):
    ssCnt = {}
    # statistic item number in dataset
    for tid in D:
        for can in Ck:
            if can <= tid:
                if can not in ssCnt:
                    ssCnt[can] = 1
                else:
                    ssCnt[can] += 1
    
    numItems = float(len(D))
    retList = []
    supportData = {}

    for k in ssCnt:
        support = ssCnt[k] / numItems
        # randomized sample alg --> threshold / 100
        if support >= (minSupport/100):
            retList += [k]
        supportData[k] = support
    
    return retList, supportData



def aprioriGen(Lk, k):
    retList = []
    lenLk = len(Lk) # k-1 th frequence itemset

    for i in range(lenLk):
        for j in range(i+1, lenLk):
            L1 = list(Lk[i])[:k-2]
            L2 = list(Lk[j])[:k-2]
            L1.sort(); L2.sort()
            if L1 == L2:
                retList.append(Lk[i] | Lk[j])

    # print(retList)
    return retList




def apriori(dataset, minSupport=0.5):
    D = list(map(set, dataset))

    # print('.................................')
    # print(D)
    # print('.................................')

    C1 = createC1(dataset)
    L1, supportData = scanD(D, C1, minSupport)
    L = [L1]
    k = 2
    # print(k,'**********'*20)
    # print(C1)
    # print(k, '***********'*20)
    
    while(len(L[k-2]) > 0):
        # print(k, 'xxxxxxxxxxx')
        # print(L[k-2])
        # print(k, 'xxxxxxxxxxx')  
        # 组合 combination  
        Ck = aprioriGen(L[k - 2], k) # selection indicate itemset
        # print(k,'**********'*20)
        # print(Ck)
        # print(k,'***********'*20)
        Lk, supK = scanD(D, Ck, minSupport)
        supportData = supK
        L.append(Lk) # update indicate frequent itemset
        # print(k, 'LK'*50)
        # print(L)
        # print(k, 'LK'*50)
        k += 1
    
    return L, supportData



if __name__ == "__main__":
    p, n, fs = next(os.walk('./dataset'))

    dataset = [p +'/'+f for f in fs if not '.gz' in f]
    sra = SimpleRondomAlg(rate=0.1, thresh=0.5)


    for data in dataset[4:5]:
        # data = [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]
        sample = sra.sample(data)
        L, supportData = apriori(sample)

    print('-'*100)
    print(L)
    print('-'*100)
    print(supportData)
    print('-'*100)







