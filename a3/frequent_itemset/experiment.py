# coding=utf-8
import pandas as pd




def experiement(path1, path2):
    df1 = pd.read_csv(path1, header=None, encoding='utf-8-sig')
    df2 = pd.read_csv(path2, header=None, encoding='utf-8-sig')


    joint = set(df1[0]) & set(df2[0])
    total = set(df1[0]) | set(df2[0])
    
    rate1 = len(joint) / len(df1)
    rate2 = len(joint) / len(df2)

    print('SON result:')
    print('--'*20)
    print(set(df1[0]))
    print('SRA result')
    print('--'*20)
    print(set(df2[0]))
    print('joint result')
    print('--'*20)
    print(set(joint))
    print('--'*20)
    print('the proportion of joint result in SON result')
    print(rate1)
    print('the proportion of joint result in SRA result')
    print(rate2)





if __name__ == "__main__":
    path1 = './result/T10/result_son_0_0.05_.txt'
    path2 = './result/T10/result_sra_0_0.05_.txt'

    experiement(path1, path2)