from django.shortcuts import render
from exam.models import *
import json,ast
from django.http import HttpResponse
import re,string,random,datetime,os,csv
from django.conf import settings
from exam.markreader import get_answer_list

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

    #テストの印刷用データをajaxで取得する
    def ajax_n21_getquestion( request ):
        body = byteToDic( request.body )
        o_id = request.session['o_id']
        b_field = body['b_field']
        qb = QuestionBoki.objects.filter(b_field=b_field).values()
        data = {'qlist':[]}
        for q in qb:
            dic = {}
            dic['b_id'] = q['b_id']
            dic['b_times'] = q['b_times']
            dic['b_que1'] = q['b_que1']
            dic['b_que2'] = q['b_que2']
            data['qlist'].append( dic )

        return HttpResponseJson( data )
