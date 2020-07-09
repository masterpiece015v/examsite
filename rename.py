import os


if __name__ == "__main__":
    cur_dir = os.getcwd()
    base_dir = os.path.join(cur_dir, 'exam', 'static', 'exam', 'pdf', 'question_pm')

    list_dir = os.listdir(base_dir)
    datas = []
    for fn in list_dir:
        fns = fn.split("_")
        if fns[1][3:]=='h':
            in_fn = os.path.join( base_dir , fn )
            out_fn = os.path.join( base_dir, fns[0] + "_" + fns[1][0:3]+'01' + "_" + fns[2] + "_" + fns[3] )
            os.rename( in_fn , out_fn )
        else:
            in_fn = os.path.join( base_dir , fn )
            out_fn = os.path.join( base_dir, fns[0] + "_" + fns[1][0:3]+'02' + "_" + fns[2] + "_" + fns[3] )
            os.rename( in_fn , out_fn )
