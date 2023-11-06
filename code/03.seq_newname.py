import sys

import pandas as pd
from Bio import SeqIO

data = pd.read_csv(sys.argv[1], sep="\t", header=None, index_col=6)
id_dict = data[1].to_dict()
print(data.head())
seqs = []
n = 0
for seq_record in SeqIO.parse(sys.argv[2], "fasta"):
	if seq_record.id in id_dict:
		seq_record.id = id_dict[seq_record.id]
		n += 1
	else:
		continue
	seqs.append(seq_record)
SeqIO.write(seqs, sys.argv[3], "fasta")
print(n)
