## a3 -1-1 simple randomized algorithm

### 1. introduction

`sr_alg.py` : simple randomized algorithm based on Apriori<br>

### 2. params(in main function)
1. `rr` : the save path
2. `rate`: the sample rate of dataset, 0.01 = 1% , 0.02 = 2%, 0.05 = 5%, 0,1 = 10%
3. `thresh`: the threshold of apriori algorithm, based on experiments, setting threshold 76 ~ 99 
4. `dataset` : [0:1] is chess, [1:2] is connect, ....
   
### 3. how to run
1. using terminal(cmd), set suitable params and run `python sr_alg.py`, do not use pycharm or other IDE.
2. the result will be saved in `./result/data/result_sra_xxx_rate.txt`, this file store the total frequent itemset.

<br><br><br>

## a3 -1-2 SON algorithm

### 1. introduction
`son_alg.py` : SON algorithm based on apriori<br>

### 2. params(in main function)
1. `rr`: save path
2. `split_num`: how many chuck you split.
3. `dataset` : [0:1] is chess, [1:2] is connect, ....

### 3. how to run
1. using terminal(cmd), set suitable params and run `python son_alg.py`, DO NOT use pycharm or other IDE.
2. the result will be saved in `./result/data/result_son_xxx_1.txt`, this file store the total frequent itemset.