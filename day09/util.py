def load_int_lines(fname):
    data = []
    with open(fname, 'rt') as f:
        for line in f.readlines():
            x = line.rstrip('\n')
            if len(x):
                data.append(int(x))
    
    return data

def load_int_line(fname):
    data = []
    with open(fname, 'rt') as f:
        str = f.readline().rstrip('\n')
        for c in str:
            data.append(int(c))
    return data

def chunks(lst, n):
    for pos in range(0, len(lst), n):
        yield lst[pos : pos+n]

class GrowingList(list):
    def __setitem__(self, index, value):
        if index >= len(self):
            self.extend([0]*(index + 1 - len(self)))
        list.__setitem__(self, index, value)
    
    def __getitem__(self, index):
        if index < len(self):
            return list.__getitem__(self, index)
        else:
            return 0

