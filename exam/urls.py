from django.conf.urls import url
from django.contrib import admin
from . import views

app_name = "exam"

urlpatterns = [
    url(r'^$',views.index , name="index" ),
    url(r'^admin/',admin.site.urls),
    # AnswerUpload 解答用紙アップロード
    url(r'^answerupload/$',views.AnswerUpload.answerupload,name='answerupload'),
    url(r'^ajax_answerupload/$',views.AnswerUpload.ajax_answerupload,name='ajax_answerupload'),
    # AnswerSheetPrint 解答用紙印刷
    url(r'^answersheetprint/$', views.AnswerSheetPrint.answersheetprint, name='answersheetprint'),
    url(r'^ajax_answersheetprint/$', views.AnswerSheetPrint.ajax_answersheetprint, name='ajax_answersheetprint'),
    # Analysis テストNOごとに結果分析
    url(r'^analysis', views.Analysis.analysis,name='analysis'),
    url(r'^ajax_gettid/$', views.Analysis.ajax_gettid, name='ajax_gettid'),
    url(r'^ajax_getresult/$', views.Analysis.ajax_getresult, name='ajax_getresult'),
    # A_All　すべてのテスト結果
    url(r'^a_all', views.A_All.a_all ,name='a_all'),
    url(r'^ajax_gettestidlist',views.A_All.ajax_gettestidlist,name='ajax_gettestidlist'),
    url(r'^ajax_gettestidresult',views.A_All.ajax_gettestidresult,name='ajax_gettestidresult'),
    # A_Bunya　分野ごとのテスト結果
    url(r'^a_bunya', views.A_Bunya.a_bunya ,name='a_bunya'),
    url(r'^ajax_getresultbunya/$',views.A_Bunya.ajax_getresultbunya,name='ajax_getresultbunya'),
    # Miss_Question　間違った問題のみ印刷
    url(r'^miss_question/$', views.Miss_Question.miss_question, name='miss_question'),
    url(r'^ajax_miss_question/$', views.Miss_Question.ajax_miss_question, name='ajax_miss_question'),
    # TestMake　テストを作る
    url(r'^testmake/$',views.TestMake.testmake,name='testmake'),
    url(r'^ajax_getclass/$', views.TestMake.ajax_getclass, name='ajax_getclass'),
    url(r'^ajax_getquestion/$', views.TestMake.ajax_getquestion, name='ajax_getquestion'),
    url(r'^ajax_testupdate/$', views.TestMake.ajax_testupdate, name='ajax_testupdate'),
    #TestPrint　テストを印刷する
    url(r'^testprint/$', views.TestPrint.testprint, name='testprint'),
    url(r'^ajax_gettestprint/$', views.TestPrint.ajax_gettestprint, name='ajax_gettestprint'),
    # Question_Pm　午後問題
    url(r'^questionpm/$', views.Question_Pm.questionpm, name='questionpm'),
    url(r'^ajax_getquestionpm/$', views.Question_Pm.ajax_getquestionpm, name='ajax_questionpm'),
    #TestMakePeriod　年度期ごとにテストを作る
    url(r'^testmakeperiod/$',views.TestMakePeriod.testmakeperiod,name='testmakeperiod'),
    url(r'^ajax_getperiod/$', views.TestMakePeriod.ajax_getperiod, name='ajax_getperiod'),
    url(r'^ajax_testupdateperiod/$', views.TestMakePeriod.ajax_testupdateperiod, name='ajax_testupdateperiod'),
    #TestDelete テストを削除する
    url(r'^testdelete/$', views.TestDelete.testdelete, name='testdelete'),
    url(r'^ajax_testdelete/$', views.TestDelete.ajax_testdelete, name='ajax_testdelete'),

    url(r'^ajax_getquestion_period/$',views.ajax_getquestion_period,name='ajax_getquestion_period'),
    url(r'^ajax_getquestion_classify/$', views.ajax_getquestion_classify, name='ajax_getquestion_classify'),
    url(r'^addlicense/$', views.addlicense, name='addlicense'),
    url(r'^addlicense_conf/$', views.addlicense_conf, name='addlicense_conf'),
    url(r'^get_m_list',views.get_m_list,name='get_m_list'),
    url(r'^get_s_list',views.get_m_list,name='get_m_list'),
    url(r'^inquiry/$', views.inquiry, name='inquiry'),
    url(r'^logoff/$',views.logoff,name="logoff"),
    url(r'^mainpage/$', views.mainpage, name='mainpage'),
    url(r'^newuser/$', views.newuser, name='newuser'),
    url(r'^orgregister/$',views.orgregister,name='orgregister'),
    url(r'^passchange/$',views.passchange,name='passchange'),
    url(r'^passchange_finish',views.passchange_finish,name='passchange_finish'),
    url(r'^userregistercsv/$', views.userregistercsv, name='userregistercsv'),
    url(r'^userregisterweb/$', views.userregisterweb, name='userregisterweb'),
    url(r'^salogin/$',views.salogin,name='salogin'),
    url(r'^sapage/$',views.sapage,name='sapage'),
    url(r'^saaddlicense/$',views.saaddlicense,name='saaddlicense'),
    url(r'^saaddlicense_filter/$',views.saaddlicense_filter,name='saaddlicense_filter'),
    url(r'^saaddlicense_conf/$',views.saaddlicense_conf,name='saaddlicense_conf'),
    url(r'^question_am_upload/$',views.question_am_upload,name='question_am_upload'),
    url(r'^ajax_question_am_upload/$',views.question_am_upload,name='ajax_question_am_upload'),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
