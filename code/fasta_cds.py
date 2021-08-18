
import sys
import numpy as np
import pandas as pd
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
gff = pd.read_csv(sys.argv[1],sep='\t',header=None, skiprows=0)
gff = gff[gff[2]=='CDS']
gff[8] = gff[8].str.split(':|=|;|-',expand=True)[2]
print(gff.head())
# exit(0)
dic = SeqIO.to_dict(SeqIO.parse(sys.argv[2],'fasta'))
records = []
for group,data in gff.groupby([0,8]):
    # data = data.sort_values(by=3,ascending=True,inplace=True)
    # print(data)
    start = data[3].astype('int').tolist()
    end = data[4].astype('int').tolist()
    strand = data[6].tolist()
    seq = ''
    for i,num in enumerate(start):
        if strand[i] == '-':
            seq+=dic[''+group[0]].seq[start[i]-1:end[i]].reverse_complement()
        else:
            seq+=dic[''+group[0]].seq[start[i]-1:end[i]]
    record = SeqRecord(seq,id=group[1],description='')
    records.append(record)
SeqIO.write(records, sys.argv[3], 'fasta')
