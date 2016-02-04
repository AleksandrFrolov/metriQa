import os
import csv

def qikprop_parser(csv_file):
    if not os.path.isfile(csv_file):
        raise IOError
    res = []
    data = csv.reader(open(csv_file, 'r'))
    header = data.next()[1:]
    for line in data:
        mol_name = line[0]
        mol_data = dict(zip(header, line[1:]))
        res.append((mol_name, mol_data))
    return dict(res)