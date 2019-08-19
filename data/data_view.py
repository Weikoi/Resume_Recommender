import pickle as pk
from util.tools import pretty_dict

data = pk.load(file=open('./sample_1000.bin', 'rb'))

for i in data[:2]:
    print(pretty_dict(i))