# 同じ問題を見つける

import MySQLdb

conn = MySQLdb.connect(
    user='webmaster',
    passwd='P@ssword',
    host='kyouin-02',
    db='examsitedb',
    charset='utf8'
)

cur = conn.cursor()
cur2 = conn.cursor()
sql = "select q_id,c_id,q_num,q_content " \
    "from exam_question " \
    "where q_content is not null"

cur.execute( sql )

rows = cur.fetchall()
datas = []
for row in rows:
    if int(row[2]) < 10:
        content = row[3][2:len( row[3] )]
    else:
        content = row[3][3:len( row[3] )]

    sql2 = "select q_id,c_id,q_num,q_content " \
            "from exam_question " \
            "where c_id='" + row[1] + "' " \
            "and q_id <> '" + row[0] + "' " \
            "and q_content is not null"
    cur2.execute( sql2 )
    rows2 = cur2.fetchall()

    for row2 in rows2:
        if not row2[3] is None:
            if int(row2[2]) < 10:
                content2 = row2[3][2:len(row2[3])]
            else:
                content2 = row2[3][3:len(row2[3])]

        i = 0
        cnt = 0
        while i < len( content )-1 and i < len( content2 ) - 1:
            if content[i] == content2[i]:
                cnt = cnt + 1
            i = i + 1

        w9 = len( content ) * 0.2
        if cnt >= w9:
            # insert
            data = (row[0]+row2[0] , row[0] , row2[0])
            print( "%s,%s"%(row[0],content) )
            print( "%s,%s"%(row2[0],content2) )
            datas.append( data )

for i,d1 in enumerate(datas):
    id1 = d1[1]
    id2 = d1[2]
    j = i + 1
    if j < len(datas):
        #print( "%s,%s"%(j,len(datas)) )
        for j in range( i+1 , len( datas) ):

            if j < len( datas ):
                id3 = datas[j][1]
                id4 = datas[j][2]

                if id1 == id4:
                    #print( datas[j] )
                    datas.pop( j )
#print( len( datas ))
sql3 = "insert into exam_compquestion values ( %s , %s , %s )"
c = conn.cursor()
c.executemany(sql3, datas)
c.close()
conn.commit()
conn.close()