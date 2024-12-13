import sys
import re
import pandas as pd
from Bio import SeqIO
# python deal_gff.py gff cds pep mark

def read_gff(file):
    data=[]
    with open(file) as f:
        for line in f.readlines():
            if re.match(r"^#", line):
                continue
            arr = line.strip().split('\t')
            if len(arr)<9:
                continue
            data.append(arr)
    return data

def extract_chromosome(s):  
    match = re.search(r'chromosome=(\d+)', s)  
    return match.group(1) if match else None

data = read_gff(sys.argv[1])
gff = pd.DataFrame(data)
chr_df = gff[gff[2] == 'region']
chr_df[8] = chr_df.loc[:,8].apply(extract_chromosome)
chr_dict = chr_df[pd.notnull(chr_df[8])].set_index(0)[8].to_dict()
gff[0] = gff[0].map(lambda x: chr_dict.get(x, x)) 

gff = gff[gff[2] == 'CDS']
gff = gff.loc[:, [0, 8, 3, 4, 6]]
gff[8] = gff[8].str.split('=|;|-',expand=True)[2]
gff = gff.groupby(8).agg({0:'first',8:'first', 3: 'min',  4: 'max',6:'first' })  

gff.columns = [0,1,2,3,4]
gff[2] =gff[2].astype(int)
gff[3] =gff[3].astype(int)
for name, group in gff.groupby(0):
    if len(group) == 1:
        continue
    start=0
    group = group.sort_values(by=[2,3],ascending=[True,False])
    for index, row in group.iterrows():
        if row[3]>start and row[2]>start:
            start=min([row[3],row[2]])
            continue
        gff.drop(index=index, inplace=True)

gff['order'] = ''
gff['newname'] = ''
for name, group in gff.groupby([0]):
    number = len(group)
    group = group.sort_values(by=[2])
    gff.loc[group.index, 'order'] = list(range(1, len(group)+1))
    gff.loc[group.index, 'newname'] = list(
        [str(sys.argv[4])+str(name)+'g'+str(i).zfill(5) for i in range(1, len(group)+1)])
gff['order'] = gff['order'].astype('int')
gff = gff[[0, 'newname', 2, 3, 4, 'order', 1]]
gff = gff.sort_values(by=[0, 'order'])
gff.to_csv(str(sys.argv[4])+'.gff', sep="\t", index=False, header=None)
lens = gff.groupby(0).max()[[3, 'order']]
lens.to_csv(str(sys.argv[4])+'.lens', sep="\t", header=None)


id_dict = gff.set_index([1])['newname'].to_dict()
#cds
seqs = []
n = 0
for seq_record in SeqIO.parse(sys.argv[2], "fasta"):
    seq_record.id =  re.search(r'XP_\d+\.\d+', seq_record.id).group()  
    if seq_record.id in id_dict:
        seq_record.id = id_dict[seq_record.id]
        seq_record.seq = seq_record.id.seq.replace('.', '*')
        n += 1
    else:
        continue
    seqs.append(seq_record)
SeqIO.write(seqs, str(sys.argv[4])+'.cds.fa', "fasta")
print('cds: '+str(n))

#pep
seqs = []
n = 0
for seq_record in SeqIO.parse(sys.argv[3], "fasta"):
    if seq_record.id in id_dict:
        seq_record.id = id_dict[seq_record.id]
        seq_record.seq = seq_record.id.seq.replace('.', '*')
        n += 1
    else:
        continue
    seqs.append(seq_record)
SeqIO.write(seqs, str(sys.argv[4])+'.pep.fa', "fasta")
print('pep: '+str(n))