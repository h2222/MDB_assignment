# coding=utf-8
import os


class PageRank:

    def __init__(self, kvps, pr, node_size):
        self.kvps = kvps
        self.pr = pr
        self.node_size = node_size        
        # pass

    def initialize(self):
        for k in self.kvps:
            col = self.kvps[k]['out_link']
            self.kvps[k]['pr'] = self.pr
            self.kvps[k]['out_link'] = dict(zip( col, map(lambda x: self.pr, col.values())))
        print('load completed')


    def compute(self, num=20, beta=0.8):
        for i in range(num):
            print('epoch:', i)
            for k in self.kvps:
                pr = self.kvps[k]['pr']
                out_link = self.kvps[k]['out_link']
                # taxation
                # 稀疏矩阵相乘
                # 矩阵相乘 
                out_value = beta * pr * 1/len(out_link)
                ## update out_link value
                for out_k in out_link:
                    try:
                        
                        self.kvps[k]['out_link'][out_k] = self.kvps[out_k]['pr'] + out_value
                    except:
                        # 跳转节点不做为起始page点, 则随机跳转至其他点
                        continue
                    # self.kvps[k]['out_link'] = dict(zip(out_link, map(lambda x: self.kvps[x]['pr']+out_value, out_link)))                
                    
                    # update begin page value
                    self.kvps[out_k]['pr'] = self.kvps[k]['out_link'][out_k]
                
            for k in self.kvps:
                self.kvps[k]['pr'] += (1-beta) * (1/self.node_size)


    def save_result(self, top=10, save_to='./result.txt'):
        if os.path.exists(save_to):
            os.remove(save_to)

        result = sorted(self.kvps.items(), key=lambda x : x[1]['pr'])[:10]

        for i in result:
            if not os.path.exists(save_to):
                with open(save_to, 'w', newline='\n',encoding='utf-8') as f:
                    f.write(str(i[0])+'\r\n')
            else:
                with open(save_to, 'a', newline='\n', encoding='utf-8') as f:
                    f.write(str(i[0])+'\r\n')

                # print("*"*10)
                # print(rnum)
                # print(self.kvps)
        # print(self.kvps)

    @staticmethod
    def load_data(fp):
        kvps = {}
        # 收集所有节点
        total = set()
        with open(fp, 'r',newline='\n', encoding='utf-8') as f:
            for i in f.readlines()[1:]:
                begin, end = map(int, i.split('\t'))
                if kvps.get(begin) == None:
                    kvps[begin] = {}
                    kvps[begin]['pr'] = 0
                    kvps[begin]['out_link'] = {}
                    kvps[begin]['out_link'][end] = 0
                    total.add(begin)
                    total.add(end)
                else:
                    kvps[begin]['out_link'][end] = 0
                    total.add(begin)
                    total.add(end)
        # print(kvp)
        pr = 1 / len(kvps.keys())
        node_size = len(total)
        # print(kvps)
        return kvps, pr, node_size
            

if __name__ == "__main__":
    fp = './web-Google.txt'
    smaple_fp = './sample_test.txt'
    kvps, pr, node_size = PageRank.load_data(smaple_fp)
    page_rank = PageRank(kvps, pr, node_size)
    page_rank.initialize()
    page_rank.compute()
    page_rank.save_result(top=4, save_to='./result_scc.txt')