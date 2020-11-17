from django.shortcuts import render
from exam.models import *
import json,ast
from django.http import HttpResponse
import re,string,random,datetime,os,csv
from django.conf import settings

#ajaxのPOSTデータをDictionaryに変換する
def byteToDic( data ):
    return ast.literal_eval( data.decode() )
#HttpResponseのJSON
def HttpResponseJson( jsonobj ):
    jsonStr = json.dumps( jsonobj , ensure_ascii=False, indent=2)
    return HttpResponse(jsonStr, content_type='application/json', charset='utf-8')

# 問題作成メイン画面
class Mainpage():
    def mainpage(request):

        return render( request,'bk/mainpage.html',{'u_admin':request.session['u_admin']})

#テスト印刷画面
class N21():
    #ページを表示する
    def n21( request ):
        user = request.session['u_id']
        o_id = request.session['o_id']

        field_list = []
        qb = QuestionBoki.objects.filter(b_que1='1').values('b_field').distinct()
        for q in qb:
            field_list.append( q['b_field'] )

        return render( request,'bk/n21.html',{'field_list':field_list,'u_admin':request.session['u_admin']})

    #回を取得する
    def ajax_n21_gettimes(request):
        body = byteToDic( request.body )
        o_id = request.session['o_id']
        b_field = body['b_field']
        print(b_field)
        qb = QuestionBoki.objects.filter(b_field=b_field,b_que1='1').values('b_times','b_que2','b_ocr').distinct().order_by('b_times').reverse()
        #print( qb )
        data = {'qlist':[]}
        for q in qb:
            dic = {}
            dic['b_times'] = q['b_times']
            dic['b_que2'] = q['b_que2']
            dic['b_ocr'] = q['b_ocr'][0:100]
            data['qlist'].append( dic )

        #print( data )
        return HttpResponseJson( data )

    #テストの印刷用データをajaxで取得する
    def ajax_n21_getquestion( request ):
        body = byteToDic( request.body )
        o_id = request.session['o_id']
        b_times = body['b_times']
        b_field = body['b_field']
        data = {'qlist':[]}
        for b in b_times:
            bt = b.split("_")[0]
            bq2 = b.split("_")[2]

            q = QuestionBoki.objects.filter(b_times=bt,b_que1='1',b_que2=bq2).values().first()
            dic2 = {}
            dic2['b_id'] = q['b_id']
            dic2['b_times'] = q['b_times']
            dic2['b_que1'] = q['b_que1']
            dic2['b_que2'] = q['b_que2']

            data['qlist'].append( dic2 )
        qbaf = QuestionBokiQ1AllowField.objects.filter(b_field=b_field).values().first()
        q1allow = qbaf['b_allow_field']
        if q1allow is not None:
            data['b_allow_field'] = q1allow.split(',')
        else:
            data['b_allow_field'] = ''

        print( data )
        return HttpResponseJson( data )

#テスト印刷画面
class N22():
    #ページを表示する
    def n22( request ):
        user = request.session['u_id']
        o_id = request.session['o_id']

        field_list = []
        qb = QuestionBoki.objects.filter(b_que1='2').values('b_field').distinct()
        for q in qb:
            field_list.append( q['b_field'] )

        return render( request,'bk/n22.html',{'field_list':field_list,'u_admin':request.session['u_admin']})
    #回を取得する
    def ajax_n22_gettimes(request):
        body = byteToDic( request.body )
        o_id = request.session['o_id']
        b_field = body['b_field']
        qb = QuestionBoki.objects.filter(b_field=b_field,b_que1='2').values('b_times','b_ocr').distinct().order_by('b_times').reverse()
        print( qb )
        data = {'qlist':[]}
        for q in qb:
            dic = {}
            dic['b_times'] = q['b_times']
            dic['b_ocr'] = q['b_ocr'][0:100]
            data['qlist'].append( dic )

        print( data )
        return HttpResponseJson( data )

    #テストの印刷用データをajaxで取得する
    def ajax_n22_getquestion( request ):
        body = byteToDic( request.body )
        o_id = request.session['o_id']
        b_times = body['b_times']
        data = {'qlist':[]}
        for b in b_times:
            qb = QuestionBoki.objects.filter(b_times=b,b_que1='2').values()
            dic1 = {'b_times':b,'list':[]}
            for q in qb:
                dic2 = {}
                dic2['b_id'] = q['b_id']
                dic2['b_times'] = q['b_times']
                dic2['b_que1'] = q['b_que1']
                dic2['b_que2'] = q['b_que2']
                dic2['b_ans_page'] = q['b_ans_page']
                dic2['b_as_page'] = q['b_as_page']
                dic2['b_com_page'] = q['b_com_page']
                dic1['list'].append( dic2 )
            data['qlist'].append( dic1 )

        print( data )
        return HttpResponseJson( data )

#テスト印刷画面
class N23():
    #ページを表示する
    def n23( request ):
        user = request.session['u_id']
        o_id = request.session['o_id']

        field_list = []
        qb = QuestionBoki.objects.filter(b_que1='3').values('b_field').distinct()
        for q in qb:
            field_list.append( q['b_field'] )

        return render( request,'bk/n23.html',{'field_list':field_list,'u_admin':request.session['u_admin']})
    #回を取得する
    def ajax_n23_gettimes(request):
        body = byteToDic( request.body )
        o_id = request.session['o_id']
        b_field = body['b_field']
        print( b_field )
        qb = QuestionBoki.objects.filter(b_field=b_field,b_que1='3').values('b_times','b_ocr','b_que2').distinct().order_by('-b_times','b_que2')
        print( qb )
        data = {'qlist':[]}
        
        for q in qb:
            if q['b_que2'] == '1':
                dic = {}
                dic['b_times'] = q['b_times']
                dic['b_ocr'] = q['b_ocr'][0:100]
                data['qlist'].append( dic )

        print( data )
        return HttpResponseJson( data )

    #テストの印刷用データをajaxで取得する
    def ajax_n23_getquestion( request ):
        body = byteToDic( request.body )
        o_id = request.session['o_id']
        b_times = body['b_times']
        data = {'qlist':[]}
        for b in b_times:
            qb = QuestionBoki.objects.filter(b_times=b,b_que1='3').values()
            dic1 = {'b_times':b,'list':[]}
            for q in qb:
                dic2 = {}
                dic2['b_id'] = q['b_id']
                dic2['b_times'] = q['b_times']
                dic2['b_que1'] = q['b_que1']
                dic2['b_que2'] = q['b_que2']
                dic2['b_ans_page'] = q['b_ans_page']
                dic2['b_as_page'] = q['b_as_page']
                dic2['b_com_page'] = q['b_com_page']
                dic1['list'].append( dic2 )
            data['qlist'].append( dic1 )

        print( data )
        return HttpResponseJson( data )


#テスト印刷画面
class N24():
    #ページを表示する
    def n24( request ):
        user = request.session['u_id']
        o_id = request.session['o_id']

        field_list = []
        qb = QuestionBoki.objects.filter(b_que1='4').values('b_field').distinct()
        for q in qb:
            field_list.append( q['b_field'] )

        return render( request,'bk/n24.html',{'field_list':field_list,'u_admin':request.session['u_admin']})
    #回を取得する
    def ajax_n24_gettimes(request):
        body = byteToDic( request.body )
        o_id = request.session['o_id']
        b_field = body['b_field']
        qb = QuestionBoki.objects.filter(b_field=b_field,b_que1='4').values('b_times','b_ocr').distinct().order_by('b_times').reverse()
        print( qb )
        data = {'qlist':[]}
        for q in qb:
            dic = {}
            dic['b_times'] = q['b_times']
            dic['b_ocr'] = q['b_ocr'][0:100]
            data['qlist'].append( dic )

        print( data )
        return HttpResponseJson( data )

    #テストの印刷用データをajaxで取得する
    def ajax_n24_getquestion( request ):
        body = byteToDic( request.body )
        o_id = request.session['o_id']
        b_times = body['b_times']
        data = {'qlist':[]}
        for b in b_times:
            qb = QuestionBoki.objects.filter(b_times=b,b_que1='4').values()
            dic1 = {'b_times':b,'list':[]}
            for q in qb:
                dic2 = {}
                dic2['b_id'] = q['b_id']
                dic2['b_times'] = q['b_times']
                dic2['b_que1'] = q['b_que1']
                dic2['b_que2'] = q['b_que2']
                dic2['b_ans_page'] = q['b_ans_page']
                dic2['b_as_page'] = q['b_as_page']
                dic2['b_com_page'] = q['b_com_page']
                dic1['list'].append( dic2 )
            data['qlist'].append( dic1 )

        print( data )
        return HttpResponseJson( data )

#テスト印刷画面
class N25():
    #ページを表示する
    def n25( request ):
        user = request.session['u_id']
        o_id = request.session['o_id']

        field_list = []
        qb = QuestionBoki.objects.filter(b_que1='5').values('b_field').distinct()
        for q in qb:
            field_list.append( q['b_field'] )

        return render( request,'bk/n25.html',{'field_list':field_list,'u_admin':request.session['u_admin']})
    #回を取得する
    def ajax_n25_gettimes(request):
        body = byteToDic( request.body )
        o_id = request.session['o_id']
        b_field = body['b_field']
        qb = QuestionBoki.objects.filter(b_field=b_field,b_que1='5').values('b_times','b_ocr').distinct().order_by('b_times').reverse()
        print( qb )
        data = {'qlist':[]}
        for q in qb:
            dic = {}
            dic['b_times'] = q['b_times']
            dic['b_ocr'] = q['b_ocr'][0:100]
            data['qlist'].append( dic )

        print( data )
        return HttpResponseJson( data )

    #テストの印刷用データをajaxで取得する
    def ajax_n25_getquestion( request ):
        body = byteToDic( request.body )
        o_id = request.session['o_id']
        b_times = body['b_times']
        data = {'qlist':[]}
        for b in b_times:
            qb = QuestionBoki.objects.filter(b_times=b,b_que1='5').values()
            dic1 = {'b_times':b,'list':[]}
            for q in qb:
                dic2 = {}
                dic2['b_id'] = q['b_id']
                dic2['b_times'] = q['b_times']
                dic2['b_que1'] = q['b_que1']
                dic2['b_que2'] = q['b_que2']
                dic2['b_ans_page'] = q['b_ans_page']
                dic2['b_as_page'] = q['b_as_page']
                dic2['b_com_page'] = q['b_com_page']
                dic1['list'].append( dic2 )
            data['qlist'].append( dic1 )

        print( data )
        return HttpResponseJson( data )
