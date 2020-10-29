from django.conf.urls import url
from django.contrib import admin
from . import views

app_name = "jg"

urlpatterns = [
    #url(r'^$',views.Index.index , name="index" ),
    url(r'^mainpage/$',views.MainPage.mainpage,name="mainpage"),
    url(r'^mainpage_ajax_getperiod/$', views.MainPage.mainpage_ajax_getperiod, name='mainpage_ajax_getperiod'),
    url(r'^ajax_getquestion_period/$', views.MainPage.ajax_getquestion_period, name='ajax_getquestion_period'),
    url(r'^ajax_getquestion_classify/$', views.MainPage.ajax_getquestion_classify, name='ajax_getquestion_classify'),

    # TestMake　テストを作る
    url(r'^testmake/$', views.TestMake.testmake, name='testmake'),
    url(r'^ajax_getclass/$', views.TestMake.ajax_getclass, name='ajax_getclass'),
    url(r'^ajax_getquestion/$', views.TestMake.ajax_getquestion, name='ajax_getquestion'),
    url(r'^ajax_testupdate/$', views.TestMake.ajax_testupdate, name='ajax_testupdate'),

    # TestMakePeriod　年度期ごとにテストを作る
    url(r'^testmakeperiod/$', views.TestMakePeriod.testmakeperiod, name='testmakeperiod'),
    url(r'^ajax_getperiod/$', views.TestMakePeriod.ajax_getperiod, name='ajax_getperiod'),
    url(r'^ajax_testupdateperiod/$', views.TestMakePeriod.ajax_testupdateperiod, name='ajax_testupdateperiod'),

    # TestDelete テストを削除する
    url(r'^testdelete/$', views.TestDelete.testdelete, name='testdelete'),
    url(r'^ajax_testdelete/$', views.TestDelete.ajax_testdelete, name='ajax_testdelete'),

    # TestPrint　テストを印刷する
    url(r'^testprint/$', views.TestPrint.testprint, name='testprint'),
    url(r'^ajax_gettestprint/$', views.TestPrint.ajax_gettestprint, name='ajax_gettestprint'),

    # AnswerUpload 解答用紙アップロード
    url(r'^answerupload/$', views.AnswerUpload.answerupload, name='answerupload'),
    url(r'^ajax_answerupload/$', views.AnswerUpload.ajax_answerupload, name='ajax_answerupload'),
    url(r'^ajax_answerinsert/$', views.AnswerUpload.ajax_answerinsert, name='ajax_answerinsert'),
    url(r'^ajax_answerallinsert/$', views.AnswerUpload.ajax_answerallinsert, name='ajax_answerallinsert'),
    url(r'^ajax_getanswerlist/$', views.AnswerUpload.ajax_getanswerlist, name='ajax_getanswerlist'),

    # AnswerSheetPrint 解答用紙印刷
    url(r'^answersheetprint/$', views.AnswerSheetPrint.answersheetprint, name='answersheetprint'),
    url(r'^ajax_answersheetprint/$', views.AnswerSheetPrint.ajax_answersheetprint, name='ajax_answersheetprint'),

    # TrainPrint
    url(r'^trainprint/$', views.TrainPrint.trainprint, name='trainprint'),
    url(r'^ajax_gettrainprint/$', views.TrainPrint.ajax_gettrainprint, name='ajax_gettrainprint'),
    url(r'^ajax_testchange/$', views.TrainPrint.ajax_testchange, name='ajax_testchange'),
    url(r'^ajax_m_id_change/$', views.TrainPrint.ajax_m_id_change, name='ajax_m_id_change'),
    url(r'^ajax_s_id_change/$', views.TrainPrint.ajax_s_id_change, name='ajax_s_id_change'),
    url(r'^get_m_list', views.get_m_list, name='get_m_list'),
    url(r'^get_s_list', views.get_m_list, name='get_m_list'),

    # Analysis テストNOごとに結果分析
    url(r'^analysis', views.Analysis.analysis, name='analysis'),
    url(r'^ajax_gettid/$', views.Analysis.ajax_gettid, name='ajax_gettid'),
    url(r'^ajax_getresult/$', views.Analysis.ajax_getresult, name='ajax_getresult'),

    # A_Bunya　分野ごとのテスト結果
    url(r'^a_bunya', views.A_Bunya.a_bunya, name='a_bunya'),
    url(r'^ajax_getresultbunya/$', views.A_Bunya.ajax_getresultbunya, name='ajax_getresultbunya'),

    # A_All　すべてのテスト結果
    url(r'^a_all', views.A_All.a_all, name='a_all'),
    url(r'^ajax_gettestidlist', views.A_All.ajax_gettestidlist, name='ajax_gettestidlist'),
    url(r'^ajax_gettestidresult', views.A_All.ajax_gettestidresult, name='ajax_gettestidresult'),

    # Miss_Question　間違った問題のみ印刷
    url(r'^miss_question/$', views.Miss_Question.miss_question, name='miss_question'),
    url(r'^ajax_miss_question/$', views.Miss_Question.ajax_miss_question, name='ajax_miss_question'),

    # Question_Pm　午後問題
    url(r'^questionpm/$', views.Question_Pm.questionpm, name='questionpm'),
    url(r'^ajax_getquestionpm/$', views.Question_Pm.ajax_getquestionpm, name='ajax_questionpm'),

    # cbt
    url(r'^cbtammain/$', views.CbtAmMain.cbtammain, name='cbtammain'),
    url(r'^cbtpmmain/$', views.CbtPmMain.cbtpmmain, name='cbtpmmain'),
    url(r'^cbtpm/$', views.CbtPm.cbtpm, name='cbtpm'),
    url(r'^cbtpmresult/$', views.CbtPmResult.cbtpmresult, name='cbtpmresult'),
    url(r'^cbtpmresultshow/$', views.CbtPmResultShow.cbtpmresultshow, name='cbtpmresultshow'),
    url(r'^ajax_cbtpm_update/$', views.CbtPm.ajax_cbtpm_update, name='ajax_cbtpm_update'),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
