# coding=utf-8
import os


class PageRank:

    def __init__(self, kvps, pr, node_size):
        self.kvps = kvps
        self.pr = pr
        self.node_size = node_size
        self.dead_end = {}  


    def initialize(self):
        for k in self.kvps:
            col = self.kvps[k]['out_link']
            self.kvps[k]['pr'] = self.pr
            self.kvps[k]['out_link'] = dict(zip( col, map(lambda x: self.pr, col.values())))
        print('load completed')


    def compute(self, num=1, beta=0.8):

        for i in range(num):
            # set and initialize middle stack to save computing values
            # middle stack only savae the page in scc, so it do not save dead-end
            middle_stack = {k:0 for k in self.kvps.keys()}
            # for example
            # A
            for k in iter(self.kvps.keys()):
                # pr_A = 1/4
                pr = self.kvps[k]['pr']
                # the out_link of A => [B, C, D]
                out_link = self.kvps[k]['out_link']
                #  sparse matrix multiply (reduce 0 part)
                # taxation
                # 0.8 * 1/4 * 1/3   beta * M * v
                out_value = pr * 1/len(out_link) * beta
                # print(k, 'weight:', 1/len(out_link))
                ## update out_link value
                # B C D
                for out_k in iter(out_link):
                    try:
                        # B: 0+1/4*1/3
                        # C: 0+1/4*1/3
                        # D: 0+1/4*1/3
                        # where 0 is initial value of middle stack
                        middle_stack[out_k] += out_value

                        # if meet with dead-end point, computing dead-end PR value
                        if out_k in self.dead_end:
                            self.dead_end[out_k] += out_value
                    except:
                        # if you find dead-end in the out_links of current page 
                        # but the dead-end can not be found in middle stack, 
                        # you will turn to here, so we create a k-v pair from dead-end
                        # the key is name of dead-end, and value is the out_link value 
                        # to this dead-end from the current page
                        print('this page "'+str(out_k)+'" is dead-end')
                        self.dead_end[out_k] = out_value
                        continue
            ### update begin page PR from middle_stack and dead-end PR
            # beat*M*v + (1-beta)*e/n
            r_val  = (1 - beta) * 1/self.node_size  
            for k in iter(self.kvps.keys()):
                middle_stack[k] += r_val
                self.kvps[k]['pr'] = middle_stack[k]
            
            for k in iter(self.dead_end):
                self.dead_end[k] += r_val
            print('epoch',i)


    def save_result(self, top=10, save_to='./result.txt'):
        if os.path.exists(save_to):
            os.remove(save_to)

        result = {k:v['pr'] for k, v in self.kvps.items()}
        result.update(self.dead_end)
        # print('dead-end', self.dead_end)
        result = sorted(result.items(), key=lambda x: x[1], reverse=True)
        # print('good', result)
        for page, pr in result[:top]:
            if not os.path.exists(save_to):
                with open(save_to, 'w', newline='\n',encoding='utf-8') as f:
                    f.write(str(page)+':'+str(pr)+'\r\n')
            else:
                with open(save_to, 'a', newline='\n', encoding='utf-8') as f:
                    f.write(str(page)+':'+str(pr)+'\r\n')

    @staticmethod
    def load_data(fp, start=4):
        kvps = {}
        # collect all page(includ dead-end)
        total = set()
        with open(fp, 'r',newline='\n', encoding='utf-8') as f:
            for i in f.readlines()[start:]:
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
        pr = 1 / len(kvps.keys())
        node_size = len(total)
        return kvps, pr, node_size
            

if __name__ == "__main__":
    fp = ['./web-Google.txt', './result_top10.txt'] # start from line 4
    smaple_fp_scc = ['./sample_test.txt', './result_scc.txt'] # start from line 1
    smaple_fp_dn = ['./sample_test2.txt', './result_dn.txt'] # start from line 1
    kvps, pr, node_size= PageRank.load_data(fp[0], start=4)
    page_rank = PageRank(kvps, pr, node_size)
    page_rank.initialize()
    page_rank.compute(num=10)
    page_rank.save_result(top=10, save_to=fp[1])