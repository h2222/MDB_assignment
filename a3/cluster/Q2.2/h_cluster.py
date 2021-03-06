# coding=utf-8


'''
 implement hierarchical cluster with a list of data [1, 2, 3....]
'''

from itertools import combinations
import numpy as np
from random import randint

def hcluster(data=[1,4,9,16,25,36,49,64,81], cluster={}, centroid_list=[]):

    # the condition that stop the recursion 
    # if the data length less than 2, return final data(final centroid), cluster, and centroid_list
    if len(data) <= 2:
        return data, cluster, centroid_list

    result = []
    min_d = np.inf # initialization, c1 and c2 are 2 point of minimized distance, and mid_d is minimized distance.
    c1 = -99
    c2 = -99
    for x, y in combinations(data, 2):# find mid_d and c1, c2
        distance = np.abs(x - y)
        if distance < min_d:
            min_d = distance
            c1 = x
            c2 = y
    
    centroid = np.mean([c1, c2]) # caculate centroid and save it into centroid_list
    centroid_list.append(centroid)


    # if the cluster is dict, the key(str) is cluster name, and value(list) is the value in the cluster.
    # first, there are nothing in cluster, so we build the first cluster, the value of first cluster are c1 and c2 
    if cluster == {}:
        cluster['C'+str(hash(centroid))] = []
        cluster['C'+str(hash(centroid))] += [c1]
        cluster['C'+str(hash(centroid))] += [c2]
    else:
        # there are different condition in here  
        # 1. c1 is centroid, and c2 is not centroid, so we put c2 in c1's cluster
        # 2. c2 is centroid, and c1 is not centroid, so we put c1 in c2's cluster
        # 3. both c1 and c2 are not centroids, so we build a new cluster and put c1 and c2 into it.
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

    # we remove the c1 and c2 from data and put new centroid into data
    data.remove(c1)
    data.remove(c2)
    data.append(centroid)
    print('good')

    # do the recursive method, and use new data
    result, cluster, centroid_list = hcluster(data=data, cluster=cluster, centroid_list=centroid_list)
    
    return result, cluster, centroid_list    

if __name__ == "__main__":
    r, c, l = hcluster()

    print('cluster :\n', c) 

