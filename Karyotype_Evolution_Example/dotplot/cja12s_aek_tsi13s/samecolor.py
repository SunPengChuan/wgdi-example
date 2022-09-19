from email.header import Header
import pandas as pd
import sys

df = pd.read_csv(sys.argv[1])
print(df)
df = df[df['class1_color']==df['class2_color']]
print(df)
df.to_csv(sys.argv[2],index=False,header=True)