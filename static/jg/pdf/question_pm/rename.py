import os

for file in os.listdir():
    print( file )
    list = file.split("_")
    if list[3] == "ans":
        #os.rename( file , "%s_%s_%s_ans.pdf"%(list[0],list[1],list[2][0:2]))
        print( "%s_ans"%file )
    else:
        #os.rename( file, "%s_%s_%s.pdf"%(list[0],list[1],list[2][0:2] ))
        print( file )
