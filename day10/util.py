import os

def load_int_lines_list(fname):
    folder = os.path.dirname(os.path.realpath(__file__))
    fname = os.path.join(folder, fname)
    data = []
    with open(fname, 'rt') as f:
        # return [int(line.rstrip('\n')) for line in f.readlines()]
        for line in f.readlines():
            x = line.rstrip('\n')
            if len(x):
                data.append(int(x))

    return data


def load_str_lines_list(fname):
    folder = os.path.dirname(os.path.realpath(__file__))
    fname = os.path.join(folder, fname)
    data = []
    with open(fname, 'rt') as f:
        # return [int(line.rstrip('\n')) for line in f.readlines()]
        for line in f.readlines():
            x = line.rstrip('\n')
            if len(x):
                data.append(x)

    return data

def load_int_list(fname):
    folder = os.path.dirname(os.path.realpath(__file__))
    fname = os.path.join(folder, fname)
    with open(fname, 'rt') as f:
        line = f.readline().rstrip('\n')
        return [int(item) for item in line.split(',')]

def load_number_string_list(fname):
    folder = os.path.dirname(os.path.realpath(__file__))
    fname = os.path.join(folder, fname)
    with open(fname, 'rt') as f:
        line = f.readline().rstrip('\n')
        return [int(item) for item in line]

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

