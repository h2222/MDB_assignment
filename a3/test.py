



a = {'a':1, 'b':2, 'c':3}


sa = dict(sorted(a.items(), key=lambda x: x[1], reverse=True))




print(sa)