
import os
import sys
# s1.pep s2.pep s2 s1_s2.blast
index, target, db1, out = sys.argv[1:]
print(index, target, db1, out)
db = str(db1)+'dia_db'
if not os.path.exists(db1):
    command = ' '.join(['diamond', 'makedb', '--in', target, '-d', db])
    os.system(command)
if not os.path.exists(out):
    command = ' '.join(['diamond', 'blastp', '-d', db, '-q', index, '-o', out])
    os.system(command)
