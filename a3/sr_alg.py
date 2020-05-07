# coding = utf-8

import os, sys
from random import randint, shuffle
import itertools
import copy


def sample_data(path, rate):

    sample = []
    rannum = [i for i in range(rate)]
    shuffle(rannum)

    with open(path, encoding='utf-8') as f:
        for line in f.readlines():
            s = [i for i in map(int, line.split(' ')[:-1])]
            r = randint(0, 100)
            # choose 1% of dataset as sample, when random number == 49, choose it as sample.
            if r in rannum:
                sample.append(s)
    # relase memory
    # print(sys.getsizeof(f.readlines()))
    del f

    return sample





def apriori_v2(data):

    p = 1
    thresh = 10
    save = set()
    static = {}
    temp = copy.deepcopy(data)

    # print(temp)

    while len(temp) > 2:
        for line in temp:
            for i in line:
                save.add(i)

        cmb = list(itertools.combinations(save, p))

        for c in cmb:
            for d in data:             
                if set(c).issubset(set(d)):
                    if not c in static:
                        static[c] = 1
                    else:
                        static[c] += 1

        static = { k:v for k, v in sorted(static.items(), key=lambda x: x[1], reverse=True) if v >= 10}
        temp = [list(i) for i in static.keys()]

        # 更新分类处理
        p += 1        
        print(temp)




def apriori(data, itemset=None, c=1):

    # if c == 4:
        # return data 

    thresh = 10
    # step one: filter
    
    static = {}
    temp = []

    if itemset ==  None:
        for i in data:
            for j in i:
                temp.append(j)
    else:
        for i in itemset:
            for j in i:
                temp.append(j)
    
    comb = list(itertools.combinations(temp, c))

    print(len(data))
    print(len(comb))
    for s in comb:
        for d in data:
            print([*s])
            print(d)
            if [*s] in d:
                # print(set(s),set(d))
                if not s in static:
                    static[s] = 1
                else:
                    static[s] +=1

    print(static)

    del data
    # sort and filter
    static = { k:v for k, v in sorted(static.items(), key=lambda x: x[1], reverse=True) if v >= thresh}
    data = [list(i) for i in static.keys()]
    print(data)

    # c += 1
    # apriori(data=data, c=c)


    



if __name__ == "__main__":

    p, n, fs = next(os.walk('./dataset'))

    dataset = [p +'/'+f for f in fs if not '.gz' in f]

    for data in dataset[:1]:
        print(data)
        sample = sample_data(data, rate=1)
        apriori_v2(sample)
