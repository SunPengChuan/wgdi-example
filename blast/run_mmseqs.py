import os
import re
import shutil
import sys

index, target, db1, db2, out = sys.argv[1:]
print(index, target, db1, db2, out)
db1 = str(db1)+'db'
db2 = str(db2)+'db'
if not os.path.exists(db1):
    command = ' '.join(['mmseqs', 'createdb', index, db1])
    os.system(command)
if not os.path.exists(db2):
    command = ' '.join(['mmseqs', 'createdb', target, db2])
    os.system(command)
tmp = db1+'_'+db2
result = db1+'_'+db2+'_result'
if os.path.exists(tmp):
    shutil.rmtree(tmp)
os.mkdir(tmp)
command1 = ' '.join(['mmseqs', 'createindex', db2, tmp])
command2 = ' '.join(['mmseqs', 'search', db1, db2, result, tmp, '-e', '1e-5'])
command3 = ' '.join(['mmseqs', 'convertalis', db1, db2, result, out])
os.system(command1)
os.system(command2)
os.system(command3)
files = [fname for fname in os.listdir('.') if re.match(result, fname)]
for f in files:
    os.remove(f)
shutil.rmtree(tmp)
