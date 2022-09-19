import sys
import pandas as pd
import matplotlib.pyplot as plt

# python local.py blast_matrix.csv hsa17s12.gff ptr16s13.gff wgdi.hsa17s_ptr16s.alignment.csv wgdi.12-13.svg

matrix = pd.read_csv(sys.argv[1])
gff1 = pd.read_csv(sys.argv[2],sep='\t',index_col=1)
gff2 = pd.read_csv(sys.argv[3],sep='\t',index_col=1)

df = matrix[(matrix['0'].isin(gff1.index.tolist())) & (matrix['1'].isin(gff2.index.tolist()))]
# print(df)

# plot dotplot 
fig, ax = plt.subplots(figsize=(8,8))
markersize = 8
ax.scatter(df['loc2'], df['loc1'], s=float(markersize), c=df['color'],
                   alpha=1, edgecolors=None, linewidths=0, marker='o')

# plot line of alignment
alignment = pd.read_csv(sys.argv[4],header=None)
alignment['pair'] = alignment[0]+alignment[1]

alignment_matrix = df[(df['0']+df['1']).isin(alignment['pair'])]
alignment_matrix = alignment_matrix.sort_values(by='loc1')
ax.plot(alignment_matrix['loc2'],alignment_matrix['loc1'],color='pink',alpha=0.5,linewidth=2)
markersize = 50
ax.scatter(alignment_matrix['loc2'], alignment_matrix['loc1'], s=float(markersize), c=alignment_matrix['color'],
                   alpha=1, edgecolors=None, linewidths=0, marker='o')
# wgdi : orange 
# MCScanX : green
# JCVI : pink

print(len(alignment_matrix))
plt.gca().invert_yaxis()
ax.set_xticks([])
ax.set_yticks([])
plt.savefig(sys.argv[5], dpi=300)
plt.show()