from django.shortcuts import render
from exam.models import *
import json,ast
from django.http import HttpResponse
import re,string,random,datetime,os,csv
from django.conf import settings
from exam.markreader import get_answer_list
# Create your views here.

#グローバル変数
testdic = {'fe':'基本情報','ap':'応用情報','sc':'情報セキュリティ'}

# RandomId
def random_id(n):
    randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
    return ''.join(randlst)

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
#ajaxのPOSTデータをDictionaryに変換する
def byteToDic( data ):
    return ast.literal_eval( data.decode() )
#HttpResponseのJSON
def HttpResponseJson( jsonobj ):
    jsonStr = json.dumps( jsonobj , ensure_ascii=False, indent=2)
    return HttpResponse(jsonStr, content_type='application/json', charset='utf-8')
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

#セッションにu_idを含むかをチェックする
def securecheck( request ):
    if 'u_id' not in request.session:
        return render( request,'exam/errorpage.html',{'message','不正なアクセスです。'})

# メインページ
class MainPage():
    def mainpage(request):
        u_id = request.session['u_id']
        u_admin = request.session['u_admin']
        o_id = request.session['o_id']
        u_name = request.session['u_name']

        return render(request, 'ip/mainpage.html',{'u_id': u_id, 'u_name': u_name, 'u_admin': u_admin})

class Ip_Field():
    def ip_field(request):
        u_id = request.session['u_id']
        u_admin = request.session['u_admin']
        o_id = request.session['o_id']
        u_name = request.session['u_name']

        ip_l_field = QuestionIp.objects.values('ip_l_field').distinct().order_by('ip_l_field')

        ip_l_fields = []
        for l in ip_l_field:
            dict = {'ip_l_field':l['ip_l_field']}
            ip_l_fields.append( dict )
            print( dict )
        return render(request,'ip/ip_field.html',{'list':ip_l_fields})

    #大分類を変更したときのajax
    def ajax_ip_l_field_change(request):

        c_dic = byteToDic(request.body)
        ip_l_field = c_dic['ip_l_field']

        ip_m_fields = QuestionIp.objects.filter(ip_l_field=ip_l_field).values('ip_m_field').distinct().order_by('ip_l_field','ip_m_field')
        questions = QuestionIp.objects.filter(ip_l_field=ip_l_field).values('ip_period','ip_num','ip_l_field','ip_m_field','ip_s_field','ip_id','ip_answer').distinct().order_by('ip_s_field','-ip_id')

        field_list = []
        for m in ip_m_fields:
            dict = {'ip_m_field':m['ip_m_field']}
            print( dict )
            field_list.append( dict )

        question_list = []
        for q in questions:
            dict = {'ip_id':q['ip_id'],'ip_period':q['ip_period'],'ip_num':q['ip_num'],'ip_l_field':q['ip_l_field'],'ip_m_field':q['ip_m_field'],'ip_s_field':q['ip_s_field'],'ip_answer':q['ip_answer']}
            print( dict )
            question_list.append( dict )

        return HttpResponseJson({'field_list':field_list,'question_list':question_list})

    #中分類を変更したときのajax
    def ajax_ip_m_field_change(request):

        c_dic = byteToDic(request.body)
        ip_l_field = c_dic['ip_l_field']
        ip_m_field = c_dic['ip_m_field']

        ip_s_fields = QuestionIp.objects.filter(ip_l_field=ip_l_field,ip_m_field=ip_m_field).values('ip_s_field').distinct().order_by('ip_s_field')
        questions = QuestionIp.objects.filter(ip_l_field=ip_l_field,ip_m_field=ip_m_field).values('ip_period','ip_num','ip_l_field','ip_m_field','ip_s_field','ip_id','ip_answer').distinct().order_by('ip_s_field','-ip_id')

        field_list = []
        for s in ip_s_fields:
            dict = {'ip_s_field':s['ip_s_field']}
            print( dict )
            field_list.append( dict )

        question_list = []
        for q in questions:
            dict = {'ip_id':q['ip_id'],'ip_period':q['ip_period'],'ip_num':q['ip_num'],'ip_l_field':q['ip_l_field'],'ip_m_field':q['ip_m_field'],'ip_s_field':q['ip_s_field'],'ip_answer':q['ip_answer']}
            print( dict )
            question_list.append( dict )

        return HttpResponseJson({'field_list':field_list,'question_list':question_list})

    #小分類を変更したときのajax
    def ajax_ip_s_field_change(request):

        c_dic = byteToDic(request.body)
        ip_s_field = c_dic['ip_s_field']
        print( ip_s_field )
        questions = QuestionIp.objects.filter(ip_s_field=ip_s_field).values('ip_period','ip_num','ip_l_field','ip_m_field','ip_s_field','ip_id','ip_answer').distinct().order_by('ip_s_field','-ip_id')

        question_list = []
        for q in questions:
            dict = {'ip_id':q['ip_id'],'ip_period':q['ip_period'],'ip_num':q['ip_num'],'ip_l_field':q['ip_l_field'],'ip_m_field':q['ip_m_field'],'ip_s_field':q['ip_s_field'],'ip_answer':q['ip_answer']}
            print( dict )
            question_list.append( dict )

        return HttpResponseJson({'question_list':question_list})