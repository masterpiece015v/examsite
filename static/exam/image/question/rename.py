import glob
import os

path = '*.png'

slist = glob.glob(path)

#print( slist )

for file in slist:
    if( len(file) == 14 ):
        dname = file[0:5] + file[6:14]
        os.rename(file,dname)