import matplotlib.pyplot as plt
# from upsetplot import generate_counts, plot

from upsetplot import from_contents, UpSet

import pandas as pd
import sys


alignment = pd.read_csv(sys.argv[1],sep=',',header=None,index_col=0)
alignment = alignment.dropna()
# print(alignment[alignment[1]!=alignment[2]])
# print(alignment[alignment[1]!=alignment[3]])
# print(alignment[alignment[3]!=alignment[2]])
# exit(0) 
data=[]
for col in alignment.columns:
    df = alignment[col].reset_index()
    df = df[df[col].str.contains('ptr',na=False)]
    # print(df)
    df['id'] = df[0]+df[col]
    print(df)
    data.append(set(df['id'].values))


# plt.figure()
# print(data)
labels = ['repeat_number=5','repeat_number=10','repeat_number=20']
data = from_contents(dict(zip(labels,data)))
UpSet(data, subset_size='count',show_counts=True).plot()
# print(data)
# venn3(
#     subsets = data,
#     set_labels=('grading=50,50,50','rading=50,40,50','rading=50,25,10'),
#     set_colors=('orange','green','red')
# )
plt.savefig('upsetplot_reapeat.svg')
plt.show()