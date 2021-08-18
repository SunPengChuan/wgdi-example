#!usr/bin/env python
# conding: utf-8
import sys

import pandas as pd

data = pd.read_csv(sys.argv[1], sep="\t", header=None)
# new = data[1].str.split('.').str
# data['id'] = new[0].values
# # data['id']  =data[1]
# data['cha'] = data[3]-data[2]
# print(data['id'])
# data['a'] = new[2].values
# # data['b'] = new[3].values
# print(data.head())
data[2] =data[2].astype(int)
data[3] =data[3].astype(int)
for name, group in data.groupby(0):
    if len(group) == 1:
        continue
    start=0
    # print(group.head())
    group = group.sort_values(by=[2,3],ascending=[True,False])
    for index, row in group.iterrows():
        # print(row)
        if row[3]>start and row[2]>start:
            start=max([row[3],row[2]])
            continue
        data.drop(index=index, inplace=True)
    # ind = group.sort_values(by='cha', ascending=False).index[1:].values
    #print(name)
    # print(group.sort_values(by='cha',ascending=False))

    

# data = data[data[1].str.contains('\.mRNA1$')]
data['order'] = ''
data['newname'] = ''
print(data.head())
for name, group in data.groupby([0]):
    number = len(group)
    group = group.sort_values(by=[2])
    data.loc[group.index, 'order'] = list(range(1, len(group)+1))
    data.loc[group.index, 'newname'] = list(
        ['aco48s'+str(name)+'g'+str(i).zfill(5) for i in range(1, len(group)+1)])
data['order'] = data['order'].astype('int')
data = data[[0, 'newname', 2, 3, 4, 'order', 1]]
print(data.head())
data = data.sort_values(by=[0, 'order'])
data.to_csv(sys.argv[2], sep="\t", index=False, header=None)
lens = data.groupby(0).max()[[3, 'order']]
lens.to_csv(sys.argv[3], sep="\t", header=None)
