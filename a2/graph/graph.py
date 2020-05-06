# coding = utf-8




'''
LSH locality sentitive hash 

P(similar) = 1 - (1 - S^r)^b   

S : similarity of two items
r : rows per band
b : bands per signature matrix
'''


import numpy as np
from matplotlib import pyplot as plt

def lsh_graph():
    r_b = [(3, 10, '*', 'r=3, b=10'), (5, 20, 'o', 'r=5 b=20'), (5, 50, 'x', 'r=5 b=50')]
    s = np.arange(0.01, 1, 0.05)

    plt.title('LSH probability S_curve')
    for r, b, mark, label in r_b:
        p = 1 - (1 - s**r)**b
        plt.plot(s, p, marker=mark, label=label)
        plt.legend()
    plt.margins(0)
    plt.subplots_adjust(bottom=0.01)
    plt.ylabel('probability')
    plt.yticks([i*0.1 for i in range(0, 12, 1)])
    plt.xticks([i*0.01 for i in range(0, 100, 10)])
    plt.xlabel('Similarity')
    plt.show()



def pf_graph():
    k = np.arange(1, 10, 1)
    m = 2
    n = 10
    p = (1 - np.exp(- k*m/n))**k

    plt.plot(k, p, marker='*')
    plt.ylabel('probability of false-positive')
    plt.xlabel('the number of hash functions')
    plt.show()




if __name__ == "__main__":
    lsh_graph()
    pf_graph()
