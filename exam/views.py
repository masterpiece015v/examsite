from io import TextIOWrapper
from django.shortcuts import render,HttpResponseRedirect
from django.http import HttpResponse
from django.core.mail import EmailMessage
import re,string,random,datetime,os,csv
from .models import *
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

#グローバル変数
testdic = {'fe':'基本情報','ap':'応用情報','sc':'情報セキュリティ'}

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
    return ast.literal_eval( data.decode() )
#セッションにu_idを含むかをチェックする
def securecheck( request ):
    if 'u_id' not in request.session:
        return render( request,'exam/errorpage.html',{'message','不正なアクセスです。'})
#HttpResponseのJSON
def HttpResponseJson( jsonobj ):
    jsonStr = json.dumps( jsonobj , ensure_ascii=False, indent=2)
    return HttpResponse(jsonStr, content_type='application/json', charset='utf-8')
#リストを整列する
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

#-*-*-*-*-*-ページ-*-*-*-*-*-*-*-*-*
#ログイン
class Index():
    def index( request):
        request.session.clear()
        return render(request, 'exam/index.html')

#新規ユーザ登録
class NewUser():
    def newuser( request ):
        if request.method != "POST":
            return render(request,'exam/newuser.html')

        u_email = request.POST['u_email']
        # メールアドレスチェック
        #try:
        #    user = User.objects.get(u_email=u_email)
        #except ObjectDoesNotExist:
        #存在しないので登録できる
        auth_key = auth_add('newuser', u_email)

        sub = '新規ユーザ登録'
        con = """
            新規ユーザ登録をしていただきありがとうございました。
            24時間以内に、下記URLから本登録にお進みください。
            http://examsite.room.kaikei.ac.jp/exam/orgregister/?auth_key=%s
            """ % (auth_key)
        EmailMessage(sub, con, to=[u_email, ]).send()
        return render(request, 'exam/message.html', {'message': 'メールアドレス宛に登録サイトのURLを送信しました。'})

        #メールアドレスが存在したので登録できない
        #return render( request,'exam/newuser.html',{'message':'そのメールアドレスはすでに登録されています。'})

#アカウント登録
class OrgRegister():
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

        num = Org.objects.values('o_id')

        numlist=[]
        for n in num:
            numlist.append( int(n['o_id']) )

        if len( numlist ) == 0:
            o_id = '0001'
        else:
            o_id = code4(max(numlist) + 1)

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

# パスワードを変更する
class PassChange():
    def passchange( request ):
        return render( request, 'exam/passchange.html')

# パスワードの変更完了
class PassChangeFinish():
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
class Inquiry():
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
class Addlicense():
    def addlicense( request ):
        #セッションにユーザIDの記録がない
        securecheck( request )

        o_id = request.session['o_id']
        org = Org.objects.get(o_id=o_id)
        o_name = org.o_name
        return render( request,'exam/addlicense.html',{'o_id':o_id,'o_name':o_name,'u_admin':request.session['u_admin']})

#ライセンスの購入
class AddlicenseConf():
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
class Logoff():
    def logoff( request ):
        request.session['u_id'] = ""
        return render( request,'exam/index.html')


# メインページ
class MainPage():
    def mainpage(request):
        t_dict = {'fe': '基本情報', 'ap': '応報情報', 'sc': 'セキュリティ'}
        # セッションIDがある(戻るボタンなどで帰ってきたとき用)
        if 'u_id' in request.session:
            if request.session['u_id'] != "":

                u_id = request.session['u_id']
                try:
                    user = User.objects.get(pk=u_id)
                except:
                    return render(request, 'exam/errorpage.html', {'message': '不正なアクセスです。'})
                # request.session['u_id'] = u_id
                u_name = user.u_name
                u_admin = user.u_admin
                request.session['u_admin'] = u_admin
                test = Question.objects.values_list('q_test').distinct()
                testlist = []
                for t in test:
                    dict = {}
                    dict['test'] = t[0]
                    dict['name'] = t_dict[t[0]]
                    testlist.append(dict)

                period = Question.objects.values_list('q_period').distinct()
                periodlist = []
                for p in period:
                    dict = {}
                    dict["period"] = p[0]
                    if p[0][3:5]=="01":
                        dict["name"] = p[0][0:3] + "(春)"
                    else:
                        dict["name"] = p[0][0:3] + "(秋)"
                    periodlist.append( dict )

                classify = Classify.objects.values_list('m_id', 'm_name').distinct()
                print(classify)
                classifylist = []
                for c in classify:
                    dict = {}
                    dict['m_id'] = c[0]
                    dict['m_name'] = c[1]
                    classifylist.append(dict)

                return render(request, 'exam/mainpage.html',
                              {'u_id': u_id, 'u_name': u_name, 'u_admin': u_admin, 'period': periodlist,
                               'classify': classifylist, 'test': testlist})

        # u_idやパスワードを持っていない
        if request.method != "POST":
            return render(request, 'exam/errorpage.html', {'message': '不正なアクセスです。'})

        u_id = request.POST["u_id"]
        u_pass = request.POST["u_pass"]
        ipa = request.environ['REMOTE_ADDR']  # IP-Address

        # アカウントが有効かをチェック
        try:
            print(u_id)
            user = User.objects.get(pk=u_id)
        except:
            return render(request, 'exam/errorpage.html', {'message': '不正なアクセスです。'})

        if user.u_enable == False:
            return render(request, 'exam/errorpage.html', {'message': 'アカウントが有効ではありません。管理者に問い合わせてください。'})

        # ブルートフォース対策10分間に100回以上のログイン失敗
        if checkBruteforce(u_id, 'mainpage'):
            user.u_enable = 0
            user.save()
            con = """
            不正なアクセスを検知したので、アカウントをロックしました。
            解除申請をしてください。
            """
            EmailMessage('アカウントロック', con, to=[user.u_email, ]).send()
            return render(request, 'exam/errorpage.html', {'message': '不正なログインを検知しました。アカウントをロックします。'})

        # u_idが存在するか
        try:
            user = User.objects.get(u_id=u_id)
        except ObjectDoesNotExist:
            # メールアドレスが存在するか
            try:
                user = User.objects.get(u_email=u_id)
            except ObjectDoesNotExist:
                # どちらも存在しない（ログイン失敗)
                addAccessLog(request, 'mainpage', 'f')
                return render(request, 'exam/index.html', {'message': 'ユーザID（メールアドレス）、パスワードのいずれかが違います。'})

        if user.pass_check(u_pass=u_pass):
            addAccessLog(request, 'mainpage', 's')
            request.session['u_id'] = u_id
            u_name = user.u_name
            u_admin = user.u_admin
            request.session['o_id'] = user.o_id
            request.session['u_admin'] = u_admin
            test = Question.objects.values_list('q_test').distinct()
            testlist = []
            for t in test:
                dict = {}
                dict['test'] = t[0]
                dict['name'] = t_dict[t[0]]
                testlist.append(dict)

            period = Question.objects.values_list('q_period').distinct()
            periodlist = []
            for p in period:
                dict = {}
                dict["period"] = p[0]
                if p[0][3:5] == "01":
                    dict["name"] = p[0][0:3] + "(春)"
                else:
                    dict["name"] = p[0][0:3] + "(秋)"
                periodlist.append(dict)

            classify = Classify.objects.values_list('m_id', 'm_name').distinct()

            classifylist = []
            for c in classify:
                dict = {}
                dict['m_id'] = c[0]
                dict['m_name'] = c[1]
                classifylist.append(dict)
            return render(request, 'exam/mainpage.html',
                          {'u_id': u_id, 'u_name': u_name, 'u_admin': u_admin, 'period': periodlist,
                           'classify': classifylist,'test':testlist})
        else:
            addAccessLog(request, 'mainpage', 'f')
            return render(request, 'exam/index.html', {'message': 'ユーザID（メールアドレス）、パスワードのいずれかが違います。'})

    # 試験区分が送られてくるので、年度期を返す
    def mainpage_ajax_getperiod( request ):

        securecheck( request )
        dic = byteToDic(request.body)
        q_test = dic['q_test']

        json = []
        period = Question.objects.filter(q_test=q_test).values_list('q_period').distinct()
        for p in period:
            dict = {'period':p[0]}
            if p[0][3:5] == "01":
                dict['name'] = p[0][0:3] + "(春)"
            else:
                dict['name'] = p[0][0:3] + "(秋)"
            json.append( dict )

        return HttpResponseJson(json)

    # 試験区分と年度期が送られてくるので、問題を返す
    def ajax_getquestion_period( request):
        c_dic = byteToDic( request.body )
        if 'q_period' in c_dic:
            q_period = c_dic['q_period']
            q_test = c_dic['q_test']
            question = Question.objects.filter(q_period=q_period,q_test=q_test).values_list('q_id','q_answer')

            questionlist = []
            for q in question:
                dict = {}
                dict['q_id'] = q[0]
                dict['q_answer'] = q[1]
                questionlist.append( dict )

            return HttpResponseJson( questionlist )

    # 試験区分と分野が送られてくるので、問題を返す
    def ajax_getquestion_classify( request):
        c_dic = byteToDic( request.body )
        if 'm_id' in c_dic:
            m_id = c_dic['m_id']
            q_test = c_dic['q_test']
            question = Question.objects.filter(q_test=q_test).values()

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

#テスト印刷画面
class TrainPrint():
    #ページを表示する
    def trainprint( request ):
        securecheck( request )

        user = User.objects.get(pk=request.session['u_id'])
        o_id = user.o_id

        test = Question.objects.values('q_test').distinct()
        test_list = []
        for t in test:
            dic = {'test':t['q_test'],'name':testdic[ t['q_test']]}
            test_list.append( dic )
        middle = Question.objects.values('c__m_id','c__m_name').distinct()
        m_list = []
        for m in middle:
            dict= {'m_id':m['c__m_id'],'m_name':m['c__m_name']}
            m_list.append( dict )
        small = Question.objects.values('c__s_id','c__s_name').filter(c__m_id='01').distinct()
        s_list = []
        for s in small:
            dict = {'s_id':s['c__s_id'],'s_name':s['c__s_name']}
            s_list.append( dict )
        question = Question.objects.values('q_id','q_title','q_answer').filter(c__m_id='01',q_test='fe')
        q_list = []
        for q in question:
            dict = {'q_id':q['q_id'],'q_title':q['q_title'],'q_answer':q['q_answer']}
            q_list.append( dict )
        return render( request,'exam/trainprint.html',{'test':test_list,'u_admin':request.session['u_admin'],'m_list':m_list,'s_list':s_list,'q_list':q_list })

    #テストの印刷用データをajaxで取得する
    def ajax_gettrainprint( request ):
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

    #基本、応用が切り替わった
    def ajax_testchange(request ):
        dict = byteToDic( request.body )
        test = dict['test']
        list = []
        if 'm_id' in dict and 's_id' in dict:
            m_id = dict['m_id']
            s_id = dict['s_id']
            question = Question.objects.values('q_id','q_title','q_answer').filter(q_test=test,c__s_id=s_id,c__m_id=m_id)
        elif 'm_id' in dict:
            m_id = dict['m_id']
            question = Question.objects.values('q_id', 'q_title','q_answer').filter(q_test=test, c__m_id=m_id)
        for q in question:
            dict = {'q_id': q['q_id'], 'q_title': q['q_title'],'q_answer':q['q_answer']}
            list.append(dict)

        return HttpResponseJson(list)

    def ajax_m_id_change(request ):
        dict = byteToDic( request.body )
        test = dict['test']
        list1 = []
        if 'm_id' in dict:
            m_id = dict['m_id']
            question = Question.objects.values('q_id', 'q_title','q_answer').filter(q_test=test, c__m_id=m_id)
        for q in question:
            dict = {'q_id': q['q_id'], 'q_title': q['q_title'],'q_answer':q['q_answer']}
            list1.append(dict)
        list2 = []
        classify = Classify.objects.values('s_id','s_name').filter(m_id=m_id)
        for c in classify:
            dict = {'s_id':c['s_id'], 's_name':c['s_name']}
            list2.append( dict )

        return HttpResponseJson({'list1':list1,'list2':list2})

    def ajax_s_id_change(request):
        dict = byteToDic( request.body )
        print( dict )
        test = dict['test']
        list = []
        if 'm_id' in dict and 's_id' in dict:
            m_id = dict['m_id']
            s_id = dict['s_id']
            question = Question.objects.values('q_id','q_title','q_answer').filter(q_test=test,c__s_id=s_id,c__m_id=m_id)
        elif 'm_id' in dict:
            m_id = dict['m_id']
            question = Question.objects.values('q_id', 'q_title','q_answer').filter(q_test=test, c__m_id=m_id)

        for q in question:
            dict = {'q_id': q['q_id'], 'q_title': q['q_title'],'q_answer':q['q_answer']}
            list.append(dict)

        #print( list )
        return HttpResponseJson(list)
#テスト印刷画面
class TestPrint():
    #ページを表示する
    def testprint( request ):
        securecheck( request )
        user = User.objects.get(pk=request.session['u_id'])
        o_id = user.o_id

        mt = MakeLittletest.objects.filter(o_id=o_id,u_id=user.u_id)
        test_list = []
        for m in mt:
            test = LittleTest.objects.filter(t_id=m.t_id).values('t_id','q__c__m_name','t_date').distinct()
            m_name_marge = test[0]['q__c__m_name']
            for i in range(1,len( test )):
                m_name_marge = "%s,%s"%(m_name_marge,test[i]['q__c__m_name'])
            cnt = ResultTest.objects.filter(t_id=m.t_id,u__o_id=o_id).values('t_id','u_id').distinct().count()
            test_list.append({'t_id':m.t_id,'u_id':user.u_id,'t_date':test[0]['t_date'],'cnt':cnt,'m_name':m_name_marge} )

        #test = LittleTest.objects.filter(o_id=o_id).values('t_id','t_date').distinct()

        """
        for t in test:
            t_id = t['t_id']
            #print( "%s%s"%(o_id,t_id))

            mt = MakeLittletest.objects.filter(t_id=t_id).values('u_id')
            for m in mt:
                u_id = m['u_id']
                print( u_id )
            cnt = ResultTest.objects.filter(t_id=t_id,u__o_id=o_id).values('t_id','u_id').distinct().count()
            #print( mt.u_id )
            m_name_set = LittleTest.objects.filter(o_id=o_id,t_id=t_id).values('q__c__m_name').distinct()
            m_name_marge = m_name_set[0]['q__c__m_name']
            for i in range(1,len( m_name_set )):
                m_name_marge = "%s,%s"%(m_name_marge,m_name_set[i]['q__c__m_name'])
            #print( m_name_marge )
            test_list.append( {'t_id':t_id,'u_id':u_id,'t_date':t['t_date'],'cnt':cnt,'m_name':m_name_marge})
            #test_list.append({'t_id': t_id,'t_date': t['t_date'], 'cnt': cnt, 'm_name': m_name_marge})
        """

        return render( request,'exam/testprint.html',{'test_list':test_list,'u_admin':request.session['u_admin']})


    #テストの印刷用データをajaxで取得する
    def ajax_gettestprint( request ):
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

#テスト削除
class TestDelete():
    def testdelete( request ):
        securecheck( request )
        user = User.objects.get(pk=request.session['u_id'])
        o_id = user.o_id

        test = LittleTest.objects.filter(o_id=o_id).values('t_id','t_date').distinct()
        test_list = []
        for t in test:
            t_id = t['t_id']
            mt = MakeLittletest.objects.get(pk="%s%s"%(o_id,t_id))

            test_list.append( {'t_id':t_id,'u_id':mt.u_id,'t_date':t['t_date']})
        return render( request,'exam/testdelete.html',{'test_list':test_list,'u_admin':request.session['u_admin']})

    # テストを消すajax
    def ajax_testdelete( request ):
        c_dic = byteToDic( request.body )

        if 's_test' in c_dic:
            o_id = request.session['o_id']
            s_test = c_dic['s_test']

            resulttest = ResultTest.objects.filter(u__o_id=o_id,t_id=s_test).values()

            print( len( resulttest) )

            #受験履歴があれば削除しない
            if( len(resulttest) == 0 ):
                LittleTest.objects.filter(t_id=s_test,o_id=o_id).delete()
                MakeLittletest.objects.filter(t_id=s_test,o_id=o_id).delete()
            else:
                return HttpResponseJson({'error':s_test+'は受験データが存在します。'})

            makelittletest = MakeLittletest.objects.filter(o_id=o_id).all()

        test_list = []
        for m in makelittletest:
            dict = {}
            dict['t_id'] = m.t_id
            dict['u_id'] = m.u_id
            test_list.append( dict )
        return HttpResponseJson( test_list )

#間違った問題を印刷
class Miss_Question():
    #ページの表示
    def miss_question( request ):
        securecheck( request )
        user = User.objects.get(pk=request.session['u_id'])
        o_id = user.o_id

        users = User.objects.filter(o_id=o_id).values()
        makeusers = MakeLittletest.objects.filter(o_id=o_id).values('u_id').distinct()

        print( users )
        print( makeusers )

        return render( request,'exam/miss_question.html',{'u_admin':request.session['u_admin'] , 'users':users , 'makeusers':makeusers })
    #テストの印刷用データをajaxで取得する
    def ajax_miss_question( request ):
        c_dic = byteToDic( request.body )
        o_id = request.session['o_id']
        m_u_id = c_dic['m_u_id']

        makelittletest = MakeLittletest.objects.filter(o_id=o_id,u_id=m_u_id).values('t_id')
        q_list = []
        list = []
        for t in makelittletest:
            #print( t['t_id'] )
            resulttest = ResultTest.objects.filter(u_id=c_dic['u_id'],t_id=t['t_id']).values('t_id','t_num','r_answer')
            #print( resulttest )
            for item in resulttest:
                littletest = LittleTest.objects.filter(t_id=item['t_id'] , t_num=item['t_num'] , o_id=o_id)
                q_id = littletest[0].q_id
                question = Question.objects.get(pk=q_id)
                if item['r_answer'] != question.q_answer:

                    q_list.append(question.q_id)

        q_list.sort()

        for i in range(len(q_list)):
            question = Question.objects.get(pk=q_list[i])
            dic={}
            #dic['t_id']=item['t_id']
            #dic['t_num']=str( item['t_num'] )
            dic['q_id']=q_list[i]
            dic['q_answer'] = question.q_answer
            classify = Classify.objects.filter(c_id=question.c_id)
            #c = question.get_classify()
            dic['l_name'] = classify[0].l_name
            dic['m_name'] = classify[0].m_name
            dic['s_name'] = classify[0].s_name

            #dic['l_name'] = question_c__l_name
            #dic['m_name'] = question_c__m_name
            #dic['s_name'] = question_c__s_name

            print( dic )
            list.append(dic)

        return HttpResponseJson( list )

#解答用紙印刷
class AnswerSheetPrint():
    # ページの表示
    def answersheetprint( request ):
        o_id = request.session['o_id']
        if 't_id' in request.GET:
            t_id = request.GET.get('t_id')
            test = LittleTest.objects.filter(o_id=o_id, t_id=t_id)
            user = User.objects.filter(o_id=o_id)

            t_list = []
            for t in test:
                dic = {}
                dic['t_num'] = t.t_num
                dic['q_id'] = t.q_id
                t_list.append(dic)

            u_list = []
            for u in user:
                dic = {}
                dic['u_id'] = u.u_id
                dic['u_name'] = u.u_name
                u_list.append(dic)

            list = {'t_list': t_list, 'u_list': u_list, 'o_id': o_id}

            test = LittleTest.objects.filter(o_id=o_id).values('t_id', 't_date').distinct()
            t_list = []
            for t in test:
                dic = {}
                dic['t_id'] = t['t_id']
                dic['t_date'] = t['t_date']
                t_list.append(dic)

            return render(request, 'exam/answersheetprint.html', {'test': t_list, 'u_admin': request.session['u_admin'] , 't_id':t_id , 'list':list })

        test = LittleTest.objects.filter(o_id=o_id).values('t_id','t_date').distinct()
        list = []
        for t in test:
            dic = {}
            dic['t_id'] = t['t_id']
            dic['t_date'] = t['t_date']
            list.append( dic )

        return render( request, 'exam/answersheetprint.html',{'test':list,'u_admin':request.session['u_admin'] })

    # ajax
    def ajax_answersheetprint( request ):
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
        #print( list )
        return HttpResponseJson( list )

# 分析ページ(全員)
class A_All():
    # ページを表示
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
                l_list = LittleTest.objects.filter(t_id=t_id,t_num=t_num,o_id=o_id)
                q_id = l_list[0].q_id
                q_list = Question.objects.filter(q_id=q_id)
                q_answer = q_list[0].q_answer
                if r_answer == q_answer:
                    positive = positive + 1

            result ={'u_id':u_id , 'u_name':u_name , 'positive':positive }
            result_list.append( result )
            #print("%s,%s,%s,%d\n" % (u_id, u_name,t_id,positive))

        test_set = set(t_list)
        test_list = []
        for t in test_set:
            test_list.append({'t_id': t})
        u_admin = request.session['u_admin']

        make_test_uid = MakeLittletest.objects.filter(o_id=o_id).values('u_id').distinct()
        make_test_uid_list = []
        for m in make_test_uid:
            u_id = m['u_id']
            make_test_uid_list.append( {'u_id':u_id})

        return render(request, 'exam/a_all.html', {'result_list': result_list, 'u_admin': u_admin,'test_list':test_list , 'make_test_uid_list':make_test_uid_list})

    # 管理者IDからTestIdを取得するajax
    def ajax_gettestidlist(request):
        c_dic = byteToDic(request.body)

        if 'u_id' in c_dic:
            u_id = c_dic['u_id']
            mk = MakeLittletest.objects.filter(u_id=u_id)
            test_list = []
            for m in mk:
                t_id = m.t_id
                test_list.append({'t_id': t_id})

        return HttpResponseJson(test_list)
    # テストIDからテストの結果を取得するajax
    def ajax_gettestidresult( request ):
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
                l_list = LittleTest.objects.filter(t_id=t_id,t_num=t_num,o_id=o_id)
                q_id = l_list[0].q_id
                q_list = Question.objects.filter(q_id=q_id)
                q_answer = q_list[0].q_answer
                if r_answer == q_answer:
                    positive = positive + 1

            result ={'u_id':u_id , 'u_name':u_name , 'positive':positive }
            result_list.append( result )
            # print("%s,%s,%s,%d\n" % (u_id, u_name,t_id,positive))
            # print( result_list )
        return HttpResponseJson( result_list )

# 分析ページ(分野ごと)
class A_Bunya():
    # ページを表示する
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

        #print( l_list )
        u_admin = request.session['u_admin']
        return render(request, 'exam/a_bunya.html', {'user_list': user_list, 'u_admin': u_admin , 'l_list':l_list , 'u_id':u_id} )

    # u_idから分野ごとの点数を取得する ajax
    def ajax_getresultbunya( request):
        c_dic = byteToDic( request.body )
        if 'u_id' in c_dic:
            u_id = c_dic['u_id']
            o_id = request.session['o_id']
            list = []
            resulttest = ResultTest.objects.filter(u_id=u_id)
            for r in resulttest:
                dict = {'u_id': u_id}
                litteltest = LittleTest.objects.values('q_id','q__c__l_id','q__c__l_name','q__c__m_id','q__c__m_name','q__c__s_id','q__c__s_name','q__q_answer').filter( t_id=r.t_id,t_num=r.t_num,o_id=o_id).order_by('q__c__m_id','q__c__s_id')
                for l in litteltest:
                    # question = Question.objects.get(pk=l.q_id)
                    # classify = Classify.objects.get(pk=question.c_id)
                    dict['q_id'] = l['q_id']
                    dict['l_id'] = l['q__c__l_id']
                    dict['l_name'] = l['q__c__l_name']
                    dict['m_id'] = l['q__c__m_id']
                    dict['m_name'] = l['q__c__m_name']
                    dict['s_id'] = l['q__c__s_id']
                    dict['s_name'] = l['q__c__s_name']
                    dict['r_answer'] = r.r_answer
                    dict['q_answer'] = l['q__q_answer']
                    if r.r_answer == l['q__q_answer']:
                        dict['result'] = 1
                    else:
                        dict['result'] = 0
                    list.append( dict )

            list = list_in_dict_sort(list,'m_id','s_id')

            return HttpResponseJson( list )

# 分析ページ
class Analysis():
    # ページの表示
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
    # u_idからt_idを取得する ajax
    def ajax_gettid( request):
        c_dic = byteToDic( request.body )
        if 'u_id' in c_dic:
            u_id = c_dic['u_id']
            classify = ResultTest.objects.filter(u_id=u_id)
            classify = classify.values('t_id').distinct()
            dics = {'t_id':[]}

            for c in classify:
                dics['t_id'].append( c['t_id'])

            return HttpResponseJson( dics )

    # u_idとt_idからテストの結果を取得する ajax
    def ajax_getresult( request):
        c_dic = byteToDic( request.body )
        o_id = request.session['o_id']
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
                littletest = LittleTest.objects.filter(t_id=t_id,t_num=t_num,o_id=o_id)
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

# 解答のアップロード
class AnswerUpload():
    # ページの表示
    def answerupload( request ):

        securecheck( request )
        u_admin = request.session['u_admin']
        # アップするファイルのパス
        o_id = request.session['o_id']
        media_path = os.path.join(settings.STATIC_ROOT,"exam","answer",o_id)

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
            #if len(upfiles)>1:
            #    return render(request, 'exam/answerupload.html',{"message": "ファイルのアップロードは1つずつにしてください。",'u_admin':u_admin})

            #複数のファイルがアップロードされる
            list = []
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
                    #return render(request, 'exam/answerupload.html', { "message" : "そのデータはすでに存在します。", "t_id" : test_id , "u_id" : user_id , "answerlist" : answerlist ,'u_admin':u_admin})
                    dict = {'t_id':test_id,'u_id':user_id,'exists':1}
                    list.append( dict )
                else:
                    # 画像をデータベースに登録する
                    #add_answerimage = AnswerImage( image=filename , o_id=org_id , t_id=test_id , u_id=user_id )
                    #add_answerimage.save()

                    # 解答をResultTestに登録する
                    date = datetime.datetime.now()

                    #テスト数を取得
                    #num = LittleTest.objects.filter( o_id=org_id,t_id=test_id ).count()
                    #num = record.count()

                    cnt = 0
                    for answer in answerlist:
                        if cnt < 80:
                            if answer[1] == "未回答" or answer[1] == "複数回答":
                                add_rt = ResultTestTemp(t_id=test_id, t_num=code4(answer[0]), r_answer='', r_date=date, u_id=user_id)
                            else:
                                add_rt = ResultTestTemp(t_id=test_id,t_num=code4(answer[0]),r_answer=answer[1],r_date=date,u_id=user_id)
                            add_rt.save()
                        cnt = cnt + 1
                    #ファイルを削除する
                    #filelist = glob.glob( media_path + '/*')

                    #for file in filelist:
                        #print( os.path.join(media_path,file))
                        #os.remove( os.path.join(media_path, file ) )
                    dict = {'t_id':test_id,'u_id':user_id,'exists':0}
                    list.append( dict )
            return render(request, 'exam/answerupload.html' , { 'list':list ,'u_admin':u_admin})

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

    # insert
    def ajax_answerinsert( request):
        c_dic = byteToDic(request.body)
        o_id = request.session['o_id']
        print( c_dic )
        old_t_id = c_dic['old_t_id']
        old_u_id = c_dic['old_u_id']
        new_t_id = c_dic['new_t_id']
        new_u_id = c_dic['new_u_id']
        answerlist = c_dic['answerlist']

        media_path = os.path.join(settings.STATIC_ROOT, "exam", "answer", o_id)

        # 登録チェック
        check_answer = ResultTest.objects.filter(t_id=new_t_id, u_id=new_u_id)

        # すでにテストID＋ユーザIDが存在する場合
        if len(check_answer) >= 1:
            for i, a in enumerate(answerlist):
                result = ResultTest.objects.filter(t_id=new_t_id, u_id=new_u_id, t_num=code4(i + 1))
                result.update(r_answer=a[1])
            return HttpResponseJson({'message': '更新しました。'})
        else:
            # 解答をResultTestに登録する
            date = datetime.datetime.now()
            # テスト数を取得
            num = LittleTest.objects.filter(o_id=o_id, t_id=new_t_id).count()

            cnt = 0
            for answer in answerlist:
                if cnt < num:
                    if answer[1] == "未回答" or answer[1] == "複数回答":
                        add_rt = ResultTest(t_id=new_t_id, t_num=code4(answer[0]), r_answer='',r_date=date,u_id=new_u_id)
                    else:
                        add_rt = ResultTest(t_id=new_t_id, t_num=code4(answer[0]), r_answer=answer[1], r_date=date,u_id=new_u_id)
                    add_rt.save()
                cnt = cnt + 1

            # ResultTestTempのデータを削除する
            ResultTestTemp.objects.filter(t_id=old_t_id,u_id=old_u_id).delete()

            # ファイルを削除する
            #filelist = glob.glob(media_path + '/*')

            #for file in filelist:
                #print(os.path.join(media_path, file))
                # os.remove( os.path.join(media_path, file ) )
        c_dic['message'] = "追加できました。"
        return HttpResponseJson(c_dic)

    # すべて追加
    def ajax_answerallinsert(request):
        c_dic = byteToDic(request.body)
        o_id = request.session['o_id']

        list = c_dic['list']
        dict = {'list':[]}

        for l in list:

            # 登録チェック
            t_id = l['t_id']
            u_id = l['u_id']

            check_answer = ResultTest.objects.filter(t_id=t_id, u_id=u_id)

            # すでにテストID＋ユーザIDが存在する場合
            if len(check_answer) >= 1:
                print( t_id )
                dic = {'t_id':t_id , 'u_id':u_id}
                dict['list'].append( dic )

            else:
                # 解答をResultTestに登録する
                date = datetime.datetime.now()
                # テスト数を取得
                num = LittleTest.objects.filter(o_id=o_id, t_id=t_id).count()

                cnt = 0
                resulttesttemp = ResultTestTemp.objects.filter(t_id=t_id,u_id=u_id).valuse()

                for r in resulttesttemp:
                    if cnt < num:
                        if answer[1] == "未回答" or answer[1] == "複数回答":
                            add_rt = ResultTest(t_id=r['t_id'], t_num=r['t_id'], r_answer='', r_date=date,u_id=r['u_id'])
                        else:
                            add_rt = ResultTest(t_id=r['t_id'], t_num=r['t_id'], r_answer=answer[1], r_date=date,u_id=r['u_id'])
                        add_rt.save()
                    cnt = cnt + 1

                    # ResultTestTempのデータを削除する
                    ResultTestTemp.objects.filter(t_id=old_t_id, u_id=old_u_id).delete()
                dic = {'t_id': t_id, 'u_id': u_id}
                dict['list'].append(dic)
        print( dict )
        return HttpResponseJson( dict )

    # upload
    def ajax_answerupload( request ):

        c_dic = byteToDic(request.body)
        o_id = request.session['o_id']

        old_t_id = c_dic['old_t_id']
        old_u_id = c_dic['old_u_id']
        new_t_id = c_dic['new_t_id']
        new_u_id = c_dic['new_u_id']
        answerlist = c_dic['answerlist']

        media_path = os.path.join(settings.STATIC_ROOT,"exam","answer",o_id)

        # 新しいidと古いidが違えば、古いidのほうを消す
        if new_t_id != old_t_id or new_u_id != old_u_id:
            ResultTest.objects.filter(t_id=old_t_id,u_id=old_u_id).delete()

        # 登録チェック
        check_answer = ResultTest.objects.filter(t_id=new_t_id, u_id=new_u_id)

        # すでにテストID＋ユーザIDが存在する場合は元のデータを更新
        if len(check_answer) >= 1:
            for i,a in enumerate( answerlist ):
                result=ResultTest.objects.filter(t_id=new_t_id,u_id=new_u_id,t_num=code4(i+1))
                result.update(r_answer=a[1])

            return HttpResponseJson( {'message':'更新しました。'})
        else:
        #ない場合は追加する
            # 解答をResultTestに登録する
            date = datetime.datetime.now()

            # テスト数を取得
            num = LittleTest.objects.filter(o_id=o_id, t_id=new_t_id).count()

            cnt = 0
            for answer in answerlist:
                if cnt < num:
                    if answer[1] == "未回答" or answer[1] == "複数回答":
                        add_rt = ResultTest(t_id=new_t_id, t_num=code4(answer[0]), r_answer='', r_date=date, u_id=new_u_id)
                    else:
                        add_rt = ResultTest(t_id=new_t_id, t_num=code4(answer[0]), r_answer=answer[1], r_date=date,u_id=new_u_id)
                    add_rt.save()
                cnt = cnt + 1
        c_dic['message'] = "登録できました。"
        return HttpResponseJson( c_dic )

    # t_idとu_idからテストの結果を取得する
    def ajax_getanswerlist(request):
        c_dic = byteToDic(request.body)
        o_id = request.session['o_id']

        t_id = c_dic['t_id']
        u_id = c_dic['u_id']
        ex = c_dic['ex']

        if ex == '未':
            resulttest = ResultTestTemp.objects.filter(t_id=t_id,u_id=u_id).values('t_num','r_answer')
        else:
            resulttest = ResultTest.objects.filter(t_id=t_id, u_id=u_id).values('t_num', 'r_answer')

        result = {'t_id':t_id,'u_id':u_id,'answerlist':[]}

        for r in resulttest:
            dict={'t_num':r['t_num'],'r_answer':r['r_answer']}
            result['answerlist'].append( dict )

        return HttpResponseJson( result )

# cbtam
class CbtAmMain():
    def cbtammain(request):
        return render( request,'exam/cbtammain.html', {'u_admin':request.session['u_admin']})

# cbtpm
class CbtPmMain():
    def cbtpmmain(request):
        questioncbtpm = QuestionCbtPm.objects.values('q_test','q_period').distinct()
        return render( request,'exam/cbtpmmain.html',{'u_admin':request.session['u_admin'] , 'questioncbtpm':questioncbtpm})

# cbtpm
class CbtPm():
    def cbtpm(request):
        q_id = request.GET.get('q_id')
        q_test = q_id[0:2]
        q_period = q_id[2:7]
        question = QuestionCbtPm.objects.values('q_q').filter(q_test=q_test,q_period=q_period).distinct()
        return render( request,'exam/cbtpm.html',{'u_admin':request.session['u_admin'] ,
                                                  'q_test':q_test,'q_period':q_period,
                                                  'question':question ,
                                                  'r_id':random_id(10)})

    def ajax_cbtpm_get_q(request):
        c_dic = byteToDic( request.body )
        #print( c_dic )
        q_test = c_dic['q_test']
        q_period = c_dic['q_period']
        q_q = c_dic['q_q']

        question = QuestionCbtPm.objects.values('q_question','q_symbol','q_lastanswer').filter(q_test=q_test,q_period=q_period,q_q=q_q)
        list = []
        for q in question:
            dict = {}
            dict['q_question'] = q['q_question']
            dict['q_symbol'] = q['q_symbol']
            dict['q_lastanswer'] = q['q_lastanswer']
            list.append( dict )

        return HttpResponseJson( {'pdf':"%s%s%s.pdf"%(q_test,q_period,q_q),'list':list} )

def random_id(n):
    randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
    return ''.join(randlst)

# 問題作成メイン画面
class TestMake():
    def testmake(request):
        # セッションを持っていない
        if 'u_id' not in request.session:
            return render(request, 'exam/errorpage.html', {'message': '不正なアクセスです'})

        l_class_list = Classify.objects.values('l_id', 'l_name').distinct()
        q_test = Question.objects.values('q_test').distinct()

        return render(request, 'exam/testmake.html',
                      {'l_class_list': l_class_list, 'q_test': q_test, 'u_admin': request.session['u_admin']})
    # 分類名を取得する ajax
    def ajax_getclass(request):
        c_dic = byteToDic(request.body)
        if 'l_class' in c_dic:
            l_id = c_dic['l_class']
            print(l_id)
            classify = Classify.objects.filter(l_id=l_id)
            dics = {}
            for c in classify:
                dic = {c.m_id: c.m_name}
                dics.update(dic)

        if 'm_class' in c_dic:
            m_id = c_dic['m_class']
            print(m_id)
            classify = Classify.objects.filter(m_id=m_id)
            classify = classify.values('s_id', 's_name').distinct()
            dics = {}
            for c in classify:
                print(c["s_id"])
                dic = {c["s_id"]: c["s_name"]}
                dics.update(dic)
        return HttpResponseJson(dics)

    # 問題を取得する ajax
    def ajax_getquestion(request):
        q_dic = byteToDic(request.body)

        ary = []
        # 大分類、中分類、小分類
        if 'l_class' in q_dic and 'm_class' in q_dic and 's_class' in q_dic:
            l_id = q_dic['l_class']
            m_id = q_dic['m_class']
            s_id = q_dic['s_class']
            q_test = q_dic['q_test']
            classify = Classify.objects.filter(l_id=l_id, m_id=m_id, s_id=s_id)
            for c in classify:
                question = c.question_set.all().filter(q_test=q_test).order_by('c_id', 'q_title')
                for q in question:
                    dic = {}
                    dic['q_id'] = q.q_id
                    dic['q_title'] = q.q_title
                    ary.append(dic)

        # 大分類、中分類
        elif 'l_class' in q_dic and 'm_class' in q_dic:
            l_id = q_dic['l_class']
            m_id = q_dic['m_class']
            q_test = q_dic['q_test']
            classify = Classify.objects.filter(l_id=l_id, m_id=m_id)
            for c in classify:
                question = c.question_set.all().filter(q_test=q_test).order_by('c_id', 'q_title')
                for q in question:
                    cp = CompQuestion.objects.filter(q_id1=q.q_id)
                    dic = {}
                    dic['q_id'] = q.q_id
                    dic['q_title'] = q.q_title
                    ary.append(dic)

        # 大分類
        elif 'l_class' in q_dic:
            l_id = q_dic['l_class']
            q_test = q_dic['q_test']
            classify = Classify.objects.filter(l_id=l_id)
            for c in classify:
                question = c.question_set.all().filter(q_test=q_test).order_by('c_id', 'q_title')
                for q in question:
                    dic = {}
                    dic['q_id'] = q.q_id
                    dic['q_title'] = q.q_title
                    ary.append(dic)

        elif 'q_test' in q_dic and 'q_period' in q_dic:
            q_test = q_dic['q_test']
            q_period = q_dic['q_period']
            question = Question.objects.filter(q_test=q_test, q_period=q_period).distinct()
            for q in question:
                dic = {}
                dic['q_id'] = q.q_id
                dic['q_title'] = q.q_title
                comp = CompQuestion.objects.filter(q_id1=q.q_id)
                comp_list = []
                for c in comp:
                    comp_list.append(c.q_id2)
                dic['comp_list'] = comp_list
                ary.append(dic)

        return HttpResponseJson(ary)

    # 作ったテストをデータベースにアップする
    def ajax_testupdate(request):
        securecheck(request)
        u_id = request.session['u_id']
        if '@' in u_id:
            user = User.objects.get(u_email=u_id)
        else:
            user = User.objects.get(u_id=u_id)

        o_id = user.o_id

        num = LittleTest.objects.filter(o_id=o_id).values('t_id').distinct()

        numlist=[]
        for n in num:
            numlist.append( int(n['t_id']) )

        if len( numlist ) == 0:
            t_id = '0001'
        else:
            t_id = code4(max(numlist) + 1)

        test_dic = byteToDic(request.body)
        q_list = test_dic['q_list']
        t_date = datetime.datetime.now()
        for item in q_list:
            print(item)
            t_num = item['t_num']
            t_key = o_id + t_id + t_num
            q_id = item['q_id']
            l_test = LittleTest(t_key=t_key, t_id=t_id, t_num=t_num, t_date=t_date, o_id=o_id, q_id=q_id)
            l_test.save()

        m_test = MakeLittletest(m_key="%s%s" % (o_id, t_id), o_id=o_id, t_id=t_id, u_id=u_id)
        m_test.save()

        return HttpResponse(json.dumps({"state": "ok"}, ensure_ascii=False, indent=2), content_type='application/json',
                            charset='utf-8')

#年度期ごとの問題を作成する画面
class TestMakePeriod():
    def testmakeperiod( request ):
        #セッションを持っていない
        if 'u_id' not in request.session:
            return render( request,'exam/errorpage.html',{'message':'不正なアクセスです'})

        q_test = Question.objects.values('q_test').distinct()
        q_period_list = Question.objects.filter(q_test='fe').values('q_period').distinct()
        return render(request,'exam/testmakeperiod.html',{'q_period_list':q_period_list , 'q_test':q_test,'u_admin':request.session['u_admin']})
    # 年度期を取得する
    def ajax_getperiod(request):
        c_dic = byteToDic(request.body)
        ary = []
        if 'q_test' in c_dic:
            q_test = c_dic['q_test']
            classify = Question.objects.filter(q_test=q_test).values('q_period').distinct()
            dics = {}
            for c in classify:
                dic = {'q_period': c["q_period"]}
                ary.append(dic)
        #print(ary)
        return HttpResponseJson(ary)
    # 作ったテストをデータベースにアップする
    def ajax_testupdateperiod(request):
        securecheck(request)
        u_id = request.session['u_id']
        if '@' in u_id:
            user = User.objects.get(u_email=u_id)
        else:
            user = User.objects.get(u_id=u_id)

        o_id = user.o_id

        num = LittleTest.objects.filter(o_id=o_id).values('t_id').distinct()

        numlist=[]
        for n in num:
            numlist.append( int(n['t_id']) )

        if len( numlist ) == 0:
            t_id = '0001'
        else:
            t_id = code4(max(numlist) + 1)

        #print( t_id )
        test_dic = byteToDic(request.body)
        q_list = test_dic['q_list']
        t_date = datetime.datetime.now()
        for item in q_list:
            #print(item)
            t_num = item['t_num']
            t_key = o_id + t_id + t_num
            q_id = item['q_id']
            l_test = LittleTest(t_key=t_key, t_id=t_id, t_num=t_num, t_date=t_date, o_id=o_id, q_id=q_id)
            l_test.save()

        m_test = MakeLittletest(m_key="%s%s" % (o_id, t_id), o_id=o_id, t_id=t_id, u_id=u_id)
        m_test.save()

        return HttpResponse(json.dumps({"state": "ok"}, ensure_ascii=False, indent=2), content_type='application/json',charset='utf-8')
#午後問題表示
class Question_Js():
    # ページ表示
    def questionjs( request ):
        #セッションを持っていない
        if 'u_id' not in request.session:
            return render( request,'exam/errorpage.html',{'message':'不正なアクセスです'})

        subjects = [{'key':'01','name':'基本スキル'},{'key':'02','name':'プログラミングスキル'},{'key':'03','name':'システムデザインスキル'}]
        u_admin = request.session['u_admin']
        m_titles = QuestionJs.objects.filter(q_subject='01').values('q_num','q_title').distinct()
        titles = []
        for title in m_titles:
            titles.append({'q_num':title['q_num'] , 'q_title':title['q_title']})
        m_contents = QuestionJs.objects.filter(q_subject='01',q_num='01').values('q_id','q_period','q_subject','q_num','q_content').distinct()
        contents = []
        for content in m_contents:
            contents.append( {'q_id':content['q_id'],'filename':"%s_%s_%s.pdf"%(content['q_period'],content['q_subject'],content['q_num']),'q_content':content['q_content']})

        return render( request,'exam/questionjs.html',{'u_admin':u_admin ,'subjects':subjects , 'titles':titles,'contents':contents})
    #ajax
    def ajax_gettitle( request ):
        c_dic = byteToDic(request.body)
        q_subject = c_dic['subject']
        print( q_subject )
        m_titles = QuestionJs.objects.filter(q_subject=q_subject).values('q_num','q_title').distinct()
        titles = []
        for title in m_titles:
            titles.append({'q_num':title['q_num'],'q_title':title['q_title']})
        print( titles )
        return HttpResponseJson(titles)

    def ajax_getquestionjs(request):
        c_dic = byteToDic(request.body)
        subject = c_dic['subject']
        title = c_dic['title']
        m_contents = QuestionJs.objects.filter(q_subject=subject,q_num=title).values('q_id','q_period','q_subject','q_num','q_content').distinct()
        contents = []
        for content in m_contents:
            contents.append( {'q_id':content['q_id'],'filename':"%s_%s_%s.pdf"%(content['q_period'],content['q_subject'],content['q_num']),'q_content':content['q_content']})
        print( contents )
        return HttpResponseJson(contents)

#午後問題表示
class Question_Pm():
    # ページ表示
    def questionpm( request ):
        #セッションを持っていない
        if 'u_id' not in request.session:
            return render( request,'exam/errorpage.html',{'message':'不正なアクセスです'})

        tests = {'fe':'基本情報','ap':'応報情報','sc':'情報セキュリティ'}
        u_admin = request.session['u_admin']
        qpm = QuestionPm.objects.filter(q_test='fe').values('q_classify').distinct().order_by('q_classify')
        test = QuestionPm.objects.values('q_test').distinct()
        testlist = []
        for t in test:
            dict={'test':t['q_test'],'name':tests[t['q_test']]}
            testlist.append( dict )
        classifylist = []
        for c in qpm:
            dict={'classify':c['q_classify']}
            classifylist.append(dict)

        qpm = QuestionPm.objects.filter(q_classify='01セキュリティ',q_test='fe').values()
        q_list = []
        static_dir = settings.STATIC_ROOT
        for q in qpm:
            qfn = q['q_test'] + "_" + q['q_period'] + "_" + q['q_classify'] + "_" + q['q_title'] + ".pdf"
            afn = q['q_test'] + "_" + q['q_period'] + "_" + q['q_classify'] + "_" + "ans.pdf"
            dict = {}
            dict['qfn'] = qfn
            afn_path = os.path.join(static_dir, 'exam', 'pdf', 'question_pm', afn)
            print(afn_path)
            if (os.path.exists(afn_path)):
                dict['afn'] = afn
            else:
                dict['afn'] = "ファイルなし"
            q_list.append(dict)

        return render( request,'exam/questionpm.html',{'classify':classifylist,'u_admin':u_admin ,'test':testlist,'question':q_list})
    #ajax
    def ajax_getquestionpm(request):
        c_dic = byteToDic(request.body)
        classify = c_dic['classify']
        test = c_dic['test']
        qpm = QuestionPm.objects.filter(q_classify=classify,q_test=test).values()
        q_list = []
        static_dir = settings.STATIC_ROOT
        for q in qpm:
            qfn = q['q_test'] + "_" + q['q_period'] + "_" + q['q_classify'] + "_" + q['q_title'] + ".pdf"
            afn = q['q_test'] + "_" + q['q_period'] + "_" + q['q_classify'] + "_" + "ans.pdf"
            dict = {}
            dict['qfn'] = qfn
            afn_path = os.path.join(static_dir, 'exam', 'pdf', 'question_pm', afn)
            print(afn_path)
            if (os.path.exists(afn_path)):
                dict['afn'] = afn
            else:
                dict['afn'] = "ファイルなし"
            q_list.append(dict)

        return HttpResponseJson({'q_list': q_list})

#サイト管理者ログイン
class SaLogin():
    def salogin( request ):
        return render( request,'exam/salogin.html')

#サイト管理者ページ
class SaPage():
    def sapage( request ):
        #u_idやパスワードを持っていない
        if request.method != "POST" and 'sa_id' not in request.session:
            return render( request,'exam/errorpage.html',{'message':'不正なアクセスです。'})

        if "POST" in request.method:
            u_id = request.POST['u_id']
            u_pass = request.POST['u_pass']
            request.session['sa_id'] = u_id

        #if "sa_id" in request.session:
        #    u_id = request.session['sa_id']
        #    return render(request, 'exam/sapage.html')

        #u_idが存在するか
        try:
            s_user = SuperUser.objects.get(u_id=u_id)
        except ObjectDoesNotExist:
            addAccessLog(request,'sapage','f')
            return render(request, 'exam/salogin.html', {'message': 'ユーザID、パスワードのいずれかが違います。'})

        #ブルートフォースチェック
        if checkBruteforce(u_id,'sapage'):
            return render(request, 'exam/errorpage.html', {'message': '不正なアクセスです。'})

        if s_user.u_pass == u_pass:
            addAccessLog(request, 'sapage','s')
            return render( request,'exam/sapage.html')

        addAccessLog(request, 'sapage', 'f')
        return render( request, 'exam/errorpage.html',{'message','ログインできません。'})

#スーパーユーザがライセンス追加を許可する
class SaAddlicense():
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
class SaAddlicenseFilter():
    def saaddlicense_filter( request ):
        dic = byteToDic( request.body )

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
class SaAddlicenseConf():
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
class UserRegisterCsv():
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
class UserRegisterWeb():
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

class QuestioinAmUpload():
    def question_am_upload( request ):
        securecheck(request)
        u_admin = request.session['u_admin']

        # リクエストにfileが含まれている
        if 'file' in request.FILES:
            # アップするファイルのパス
            o_id = request.session['o_id']
            media_path = os.path.join(settings.STATIC_ROOT, "exam", "image", "question")

            upfiles = request.FILES.getlist('file')

            # 複数のファイルがアップロードされる
            filelist = []
            for uf in upfiles:
                filepath = os.path.join(media_path, uf.name)
                dest = open(filepath, 'wb+')
                #print( filepath )
                for chunk in uf:
                    dest.write(chunk)
                filelist.append( uf.name )
            return render(request, 'exam/question_am_upload.html',{'u_admin':u_admin,'filelist':filelist} )

        return render( request, 'exam/question_am_upload.html',{'u_admin':u_admin} )

    def ajax_question_am_upload( request ):
        return HttpResponseJson( {} )

#-*-*-*-*-*-*-*-*-ajaxの応答-*-*-*-*-*-*-*-*-*-

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
