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
import json,ast
from django.conf import settings
from .logger import log_write

#関数
#ajaxのPOSTデータをDictionaryに変換する
def byteToDic( data ):
    return ast.literal_eval( data.decode() )
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
        # セッションIDがある(戻るボタンなどで帰ってきたとき用)
        if 'u_id' in request.session:
            if request.session['u_id'] != "":
                u_id = request.session['u_id']
                try:
                    user = User.objects.get(pk=u_id)
                except:
                    return render(request, 'exam/errorpage.html', {'message': '不正なアクセスです:code1'})
                # request.session['u_id'] = u_id
                u_name = user.u_name
                u_admin = user.u_admin
                request.session['u_admin'] = u_admin
                return render(request, 'exam/mainpage.html',{'u_id': u_id, 'u_name': u_name, 'u_admin': u_admin})

        # u_idやパスワードを持っていない
        if request.method != "POST":
            return render(request, 'exam/errorpage.html', {'message': '不正なアクセスです:code2'})

        u_id = request.POST["u_id"]
        u_pass = request.POST["u_pass"]
        ipa = request.environ['REMOTE_ADDR']  # IP-Address

        # アカウントが有効かをチェック
        try:
            print(u_id)
            user = User.objects.get(pk=u_id)
        except:
            return render(request, 'exam/errorpage.html', {'message': '不正なアクセスです:code3'})

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
            request.session['u_name'] = u_name

            return render(request, 'exam/mainpage.html',{'u_id': u_id, 'u_name': u_name, 'u_admin': u_admin} )
        else:
            addAccessLog(request, 'mainpage', 'f')
            return render(request, 'exam/index.html', {'message': 'ユーザID（メールアドレス）、パスワードのいずれかが違います。'})


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
                users.append({'u_id':row[0],'u_pass':row[1],'u_name':row[2],'u_email':row[3],'u_admin':row[4],'u_enable':row[5]})

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
                user = {'u_id':u_id,'u_name':u_name,'u_pass':u_pass,'u_email':u_email,'u_admin':u_admin,'u_enable':u_enable}
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
            #u_id = o_id + u_id
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