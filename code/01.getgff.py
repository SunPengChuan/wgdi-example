import sys

import pandas as pd

data = pd.read_csv(sys.argv[1], sep="\t", header=None,skiprows=3)
data = data[data[2] == 'mRNA']
data = data.loc[:, [0, 8, 3, 4, 6]]
data[8] = data[8].str.split(':|=|;|\-',expand=True)[3]
# data.drop_duplicates(subset=[8], keep='first', inplace=True)
data[0] = data[0].str.replace('LG0?','')
data.to_csv(sys.argv[2], sep="\t", header=None, index=False)
