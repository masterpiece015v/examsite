import cv2
import os
import numpy as np
from .tensor import Ainum
from django.conf import settings

#数字を中央に寄せる
def img_center( img ):
    #画像のサイズを取得
    r_max = len(img)
    c_max = len(img[0])
    r_top = r_max   #縦位置の始まり
    r_bottom = 0    #縦位置の終わり
    c_left = c_max  #横位置の始まり
    c_right = 0     #横位置の終わり

    #文字の縦位置、横位置を調べる
    for r in range( r_max ):
        for c in range( c_max ):
            if img[r][c] < 10:
                if r_top > r:
                    r_top = r

                if r_bottom < r:
                    r_bottom = r

                if c_left > c:
                    c_left = c

                if c_right < c:
                    c_right = c

    #横中央値
    c_mid = int( ( c_max/2 - ( c_right + c_left ) / 2) )
    #縦中央値
    r_mid = int( (r_max/2 - ( r_top + r_bottom) / 2))
    #print( 'r_max:%d r_top:%d r_bottom:%d r_mid:%d'%(r_max,r_top,r_bottom,r_mid) )

    #横位置を調整する
    if c_mid > 0:#右にずらす
        for r in range( r_max ):
            c = c_max - 1
            while c > c_mid:
                img[r][c] = img[r][c - c_mid]
                c = c - 1
        for r in range( r_max ):
            c = c_mid
            while c > 0:
                img[r][c] = 255
                c = c - 1
    elif c_mid < 0:#左にずらす
        for r in range( r_max):
            c = 0
            while c < c_right + c_mid + 1:
                img[r][c] = img[r][c - c_mid]
                c = c + 1
        for r in range( r_max ):
            c = c_right + r_mid + 1
            while c < c_max:
                img[r][c] = 255
                c = c + 1

    #縦位置を調整する
    if r_mid > 0:#下にずらす
        for c in range( c_max ):
            r = r_max - 1
            while r > r_mid:
                img[r][c] = img[r - r_mid][c]
                r = r - 1
        for c in range( c_max ):
            r = r_mid
            while r > 0:
                img[r][c] = 255
                r = r -1
    elif r_mid < 0:#上にずらす
        for c in range( c_max ):
            r = 0
            while r < r_bottom + r_mid + 1:
                img[r][c] = img[r - r_mid][c]
                r = r + 1
        for c in range( c_max ):
            r = r_bottom + r_mid +1
            while r < r_max:
                img[r][c] = 255
                r = r + 1
    #ファイルに吐き出す
    #cv2.imwrite('img.jpg',img)
    return img

#画像を表示する
def imgshow(img):
    cv2.namedWindow("window", cv2.WINDOW_NORMAL)
    cv2.imshow('window', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#２値画像に変換する
def bwchange(img):
    img_temp = cv2.GaussianBlur(img, (5, 5), 0)
    res, img = cv2.threshold(img_temp, 50, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return res,img

# ５桁の数字を作る関数
def makenum(num):
    if num < 10:
        n = '0000' + str(num)
    elif num < 100:
        n = '000' + str(num)
    elif num < 1000:
        n = '00' + str(num)
    elif num < 10000:
        n = '0' + str(num)
    return n

def get_answer_list(filename):
    #マーカーの読み込み
    path = settings.BASE_DIR
    path = os.path.join( path , "exam" , "marker.png" )
    marker = cv2.imread(path, 0)
    #print( filename )
    #画像ファイルの読み込みとサイズ調整
    img = cv2.imread(filename, 0)
    #w, h = img.shape[::-1]
    #print("%d,%d"%(w,h))
    img = cv2.resize(img, (2100, 2964))
    #img = cv2.resize(img, (1000, 1500))
    # markeと同じ画像の位置を取得する
    res_gaku = cv2.matchTemplate(img, marker, cv2.TM_CCOEFF_NORMED)
    threshold = 0.6
    loc = np.where(res_gaku >= threshold)
    x = min(loc[1])
    y = min(loc[0])
    mark_area = { 'x' : x , 'y' : y }
    mark_list =[]
    mark_list.append( mark_area )
    for pt in zip(*loc[::-1]):
        nx = pt[0]
        ny = pt[1]
        if y + 80 < ny:
            mark_area = {}
            mark_area['x'] = nx
            mark_area['y'] = ny
            mark_list.append( mark_area )
            y = ny

    #組織ID、テストID、ユーザIDを取得する
    img_info = img[mark_list[0]['y']-25: mark_list[0]['y']+140, mark_list[0]['x']+90: mark_list[0]['x']+1805]
    img_info = cv2.resize(img_info, (1400, 200))
    org_id = img_info[0:100, 348:695]
    test_id = img_info[0:100, 1050:1400]
    user_id = img_info[104:200, 348:695]
    org_id = cv2.resize(org_id,(400,100))
    test_id = cv2.resize(test_id,(400,100))
    user_id = cv2.resize(user_id,(400,100))

    #白黒チェンジ
    res , org_id = bwchange( org_id )
    ainum = Ainum()

    o_n = ""
    for c in range(4):
        o_num = org_id[5:90 , (c*40)+10:(c*40)+50]
        o_num = cv2.resize(o_num,(28,28))
        o_n = o_n + str( ainum.get_num( o_num ) )
    res,test_id = bwchange( test_id )

    t_n = ""
    for c in range(4):
        test_num = test_id[5:90 ,(c*40)+10:(c*40)+50]
        test_num = cv2.resize(test_num,(28,28))
        t_n = t_n + str( ainum.get_num(test_num) )
    res,user_id = bwchange( user_id )

    u_n = ""
    for c in range(8):
        user_num = user_id[5:90 , (c*40)+10:(c*40)+50 ]
        user_num = cv2.resize( user_num , (28,28) )
        u_n = u_n + str( ainum.get_num(user_num) )

    # 列数
    n_col = 20
    #結果を入れる配列
    result = [[],[],[],[]]
    # マークシート
    # 全ての行が終わるまで
    for r in range(len( mark_list) ):
        if r >= 3:
            img_ans = img[ mark_list[r]['y']-15:mark_list[r]['y']+55 , mark_list[r]['x']+85: 1950]
            # リサイズ
            img_ans = cv2.resize(img_ans, (n_col * 30, 30))
            # 黒白に変換
            res_gaku, img_ans = bwchange(img_ans)
            img_ans = 255 - img_ans

            #1～20の答え
            area_sum1 = []
            for col in range(1,5):
                tmp_img = img_ans[5:90 , col * 30 : col * 30 + 30 ]
                val = np.sum(tmp_img)
                if val > 35000:
                    area_sum1.append(val)
                else:
                    area_sum1.append(0)
            result[0].append( area_sum1 > np.median(area_sum1) * 3)

            area_sum2 = []
            for col in range(6,10):
                tmp_img = img_ans[5:90, col * 30: col * 30 + 30 ]
                val = np.sum(tmp_img)
                if val > 35000:
                    area_sum2.append(val)
                else:
                    area_sum2.append(0)

            result[1].append( area_sum2 > np.median(area_sum2) * 3 )

            area_sum3 = []
            for col in range(11,15):
                tmp_img = img_ans[5:90, col * 30: col * 30 + 30 ]
                val = np.sum(tmp_img)
                if val > 35000:
                    area_sum3.append(val)
                else:
                    area_sum3.append(0)
            result[2].append( area_sum3 > np.median(area_sum3) * 3 )

            area_sum4 = []
            for col in range(16,20):
                tmp_img = img_ans[5:90, col * 30: col * 30 +30 ]
                val = np.sum(tmp_img)
                if val > 35000:
                    area_sum4.append(val)
                else:
                    area_sum4.append(0)
            result[3].append( area_sum4 > np.median(area_sum4) * 3 )

    answer = ['ア', 'イ', 'ウ', 'エ']
    answerlist = []
    # y=1→1～30 y=2→31～60 y=3→61～90
    for y in range(4):
        for x in range(len(result[y])):
            res = np.where(result[y][x] == True)[0]
            q = []
            if len(res) > 1:
                q.append(y * 20 + x + 1)
                q.append('複数回答')
            elif len(res) == 1:
                q.append(y * 20 + x + 1)
                q.append(answer[res[0]])

            else:
                q.append(y * 20 + x + 1)
                q.append('未回答')
            answerlist.append(q)

    return o_n,t_n,u_n, answerlist

if __name__ == "__main__":
    files = os.listdir('media/exam/0002/')
    #print(files)
    for file in files:
        org_id,test_id,user_id , answerlist = get_answer_list('media/exam/0002/%s' % file)
        print("org_id:%s"%org_id)
        print("test_id:%s"%test_id)
        print("user_id:%s"%user_id)
        for list in answerlist:
            print( list )


