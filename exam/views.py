from io import TextIOWrapper
from django.shortcuts import render,HttpResponseRedirect
from django.http import HttpResponse
from django.core.mail import EmailMessage
import re,string,random,datetime,os,csv
from .models import Auth,User,Org,AccessLog,Classify,Question,LittleTest,SuperUser,AddLicenseRequest,AnswerImage,ResultTest,MakeLittletest,CompQuestion,QuestionPm
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.urls import reverse
from django.utils import timezone
from .forms import AnswerImageForm
from .markreader import get_answer_list
import json,ast
from django.conf import settings
import glob
from .logger import log_write

#関数
#アクセスログに追加する
def addAccessLog(request,a_page,a_state):
    u_id = request.POST["u_id"]
    ipa = request.environ['REMOTE_ADDR']
    alog = AccessLog(u_id=u_id, a_date=datetime.datetime.now(), a_ipa=ipa, a_page=a_page, a_state=a_state)
    alog.save()

#ランダムな文字を作る関数
def randomCharacter(n):
    c = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join([random.choice(c) for i in range(n)])

#000Xのコードを作成する
def code4( c ):
    if type( c ) is int:
        if c < 10:
            return '000' + str( c )
        elif c < 100:
            return '00' + str( c )
        elif c < 1000:
            return '0' + str( c )
        else:
            return str( c )
    else:
        if len(c) == 1:
            return '000' + c
        elif len(c) == 2:
            return '00' + c
        elif len(c) == 3:
            return '0' + c
        else:
            return c

#認証システム（キーの追加）
def auth_add(auth_kind,auth_value):
    auth_key = randomCharacter(40)
    auth_date = datetime.datetime.now()
    auth = Auth(auth_key,auth_kind,auth_value,auth_date)
    auth.save()
    return auth_key

#ブルートフォースをチェックする
def checkBruteforce(u_id,a_page):
    delta = datetime.datetime.now() - datetime.timedelta(minutes=10)
    alogs = AccessLog.objects.filter(u_id=u_id,a_page=a_page,a_date__gt=delta)
    if alogs.count() >= 100:
        #攻撃されている
        return True
    else:
        #攻撃されていない
        return False

#ajaxのPOSTデータをDictionaryに変換する
def byteToDic( data ):
    return  ast.literal_eval( data.decode() )

#セッションにu_idを含むかをチェックする
def securecheck( request ):
    if 'u_id' not in request.session:
        return render( request,'exam/errorpage.html',{'message','不正なアクセスです。'})

#HttpResponseのJSON
def HttpResponseJson( jsonobj ):
    jsonStr = json.dumps( jsonobj , ensure_ascii=False, indent=2)
    return HttpResponse(jsonStr, content_type='application/json', charset='utf-8')

#-*-*-*-*-*-ページ-*-*-*-*-*-*-*-*-*
#ログイン
def index( request):
    request.session.clear()
    return render(request, 'exam/index.html')

#新規ユーザ登録
def newuser( request ):
    if request.method != "POST":
        return render(request,'exam/newuser.html')

    u_email = request.POST['u_email']
    # メールアドレスチェック
    try:
        user = User.objects.get(u_email=u_email)
    except ObjectDoesNotExist:
        #存在しないので登録できる
        auth_key = auth_add('newuser', u_email)

        sub = '新規ユーザ登録'
        con = """
        新規ユーザ登録をしていただきありがとうございました。
        24時間以内に、下記URLから本登録にお進みください。
        http://examsite.room.kaikei.ac.jp:8000/exam/orgregister/?auth_key=%s
        """ % (auth_key)
        EmailMessage(sub, con, to=[u_email, ]).send()
        return render(request, 'exam/message.html', {'message': 'メールアドレス宛に登録サイトのURLを送信しました。'})

    #メールアドレスが存在したので登録できない
    return render( request,'exam/newuser.html',{'message':'そのメールアドレスはすでに登録されています。'})

#アカウント登録
def orgregister( request ):
    #入力フォームを取得するリクエスト
    if request.method != "POST":
        auth_key = request.GET['auth_key']
        try:
            Auth.objects.get(pk=auth_key)
            return render( request,'exam/orgregister.html',{'auth_key':auth_key})
        except:
            return render( request,'exam/message.html',{'message':'不正なアクセス'})

    #登録用のリクエスト
    auth_key = request.POST['auth_key']
    u_email = request.POST['u_email']
    try:
        auth = Auth.objects.get(pk=auth_key)
    except ObjectDoesNotExist:
        return render(request, 'exam/newuser.html', {'message': '有効期限が切れました'})

    #時間チェック
    if auth.auth_date_check() != True:
        auth.delete()
        return render( request,'exam/orgregister.html',{'auth_key':auth_key,'message':'有効期限が切れました'})
    #メールアドレスチェック
    if auth.auth_value != u_email:
        return render( request,'exam/orgregister.html',{'auth_key':auth_key,'message':'メールアドレスが違います。'})

    u_id = request.POST['u_id']
    u_pass = request.POST['u_pass']
    o_name = request.POST['o_name']
    u_name = request.POST['u_name']
    o_count = len( Org.objects.all() ) + 1

    if o_count < 10:
        o_id = '000'+str(o_count)
    elif o_count < 100:
        o_id = '00'+str(o_count)
    elif o_count < 1000:
        o_id = '0'+str(o_count)
    else:
        o_id = str(o_count)

    org = Org(o_id=o_id,o_name=o_name,l_num=1)
    org.save()

    org = Org.objects.get(o_id=o_id)
    #メディアディレクトリを作成する
    media_dir = os.path.join( settings.STATIC_ROOT ,"exam","answer",o_id)
    #media_dir = "static/exam/answer/" + o_id

    os.mkdir( media_dir )

    try:
        org.user_set.create(u_id=u_id,u_pass=u_pass,u_name=u_name,u_email=u_email,u_admin=1,u_enable=1,u_hidden=0,u_date=datetime.datetime.now())
    except IntegrityError:
        return render( request,'exam/orgregister.html',{'auth_key':auth_key,'message':'そのユーザIDはすでに存在しています。'})
    #不要な認証キーの削除
    auth.delete()
    return HttpResponseRedirect('/exam/')

#メインページ
def mainpage( request ):
    #セッションIDがある(戻るボタンなどで帰ってきたとき用)
    if 'u_id' in request.session:
        if request.session['u_id'] != "":
            u_id = request.session['u_id']
            try:
                user = User.objects.get(pk=u_id)
            except:
                return render(request,'exam/errorpage.html',{'message':'不正なアクセスです。'})
            #request.session['u_id'] = u_id
            u_name = user.u_name
            u_admin = user.u_admin
            request.session['u_admin'] = u_admin
            period = Question.objects.values_list('q_period').distinct()
            periodlist = []
            for p in period:
                periodlist.append(p[0])

            classify = Classify.objects.values_list('m_id','m_name').distinct()
            print( classify )
            classifylist = []
            for c in classify:
                dict = {}
                dict['m_id'] = c[0]
                dict['m_name'] = c[1]
                classifylist.append( dict )

            return render( request,'exam/mainpage.html',{'u_id':u_id,'u_name':u_name,'u_admin':u_admin,'period':periodlist,'classify':classifylist})

    #u_idやパスワードを持っていない
    if request.method != "POST":
        return render( request,'exam/errorpage.html',{'message':'不正なアクセスです。'})

    u_id = request.POST["u_id"]
    u_pass = request.POST["u_pass"]
    ipa = request.environ['REMOTE_ADDR']    #IP-Address

    #アカウントが有効かをチェック
    try:
        print( u_id )
        user = User.objects.get(pk=u_id)
    except:
        return render( request , 'exam/errorpage.html',{'message':'不正なアクセスです。'})

    if user.u_enable==False:
        return render(request,'exam/errorpage.html',{'message':'アカウントが有効ではありません。管理者に問い合わせてください。'})

    #ブルートフォース対策10分間に100回以上のログイン失敗
    if checkBruteforce(u_id,'mainpage'):
        user.u_enable = 0
        user.save()
        con = """
        不正なアクセスを検知したので、アカウントをロックしました。
        解除申請をしてください。
        """
        EmailMessage('アカウントロック',con, to=[user.u_email, ]).send()
        return render(request,'exam/errorpage.html',{'message':'不正なログインを検知しました。アカウントをロックします。'})

    #u_idが存在するか
    try:
        user = User.objects.get(u_id=u_id)
    except ObjectDoesNotExist:
        #メールアドレスが存在するか
        try:
            user = User.objects.get(u_email=u_id)
        except ObjectDoesNotExist:
            #どちらも存在しない（ログイン失敗)
            addAccessLog(request,'mainpage','f')
            return render(request, 'exam/index.html', {'message': 'ユーザID（メールアドレス）、パスワードのいずれかが違います。'})

    if user.pass_check(u_pass=u_pass):
        addAccessLog(request,'mainpage','s')
        request.session['u_id'] = u_id
        u_name = user.u_name
        u_admin = user.u_admin
        request.session['o_id'] = user.o_id
        request.session['u_admin'] = u_admin
        period = Question.objects.values_list('q_period').distinct()
        periodlist = []
        for p in period:
            periodlist.append(p[0])

        classify = Classify.objects.values_list('m_id', 'm_name').distinct()
        print(classify)
        classifylist = []
        for c in classify:
            dict = {}
            dict['m_id'] = c[0]
            dict['m_name'] = c[1]
            classifylist.append(dict)
        return render(request, 'exam/mainpage.html',
                      {'u_id': u_id, 'u_name': u_name, 'u_admin': u_admin, 'period': periodlist,'classify': classifylist})
    else:
        addAccessLog(request,'mainpage','f')
        return render( request,'exam/index.html',{'message':'ユーザID（メールアドレス）、パスワードのいずれかが違います。'})

def passchange( request ):
    return render( request, 'exam/passchange.html')

def passchange_finish( request):
    u_id = request.session['u_id']
    old_pass = request.POST['old_pass']
    new_pass = request.POST['new_pass1']
    user = User.objects.get(pk=u_id)
    #print( user.u_pass )
    if old_pass == user.u_pass:
        #print('パスワード変更')
        user.u_pass = new_pass
        user.save()
        return render(request, 'exam/passchange_finish.html',{'message':'パスワードの変更ができました。'})
    else:
        #print('パスワードが違う')
        return render(request, 'exam/passchange.html',{'message':'パスワードが違うので変更できません。'})

#管理者問い合わせ
def inquiry( request ):
    #POSTでない
    if request.method!='POST':
        return render( request,'exam/inquiry.html')
    #POST送信
    if "lock_u_id" in request.POST :
        u_id = request.POST["lock_u_id"]
        u_pass = request.POST["lock_u_pass"]
        user = User.objects.get(pk=u_id)
        #ブルートフォース検出
        if checkBruteforce(u_id,'inquiry'):
            user.u_enable = 0
            user.save()
            con = """
            不正なアクセスを検知したので、アカウントをロックしました。
            解除申請をしてください。
            """
            EmailMessage('アカウントロック', con, to=[user.u_email, ]).send()
            return render(request,'exam/errorpage.html',{'message':'不正なログインを検知しました。アカウントをロックします。'})

        # パスワードが一致
        if user.u_pass == u_pass:
            user.u_enable = 1
            user.save()
            addAccessLog(request, 'inquiry', 's')
            return render( request,'exam/index.html')
        else:
            addAccessLog(request,'inquiry','f')
            return render(request,'exam/errorpage.html',{'message':'解除できません'})

    #パスワードのリセット
    if 'pass_u_id' in request.POST:
        u_id = request.POST['pass_u_id']
        u_email = request.POST['pass_u_email']
        try:
            user = User.objects.get(pk=u_id)
        except:
            return render( request,'exam/errorpage.html',{'message':'ユーザIDとメールアドレスが一致しません。'})

        if user.u_email == u_email:
            #except:
                #メールアドレスが存在しない
            #    return errorpage(request,'メールアドレスが存在しません。')

            #仮パスワードの設定
            damypass = randomCharacter(10)
            user.u_pass = damypass
            user.save()
            con = """
            仮のパスワードを設定しました。
            【仮パスワード】%s
           ログイン後変更してください。
            """%damypass
            EmailMessage('仮パスワードの設定',con,to=[u_email,]).send()
            content = "仮パスワードを設定しました。登録メールアドレスに仮パスワードを送りましたので、確認してください。"
            return render( request,'exam/message.html',{'message':content})

        return render( request,'exam/errorpage.html',{'message':'ユーザIDとメールアドレスが一致しません。'})

    if 'fgid_u_email' in request.POST:
        u_email = request.POST['fgid_u_email']

        try:
            user = User.objects.get(u_email=u_email)
        except:
            return render( request,'exam/errorpage.html',{'message':'登録されていないメールアドレスです。'})

        u_id = user.u_id

        con = """
        ユーザIDは
        %s
        です。
        """%u_id

        EmailMessage('ユーザID',con,to=[u_email,]).send()

        return render( request,'exam/message.html',{'message':'登録されているメールアドレスにユーザIDをお送りしました。'})

#ライセンスの購入
def addlicense( request ):
    #セッションにユーザIDの記録がない
    securecheck( request )

    o_id = request.session['o_id']
    org = Org.objects.get(o_id=o_id)
    o_name = org.o_name
    return render( request,'exam/addlicense.html',{'o_id':o_id,'o_name':o_name,'u_admin':request.session['u_admin']})

#ライセンスの購入
def addlicense_conf( request ):
    message = """
    購入処理をしております。
    終わりましたら、登録のメールアドレスにご連絡いたします。
    しばらくお待ちください。
    """
    o_id = request.POST['o_id']
    l_num = request.POST['l_num']

    adr = AddLicenseRequest(o_id=o_id,l_num=l_num,check=False,adr_date=datetime.datetime.now())
    adr.save()

    bodystr = "o_id:%s,l_num:%s"%(o_id,l_num)
    EmailMessage(subject="ライセンス購入のお知らせ",body=bodystr,to=['mstp015v@gmail.com',]).send()

    return render( request, 'exam/message.html',{'message':message})

#ログオフ
def logoff( request ):
    request.session['u_id'] = ""
    return render( request,'exam/index.html')

#問題作成メイン画面
def testmake( request ):
    #セッションを持っていない
    if 'u_id' not in request.session:
        return render( request,'exam/errorpage.html',{'message':'不正なアクセスです'})

    l_class_list = Classify.objects.values('l_id','l_name').distinct()
    q_test = Question.objects.values('q_test').distinct()

    return render(request,'exam/testmake.html',{'l_class_list':l_class_list , 'q_test':q_test,'u_admin':request.session['u_admin']})

#年度期ごとの問題を作成する画面
def testmakeperiod( request ):
    #セッションを持っていない
    if 'u_id' not in request.session:
        return render( request,'exam/errorpage.html',{'message':'不正なアクセスです'})

    q_test = Question.objects.values('q_test').distinct()
    q_period_list = Question.objects.filter(q_test='fe').values('q_period').distinct()
    return render(request,'exam/testmakeperiod.html',{'q_period_list':q_period_list , 'q_test':q_test,'u_admin':request.session['u_admin']})

#テスト印刷画面
def testprint( request ):
    securecheck( request )
    user = User.objects.get(pk=request.session['u_id'])
    o_id = user.o_id

    test = LittleTest.objects.filter(o_id=o_id).values('t_id','t_date').distinct()
    test_list = []
    for t in test:
        t_id = t['t_id']
        mt = MakeLittletest.objects.get(pk="%s%s"%(o_id,t_id))

        print( mt.u_id )

        test_list.append( {'t_id':t_id,'u_id':mt.u_id,'t_date':t['t_date']})
    return render( request,'exam/testprint.html',{'test_list':test_list,'u_admin':request.session['u_admin']})

#解答用紙印刷
def answersheetprint( request ):
    o_id = request.session['o_id']
    test = LittleTest.objects.filter(o_id=o_id).values('t_id','t_date').distinct()
    list = []
    for t in test:
        dic = {}
        dic['t_id'] = t['t_id']
        dic['t_date'] = t['t_date']
        list.append( dic )
    return render( request, 'exam/answersheetprint.html',{'test':list,'u_admin':request.session['u_admin']})

#解答用紙印刷
def answersheetprint_conf( request ):
    t_id = byteToDic( request.body )['t_id']
    o_id = request.session['o_id']

    test = LittleTest.objects.filter(o_id=o_id,t_id=t_id)
    user = User.objects.filter(o_id=o_id)

    t_list = []
    for t in test:
        dic = {}
        dic['t_num'] = t.t_num
        dic['q_id'] = t.q_id
        t_list.append( dic )

    u_list = []
    for u in user:
        dic = {}
        dic['u_id'] = u.u_id
        dic['u_name'] = u.u_name
        u_list.append( dic )

    list = {'t_list':t_list,'u_list':u_list , 'o_id':o_id }
    print( list )
    return HttpResponseJson( list )

# 分析ページ(全員)
def a_all(request):
    # セッションを持っていない
    if 'u_id' not in request.session:
        return render(request, 'exam/errorpage.html', {'message': '不正なアクセスです'})

    o_id = request.session['o_id']
    users = User.objects.filter(o_id=o_id)

    result_list = []
    t_list = []
    for user in users:
        u_id = user.u_id
        u_name = user.u_name
        r_list = ResultTest.objects.filter(u_id=u_id)
        positive = 0
        for r in r_list:
            t_id = r.t_id
            t_list.append( t_id )
            t_num = r.t_num
            r_answer = r.r_answer
            l_list = LittleTest.objects.filter(t_id=t_id,t_num=t_num)
            q_id = l_list[0].q_id
            q_list = Question.objects.filter(q_id=q_id)
            q_answer = q_list[0].q_answer
            if r_answer == q_answer:
                positive = positive + 1

        result ={'u_id':u_id , 'u_name':u_name , 'positive':positive }
        result_list.append( result )
        print("%s,%s,%s,%d\n" % (u_id, u_name,t_id,positive))

    test_set = set(t_list)
    test_list = []
    for t in test_set:
        test_list.append({'t_id': t})
    u_admin = request.session['u_admin']

    make_test_uid = MakeLittletest.objects.values('u_id').distinct()

    make_test_uid_list = []

    for m in make_test_uid:
        u_id = m['u_id']
        make_test_uid_list.append( {'u_id':u_id})

    return render(request, 'exam/a_all.html', {'result_list': result_list, 'u_admin': u_admin,'test_list':test_list , 'make_test_uid_list':make_test_uid_list})

# 分析ページ(分野ごと)
def a_bunya(request):
    # セッションを持っていない
    if 'u_id' not in request.session:
        return render(request, 'exam/errorpage.html', {'message': '不正なアクセスです'})
    u_id = request.session['u_id']
    o_id = request.session['o_id']
    users = User.objects.filter(o_id=o_id)
    user_list = users.values('u_id', 'u_name')
    print( user_list )
    littletest = LittleTest.objects.filter(o_id=o_id)
    l_list = []
    l_id_old = 0
    for l in littletest:
        q_id = l.q_id
        question = Question.objects.filter(q_id=q_id)
        c_id = question[0].c_id
        classify = Classify.objects.filter(c_id=c_id)

        l_id = classify[0].l_id
        l_name = classify[0].l_name

        if l_id != l_id_old:
            l_list.append( {'l_id':l_id ,'l_name':l_name })
            l_id_old = l_id


    print( l_list )
    u_admin = request.session['u_admin']
    return render(request, 'exam/a_bunya.html', {'user_list': user_list, 'u_admin': u_admin , 'l_list':l_list , 'u_id':u_id} )

#分析ページ
def analysis( request):
    #セッションを持っていない
    if 'u_id' not in request.session:
        return render( request,'exam/errorpage.html',{'message':'不正なアクセスです'})
    u_id = request.session['u_id']
    o_id = request.session['o_id']
    users = User.objects.filter( o_id=o_id)
    user_list = users.values('u_id','u_name')

    u_admin = request.session['u_admin']

    return render( request, 'exam/analysis.html',{'user_list':user_list ,'u_admin':u_admin , 'u_id':u_id } )

#サイト管理者ログイン
def salogin( request ):
    return render( request,'exam/salogin.html')

#サイト管理者ページ
def sapage( request ):
    #u_idやパスワードを持っていない
    if request.method != "POST" and 'sa_id' not in request.session:
        return render( request,'exam/errorpage.html',{'message':'不正なアクセスです。'})

    if "POST" in request.method:
        u_id = request.POST['u_id']
        u_pass = request.POST['u_pass']
        request.session['sa_id'] = u_id

    if "sa_id" in request.session:
        u_id = request.session['sa_id']
        return render(request, 'exam/sapage.html')

    #u_idが存在するか
    try:
        s_user = SuperUser.objects.get(u_id=u_id)
    except ObjectDoesNotExist:
        addAccessLog(request,'sapage','f')
        return render(request, 'exam/salogin.html', {'message': 'ユーザID（メールアドレス）、パスワードのいずれかが違います。'})

    #ブルートフォースチェック
    if checkBruteforce(u_id,'sapage'):
        return render(request, 'exam/errorpage.html', {'message': '不正なアクセスです。'})

    if s_user.u_pass == u_pass:
        addAccessLog(request, 'sapage','s')
        return render( request,'exam/sapage.html')

    addAccessLog(request, 'sapage', 'f')
    return render( request, 'exam/errorpage.html',{'message','ログインできません。'})

#スーパーユーザがライセンス追加を許可する
def saaddlicense( request ):
    org = Org.objects.all()
    list = []
    for o in org:
        dic = {}
        dic['o_id'] = o.o_id
        dic['o_name'] = o.o_name
        dic['l_num'] = o.l_num
        list.append( dic )
    return render( request,'exam/saaddlicense.html',{'org_list':list})

#組織ごとのフィルタ
def saaddlicense_filter( request ):
    dic = byteToDic( request.body )

    print( dic )

    adr_list = AddLicenseRequest.objects.filter(o_id=dic['o_id'])
    list = []
    for adr in adr_list:
        d = {}
        d['id'] = adr.id
        d['l_num'] = adr.l_num
        d['adr_date'] = adr.adr_date.strftime('%Y/%m/%d %H:%M:%S')
        d['check'] = adr.check
        list.append( d )
    jsonStr = json.dumps(list, ensure_ascii=False, indent=2)
    return HttpResponse(jsonStr,content_type='application/json',charset='utf-8')

#ライセンス追加confirm
def saaddlicense_conf( request ):
    dics = byteToDic(request.body)
    adr = AddLicenseRequest.objects.get(pk=dics['id'])
    o_id = adr.o_id
    org = Org.objects.get(pk=o_id)
    org.l_num = org.l_num + adr.l_num
    adr.check = True
    adr.save()
    org.save()
    adr_list = AddLicenseRequest.objects.all()
    list = []
    for adr in adr_list:
        dict = {}
        dict['id'] = adr.id
        dict['o_id'] = adr.o_id
        dict['l_num'] = adr.l_num
        dict['adr_date'] = adr.adr_date.strftime('%Y/%m/%d %H:%M:%S')
        dict['check'] = adr.check
        list.append( dict )
    jsonStr = json.dumps(list, ensure_ascii=False, indent=2)
    return HttpResponse(jsonStr,content_type='application/json',charset='utf-8')

#組織内ユーザの追加csv番
def userregistercsv( request ):
    securecheck( request )

    if request.method != 'POST':
        return render( request, 'exam/userregistercsv.html',{'users':[],'ng_users':[],'ok_users':[] , 'u_admin':request.session['u_admin']})

    #リクエストにfileが含まれている
    if 'file' in request.FILES:
        o_id = request.session['o_id']
        u_num = User.objects.filter(o_id=o_id).count()

        file = TextIOWrapper(request.FILES['file'],encoding="utf-8")
        csv_file = csv.reader(file)
        header = next(csv_file)
        users = []

        for i,row in enumerate(csv_file):
            users.append({'u_id':o_id + code4(i+u_num+1),'u_name':row[0],'u_pass':row[1],'u_email':row[2],'u_admin':row[3],'u_enable':row[4]})

        return render( request, 'exam/userregistercsv.html',{'o_id':o_id,'users':users,'u_admin':request.session['u_admin']})

    #アップデート
    l_num = int( request.POST['u_num'])

    #登録できるアカウント数の計算
    o_id = request.session['o_id']
    org = Org.objects.get(pk=o_id)
    ng_users = []
    ok_users = []
    #人数クリア追加可能
    if org.u_num_check(l_num=l_num):
        for i in range( l_num ):
            u_id = request.POST['u_id_%d'%i]
            u_name = request.POST['u_name_%d'%i]
            u_pass = request.POST['u_pass_%d'%i]
            u_email = request.POST['u_email_%d'%i]
            u_admin = request.POST['u_admin_%d'%i]
            u_enable = request.POST['u_enable_%d'%i]

            create_date = timezone.now()
            org_id = request.POST['o_id_%d'%i]
            user = {'u_id':u_id,'u_pass':u_pass,'u_name':u_name,'u_email':u_email,'u_admin':u_admin,'u_enable':u_enable}
            obj,created = User.objects.get_or_create(u_id=u_id,u_name=u_name,u_pass=u_pass,u_email=u_email,u_admin=u_admin,u_enable=u_enable,u_hidden=False,u_date=create_date,o_id=org_id)
            print( created )
            if created:
                ok_users.append(user)
            else:
                ng_users.append(user)

    if len(ng_users) > 0 and len(ok_users) > 0:
        print( '両方' )
        return render( request,'exam/userregistercsv.html',{'ok_users':ok_users,'ng_users':ng_users})
    elif len(ng_users) > 0:
        print( 'NG' )
        return render( request,'exam/userregistercsv.html',{'ng_users':ng_users})
    elif len(ok_users) > 0:
        print( 'OK' )
        return render( request,'exam/userregistercsv.html',{'ok_users':ok_users})
    else:
        return render(request, 'exam/userregistercsv.html',{'error_message':'登録数が越えています'})
    return render( request , 'exam/userregistercsv.html',{'u_admin':request.session['u_admin']})

#組織内ユーザの追加Web版
def userregisterweb( request ):
    securecheck(request)

    if request.method != 'POST':
        return render( request , 'exam/userregisterweb.html',{'u_admin':request.session['u_admin']})

    o_id = request.session['o_id']

    #登録できるアカウント数の計算
    org = Org.objects.get(pk=o_id)
    ng_users = []
    ok_users = []
    #人数クリア追加可能
    if org.u_num_check(l_num=1):
        u_id = request.POST['u_id']
        u_id = o_id + u_id
        u_name = request.POST['u_name']
        u_pass = request.POST['u_pass']
        u_email = request.POST['u_email']
        u_admin = '0'
        u_enable = '1'

        create_date = timezone.now()
        user = {'u_id':u_id,'u_pass':u_pass,'u_name':u_name,'u_email':u_email,'u_admin':u_admin,'u_enable':u_enable}
        obj,created = User.objects.get_or_create(u_id=u_id,u_name=u_name,u_pass=u_pass,u_email=u_email,u_admin=u_admin,u_enable=u_enable,u_hidden=False,u_date=create_date,o_id=o_id)
        print( created )
        if created:
            ok_users.append(user)
        else:
            ng_users.append(user)

    if len(ng_users) > 0 and len(ok_users) > 0:
        print( '両方' )
        return render( request,'exam/userregisterweb.html',{'ok_users':ok_users,'ng_users':ng_users})
    elif len(ng_users) > 0:
        print( 'NG' )
        return render( request,'exam/userregisterweb.html',{'ng_users':ng_users})
    elif len(ok_users) > 0:
        print( 'OK' )
        return render( request,'exam/userregisterweb.html',{'ok_users':ok_users})
    else:
        return render(request, 'exam/userregisterweb.html',{'error_message':'登録数が越えています'})
    return render( request , 'exam/userregisterweb.html',{'u_admin':request.session['u_admin']})

#午後問題表示
def questionpm( request ):
    qpm = QuestionPm.objects.values('q_classify').distinct().order_by('q_classify')
    return render( request,'exam/questionpm.html',{'q_list':qpm})

#-*-*-*-*-*-*-*-*-ajaxの応答-*-*-*-*-*-*-*-*-*-
def ajax_getquestionpm( request ):
    c_dic = byteToDic( request.body )
    classify = c_dic['classify']
    qpm = QuestionPm.objects.filter(q_classify=classify).values()
    q_list = []
    for q in qpm:
        qfn = q['q_test'] + "_" + q['q_period'] + "_" + q['q_classify'] + "_" + q['q_title'] +".pdf"
        afn = q['q_test'] + "_" + q['q_period'] + "_" + q['q_classify'] + "_" + "ans.pdf"
        dict = {}
        dict['qfn'] = qfn
        dict['afn'] = afn
        q_list.append( dict )

    return HttpResponseJson({'q_list':q_list})

def ajax_testdelete( request ):
    c_dic = byteToDic( request.body )
    if 's_test' in c_dic:
        o_id = request.session['o_id']
        s_test = c_dic['s_test']
        LittleTest.objects.filter(t_id=s_test,o_id=o_id).delete()
        MakeLittletest.objects.filter(t_id=s_test,o_id=o_id).delete()
        makelittletest = MakeLittletest.objects.all()

    test_list = []
    for m in makelittletest:
        dict = {}
        dict['t_id'] = m.t_id
        dict['u_id'] = m.u_id
        test_list.append( dict )

    return HttpResponseJson( test_list )

# u_idとt_idから結果を取得する
def ajax_getquestion_period( request):
    c_dic = byteToDic( request.body )
    if 'q_period' in c_dic:
        q_period = c_dic['q_period']
        question = Question.objects.filter(q_period=q_period).values_list('q_id','q_answer')

        questionlist = []
        for q in question:
            dict = {}
            dict['q_id'] = q[0]
            dict['q_answer'] = q[1]
            questionlist.append( dict )

        return HttpResponseJson( questionlist )

def ajax_getquestion_classify( request):
    c_dic = byteToDic( request.body )
    if 'm_id' in c_dic:
        m_id = c_dic['m_id']
        question = Question.objects.values()

        questionlist = []
        for q in question:
            c_id = q['c_id']
            if c_id[2:4] == m_id:
                #print( c_id + "," + c_id[2:4] )
                dict = {}
                dict['q_id'] = q['q_id']
                dict['q_answer'] = q['q_answer']
                questionlist.append( dict )
        print( questionlist )
        return HttpResponseJson( questionlist )
# u_idからt_idを取得する
def gettid( request):
    c_dic = byteToDic( request.body )
    if 'u_id' in c_dic:
        u_id = c_dic['u_id']
        classify = ResultTest.objects.filter(u_id=u_id)
        classify = classify.values('t_id').distinct()
        dics = {'t_id':[]}

        for c in classify:
            dics['t_id'].append( c['t_id'])

        #print( dics )
        return HttpResponseJson( dics )

def list_in_dict_sort( list , key1 , key2 ):
    i = 0
    while i < len( list ) - 1:
        j = i + 1
        while j < len( list ):
            if list[i][key1] > list[j][key1]:
                temp = list[i]
                list[i] = list[j]
                list[j] = temp
            elif list[i][key1] == list[j][key1] and list[i][key2] > list[j][key2]:
                temp = list[i]
                list[i] = list[j]
                list[j] = temp
            j = j + 1
        i = i + 1
    return list

# u_idから分野ごとの点数を取得する
def get_result_bunya( request):
    c_dic = byteToDic( request.body )
    if 'u_id' in c_dic:
        u_id = c_dic['u_id']
        list = []
        resulttest = ResultTest.objects.filter(u_id=u_id)
        for r in resulttest:
            dict = {'u_id': u_id}
            litteltest = LittleTest.objects.filter( t_id=r.t_id,t_num=r.t_num)
            for l in litteltest:
                question = Question.objects.get(pk=l.q_id)
                classify = Classify.objects.get(pk=question.c_id)
                dict['q_id'] = l.q_id
                dict['l_id'] = classify.l_id
                dict['l_name'] = classify.l_name
                dict['m_id'] = classify.m_id
                dict['m_name'] = classify.m_name
                dict['s_id'] = classify.s_id
                dict['s_name'] = classify.s_name
                dict['r_answer'] = r.r_answer
                dict['q_answer'] = question.q_answer
                if r.r_answer == question.q_answer:
                    dict['result'] = 1
                else:
                    dict['result'] = 0
                list.append( dict )

        list = list_in_dict_sort(list,'m_id','s_id')


        return HttpResponseJson( list )

# u_idから分野を取得する
def get_m_list( request):
    c_dic = byteToDic( request.body )
    print( "get_m_list" )
    if 'u_id' in c_dic:
        u_id = c_dic['u_id']
        l_id1 = c_dic['l_id']
        m_dics = {}
        resulttest = ResultTest.objects.filter(u_id=u_id)
        for r in resulttest:
            t_id = r.t_id
            t_num = r.t_num
            littletest = LittleTest.objects.filter(t_id=t_id,t_num=t_num)
            q_id = littletest.order_by('t_key').first().q_id
            question = Question.objects.filter( q_id=q_id )
            c_id = question.order_by('q_id').first().c_id
            classify = Classify.objects.filter(c_id=c_id)
            l_id2 = classify.order_by('c_id').first().l_id
            m_id = classify.order_by('c_id').first().m_id
            m_name = classify.order_by('c_id').first().m_name
            if l_id1 == l_id2:
                print( "%s,%s"%(m_id,m_name))
                m_dics[m_id] = m_name

        return HttpResponseJson( m_dics )

def get_s_list( request):
    c_dic = byteToDic( request.body )
    print( "get_s_list" )
    if 'u_id' in c_dic:
        u_id = c_dic['u_id']
        l_id1 = c_dic['l_id']
        m_id1 = c_dic['m_id']
        s_dics = {}
        resulttest = ResultTest.objects.filter(u_id=u_id)
        for r in resulttest:
            t_id = r.t_id
            t_num = r.t_num
            littletest = LittleTest.objects.filter(t_id=t_id,t_num=t_num)
            q_id = littletest.order_by('t_key').first().q_id
            question = Question.objects.filter( q_id=q_id )
            c_id = question.order_by('q_id').first().c_id
            classify = Classify.objects.filter(c_id=c_id)
            l_id2 = classify.order_by('c_id').first().l_id
            m_id2 = classify.order_by('c_id').first().m_id
            s_id = classify.order_by('c_id').first().s_id
            s_name = classify.order_by('c_id').first().m_name
            if l_id1 == l_id2 and m_id1 == m_id2:
                print( "%s,%s"%(s_id,s_name))
                s_dics[s_id] = s_name

        return HttpResponseJson( s_dics )

# u_idとt_idからテストの結果を取得する
def getresult( request):
    c_dic = byteToDic( request.body )
    #print( c_dic )
    if 'u_id' in c_dic:
        u_id = c_dic['u_id']
        t_id = c_dic['t_id']
        dics = {'u_id': u_id ,'t_id': t_id , 't_num' :[] , 'q_id':[],'r_answer':[] , 'q_answer':[] , 'mb' : [] , 'score':0 , 'total' : 0}
        resulttest = ResultTest.objects.filter(u_id=u_id,t_id=t_id)
        score1 = 0
        score2 = 0
        print( "%s,%s"%(u_id,t_id))
        for r in resulttest:
            t_num = r.t_num
            r_answer = r.r_answer
            littletest = LittleTest.objects.filter(t_id=t_id,t_num=t_num)
            q_id = littletest.order_by('t_key').first().q_id
            #q_id = littletest[0].q_id
            dics['q_id'].append( q_id )
            question = Question.objects.filter( q_id=q_id)
            q_answer = question.order_by('q_id').first().q_answer
            dics['t_num'].append( t_num )
            dics['r_answer'].append( r_answer)
            dics['q_answer'].append( q_answer)
            if r_answer == q_answer:
                dics['mb'].append( 1 )
                score1 = score1 + 1
            else:
                dics['mb'].append( 0 )
                score2 = score2 + 1

        dics['score'] = score1
        dics['total'] = score1 + score2

        #print( dics )
        return HttpResponseJson( dics )

#分類名を取得する
def getclass( request ):

    c_dic = byteToDic( request.body )

    if 'l_class' in c_dic:
        l_id = c_dic['l_class']
        print( l_id )
        classify = Classify.objects.filter(l_id=l_id)
        dics = {}
        for c in classify:
            dic = { c.m_id : c.m_name }
            dics.update( dic )

    if 'm_class' in c_dic:
        m_id = c_dic['m_class']
        print( m_id )
        classify = Classify.objects.filter(m_id=m_id)
        classify = classify.values('s_id','s_name').distinct()
        dics = {}
        for c in classify:
            print( c["s_id"] )
            dic = {c["s_id"] : c["s_name"]}
            dics.update( dic )
    return HttpResponseJson(dics)

#分類名を取得する
def getperiod( request ):

    c_dic = byteToDic( request.body )
    ary = []
    if 'q_test' in c_dic:
        q_test = c_dic['q_test']
        classify = Question.objects.filter(q_test=q_test).values('q_period').distinct()
        dics = {}
        for c in classify:
            dic = { 'q_period' : c["q_period"] }
            ary.append( dic )
    print( ary )
    return HttpResponseJson(ary)

#問題を取得する(ajax)
def getquestion( request ):
    q_dic = byteToDic( request.body )

    ary = []
    #大分類、中分類、小分類
    if 'l_class' in q_dic and 'm_class' in q_dic and 's_class' in q_dic:
        l_id = q_dic['l_class']
        m_id = q_dic['m_class']
        s_id = q_dic['s_class']
        q_test = q_dic['q_test']
        classify = Classify.objects.filter(l_id=l_id,m_id=m_id,s_id=s_id)
        for c in classify:
            question = c.question_set.all().filter(q_test=q_test).order_by('c_id','q_title')
            for q in question:
                dic = {}
                dic['q_id'] = q.q_id
                dic['q_title'] = q.q_title
                ary.append(dic)

    #大分類、中分類
    elif 'l_class' in q_dic and 'm_class' in q_dic:
        l_id = q_dic['l_class']
        m_id = q_dic['m_class']
        q_test = q_dic['q_test']
        classify = Classify.objects.filter(l_id=l_id,m_id=m_id)
        for c in classify:
            question = c.question_set.all().filter(q_test=q_test).order_by('c_id','q_title')
            for q in question:
                cp = CompQuestion.objects.filter(q_id1=q.q_id)
                dic = {}
                dic['q_id'] = q.q_id
                dic['q_title'] = q.q_title
                ary.append(dic)

    #大分類
    elif 'l_class' in q_dic:
        l_id = q_dic['l_class']
        q_test = q_dic['q_test']
        classify = Classify.objects.filter( l_id=l_id )
        for c in classify:
            question = c.question_set.all().filter(q_test=q_test).order_by('c_id','q_title')
            for q in question:
                dic = {}
                dic['q_id'] = q.q_id
                dic['q_title'] = q.q_title
                ary.append( dic )

    elif 'q_test' in q_dic and 'q_period' in q_dic:
        q_test = q_dic['q_test']
        q_period = q_dic['q_period']
        question = Question.objects.filter( q_test=q_test,q_period=q_period).distinct()
        for q in question:
            dic = {}
            dic['q_id'] = q.q_id
            dic['q_title'] = q.q_title
            comp = CompQuestion.objects.filter(q_id1=q.q_id)
            comp_list = []
            for c in comp:
                comp_list.append(c.q_id2)
            dic['comp_list'] = comp_list
            ary.append( dic )

    return HttpResponseJson(ary)

#作ったテストをデータベースにアップする
def testupdate( request ):
    securecheck( request )
    u_id = request.session['u_id']
    if '@' in u_id:
        user = User.objects.get(u_email=u_id)
    else:
        user = User.objects.get(u_id=u_id)

    o_id = user.o_id

    num = LittleTest.objects.filter(o_id=o_id).values('t_id').distinct().count()

    t_id = code4(num+1)
    test_dic = byteToDic( request.body)
    q_list = test_dic['q_list']
    t_date = datetime.datetime.now()
    for item in q_list:
        print( item )
        t_num = item['t_num']
        t_key = o_id + t_id + t_num
        q_id = item['q_id']
        l_test = LittleTest(t_key=t_key,t_id=t_id,t_num=t_num,t_date=t_date,o_id=o_id,q_id=q_id)
        l_test.save()

    m_test = MakeLittletest(m_key="%s%s"%(o_id,t_id),o_id=o_id,t_id=t_id,u_id=u_id)
    m_test.save()

    return HttpResponse(json.dumps({"state":"ok"}, ensure_ascii=False, indent=2), content_type='application/json', charset='utf-8')

#テストの印刷用データをajaxで取得する
def gettestprint( request ):
    t_id_dic = byteToDic( request.body )
    o_id = request.session['o_id']
    test = LittleTest.objects.filter(o_id=o_id,t_id=t_id_dic['t_id'])
    list = []
    for item in test:
        dic={}
        dic['t_id']=item.t_id
        dic['t_num']=item.t_num
        dic['q_id']=item.q_id
        dic['q_answer'] = item.get_q_answer()
        c = item.get_classify()
        dic['l_name'] = c.l_name
        dic['m_name'] = c.m_name
        dic['s_name'] = c.s_name
        list.append(dic)

    return HttpResponseJson( list )

def ajax_answerupload( request ):

    c_dic = byteToDic(request.body)
    o_id = request.session['o_id']

    test_id = c_dic['t_id']
    user_id = c_dic['u_id']
    answerlist = c_dic['answerlist']

    media_path = os.path.join(settings.STATIC_ROOT,"exam","answer",o_id)

    # 登録チェック
    check_answer = ResultTest.objects.filter(t_id=test_id, u_id=user_id)

    # すでにテストID＋ユーザIDが存在する場合
    if len(check_answer) >= 1:
        for i,a in enumerate( answerlist ):
            result=ResultTest.objects.filter(t_id=test_id,u_id=user_id,t_num=code4(i+1))
            result.update(r_answer=a[1])
            #ret = resulttest.objects.filter(t_num=code4(i+1))
            #print( ret.t_num )

        return HttpResponseJson( {'message':'更新しました。'})
    else:

        # 解答をResultTestに登録する
        date = datetime.datetime.now()

        # テスト数を取得
        num = LittleTest.objects.filter(o_id=o_id, t_id=test_id).count()

        cnt = 0
        for answer in answerlist:
            if cnt < num:
                if answer[1] == "未回答" or answer[1] == "複数回答":
                    add_rt = ResultTest(t_id=test_id, t_num=code4(answer[0]), r_answer='', r_date=date, u_id=user_id)
                else:
                    add_rt = ResultTest(t_id=test_id, t_num=code4(answer[0]), r_answer=answer[1], r_date=date,
                                        u_id=user_id)
                add_rt.save()
            cnt = cnt + 1
        # ファイルを削除する
        filelist = glob.glob(media_path + '/*')

        for file in filelist:
            print(os.path.join(media_path, file))
            # os.remove( os.path.join(media_path, file ) )
    c_dic['message'] = "登録できました。"
    return HttpResponseJson( c_dic )

#解答のアップロード
def answerupload( request ):

    securecheck( request )
    u_admin = request.session['u_admin']
    # アップするファイルのパス
    o_id = request.session['o_id']
    media_path = os.path.join(settings.STATIC_ROOT,"exam","answer",o_id)

    #if 't_id' in request.POST:
    #    print( "post" )
    #    dic = byteToDic(request.body )
    #    return HttpResponseJson(dic)

    if request.method != 'POST':
        answerimage = AnswerImage.objects.all()
        #リストの再取得
        filelist = []
        for file in answerimage:
            filelist.append( file )
        return render(request, 'exam/answerupload.html', {"filelist": filelist,'u_admin':u_admin})

    # リクエストにfileが含まれている
    if 'file' in request.FILES:

        upfiles = request.FILES.getlist('file')

        #複数ファイルのアップは拒否
        if len(upfiles)>1:
            return render(request, 'exam/answerupload.html',{"message": "ファイルのアップロードは1つずつにしてください。",'u_admin':u_admin})

        #複数のファイルがアップロードされる
        for uf in upfiles:
            files = os.listdir( media_path )
            if len(files)+1 < 10:
                num = "00" + str( len(files)+1 )
            elif len(files)+1 < 100:
                num = "0" + str( len(files)+1)
            else:
                num = str(len(files)+1)
            filename = "answer%s.jpg"%num
            filepath = os.path.join( media_path , filename )
            dest = open( filepath ,'wb+')

            for chunk in uf:
                dest.write( chunk )

            # 画像認識
            org_id, test_id, user_id, answerlist = get_answer_list(filepath)

            # 登録チェック
            check_answer = ResultTest.objects.filter( t_id=test_id,u_id=user_id )

            # すでにテストID＋ユーザIDが存在する場合
            if len( check_answer ) >= 1:
                # リストの再取得
                #answerimage = AnswerImage.objects.all()
                #filelist = []
                #for file in answerimage:
                #    filelist.append(file)
                #msg = msg + uf.name
                return render(request, 'exam/answerupload.html', { "message" : "そのデータはすでに存在します。", "t_id" : test_id , "u_id" : user_id , "answerlist" : answerlist ,'u_admin':u_admin})
            else:
                # 画像をデータベースに登録する
                #add_answerimage = AnswerImage( image=filename , o_id=org_id , t_id=test_id , u_id=user_id )
                #add_answerimage.save()

                # 解答をResultTestに登録する
                date = datetime.datetime.now()

                #テスト数を取得
                num = LittleTest.objects.filter( o_id=org_id,t_id=test_id ).count()
                #num = record.count()

                cnt = 0
                for answer in answerlist:
                    if cnt < num:
                        if answer[1] == "未回答" or answer[1] == "複数回答":
                            add_rt = ResultTest(t_id=test_id, t_num=code4(answer[0]), r_answer='', r_date=date, u_id=user_id)
                        else:
                            add_rt = ResultTest(t_id=test_id,t_num=code4(answer[0]),r_answer=answer[1],r_date=date,u_id=user_id)
                        add_rt.save()
                    cnt = cnt + 1
                #ファイルを削除する
                filelist = glob.glob( media_path + '/*')

                for file in filelist:
                    print( os.path.join(media_path,file))
                    #os.remove( os.path.join(media_path, file ) )

        # リストの再取得
        #answerimage = AnswerImage.objects.all()
        #filelist = []
        #for file in answerimage:
        #    filelist.append( file )

        return render(request, 'exam/answerupload.html' , { "t_id" : test_id , "u_id" : user_id , "answerlist" : answerlist ,'u_admin':u_admin})

    elif 'del' in request.POST:
        image = request.POST['del']
        AnswerImage.objects.filter(image=image).delete()
        os.remove( os.path.join( media_path , image ))

        # リストの再取得
        answerimage = AnswerImage.objects.all()
        filelist = []
        for file in answerimage:
            filelist.append( file )

        return render( request, 'exam/answerupload.html' , { "filelist" : filelist ,'u_admin':u_admin})

def get_test_id_list( request ):
    c_dic = byteToDic(request.body )

    if 'u_id' in c_dic:
        u_id = c_dic['u_id']
        mk = MakeLittletest.objects.filter(u_id=u_id)
        test_list = []
        for m in mk:
            t_id = m.t_id
            test_list.append( {'t_id':t_id})
    print( test_list )
    return HttpResponseJson( test_list )

def get_test_id_result( request ):

    # セッションを持っていない
    if 'u_id' not in request.session:
        return render(request, 'exam/errorpage.html', {'message': '不正なアクセスです'})

    c_dic = byteToDic(request.body )
    t_id = c_dic['t_id']
    t_id2 = t_id
    o_id = request.session['o_id']
    users = User.objects.filter(o_id=o_id)

    result_list = []
    t_list = []
    for user in users:
        u_id = user.u_id
        u_name = user.u_name
        if t_id2 == 'all':
            r_list = ResultTest.objects.filter(u_id=u_id)
        else:
            r_list = ResultTest.objects.filter(u_id=u_id,t_id=t_id)
        positive = 0
        for r in r_list:
            if t_id2 == 'all':
                t_id = r.t_id
            t_list.append( t_id )
            t_num = r.t_num
            r_answer = r.r_answer
            l_list = LittleTest.objects.filter(t_id=t_id,t_num=t_num)
            q_id = l_list[0].q_id
            q_list = Question.objects.filter(q_id=q_id)
            q_answer = q_list[0].q_answer
            if r_answer == q_answer:
                positive = positive + 1

        result ={'u_id':u_id , 'u_name':u_name , 'positive':positive }
        result_list.append( result )
        #print("%s,%s,%s,%d\n" % (u_id, u_name,t_id,positive))
        print( result_list )
    return HttpResponseJson( result_list )