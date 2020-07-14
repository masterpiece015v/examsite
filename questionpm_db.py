# static/exam/pdf/question_pmに
# fe_h2101_01セキュリティ_パケットフィルタリング.pdf
# の形式で保存しておけばデータベースに登録される

import MySQLdb,os

if __name__ == "__main__":

    conn = MySQLdb.connect(
        user='webmaster',
        passwd='P@ssword',
        host='kyouin-02',
        db='examsitedb',
        charset='utf8'
    )

    cur_dir = os.getcwd()
    base_dir = os.path.join( cur_dir , 'exam' , 'static' , 'exam' , 'pdf' , 'question_pm')

    list_dir = os.listdir( base_dir )
    datas = []
    for fn in list_dir:
        fns = fn.split("_")
        if fns[3][0:len(fns[3])-4] != 'ans':
            data = ( fns[0]+fns[1]+fns[2][0:2] , fns[0],fns[1],int(fns[2][0:2]),fns[2],fns[3][0:len(fns[3])-4])
            datas.append( data )
    print( datas )
    sql = "insert into exam_questionpm values ( %s , %s , %s , %s , %s, %s)"
    c = conn.cursor()
    c.executemany(sql, datas)
    c.close()
    conn.commit()
    conn.close()