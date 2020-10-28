from django.shortcuts import render
from exam.models import *
import json,ast
from django.http import HttpResponse
import re,string,random,datetime,os,csv
from django.conf import settings
from exam.markreader import get_answer_list

# Create your views here.

#ajaxのPOSTデータをDictionaryに変換する
def byteToDic( data ):
    return ast.literal_eval( data.decode() )
#HttpResponseのJSON
def HttpResponseJson( jsonobj ):
    jsonStr = json.dumps( jsonobj , ensure_ascii=False, indent=2)
    return HttpResponse(jsonStr, content_type='application/json', charset='utf-8')
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

        return render( request,'jk/questionjs.html',{'u_admin':u_admin ,'subjects':subjects , 'titles':titles,'contents':contents})
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
