from django.conf.urls import url
from django.contrib import admin
from . import views

app_name = "exam"

urlpatterns = [
    url(r'^$',views.Index.index , name="index" ),
    url(r'^admin/',admin.site.urls),
    # AnswerUpload 解答用紙アップロード
    url(r'^answerupload/$',views.AnswerUpload.answerupload,name='answerupload'),
    url(r'^ajax_answerupload/$',views.AnswerUpload.ajax_answerupload,name='ajax_answerupload'),
    url(r'^ajax_answerinsert/$',views.AnswerUpload.ajax_answerinsert,name='ajax_answerinsert'),
    url(r'^ajax_answerallinsert/$',views.AnswerUpload.ajax_answerallinsert,name='ajax_answerallinsert'),
    url(r'^ajax_getanswerlist/$', views.AnswerUpload.ajax_getanswerlist, name='ajax_getanswerlist'),
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
    #MainPage メインページ
    url(r'^mainpage/$', views.MainPage.mainpage, name='mainpage'),
    url(r'^mainpage_ajax_getperiod/$', views.MainPage.mainpage_ajax_getperiod, name='mainpage_ajax_getperiod'),
    url(r'^ajax_getquestion_period/$', views.MainPage.ajax_getquestion_period, name='ajax_getquestion_period'),
    url(r'^ajax_getquestion_classify/$', views.MainPage.ajax_getquestion_classify, name='ajax_getquestion_classify'),
    #QuestionJs
    url(r'^questionjs/$', views.Question_Js.questionjs, name='questionjs'),
    url(r'^ajax_getquestionjs/$', views.Question_Js.ajax_getquestionjs, name='ajax_getquestionjs'),
    url(r'^ajax_gettitle/$', views.Question_Js.ajax_gettitle, name='ajax_gettitle'),
    # Addlicense
    url(r'^addlicense/$', views.Addlicense.addlicense, name='addlicense'),

    # AddlicenseConf
    url(r'^addlicense_conf/$', views.AddlicenseConf.addlicense_conf, name='addlicense_conf'),

    # Inquiry
    url(r'^inquiry/$', views.Inquiry.inquiry, name='inquiry'),

    # Logoff
    url(r'^logoff/$',views.Logoff.logoff,name="logoff"),

    # NewUser
    url(r'^newuser/$', views.NewUser.newuser, name='newuser'),

    # OrgRegister
    url(r'^orgregister/$',views.OrgRegister.orgregister,name='orgregister'),

    # PassChange
    url(r'^passchange/$',views.PassChange.passchange,name='passchange'),

    # PassChangeFinish
    url(r'^passchange_finish',views.PassChangeFinish.passchange_finish,name='passchange_finish'),

    # UserRegisterCsv
    url(r'^userregistercsv/$', views.UserRegisterCsv.userregistercsv, name='userregistercsv'),

    # UserRegisterWeb
    url(r'^userregisterweb/$', views.UserRegisterWeb.userregisterweb, name='userregisterweb'),

    # SaLogin
    url(r'^salogin/$',views.SaLogin.salogin,name='salogin'),

    # SaPage
    url(r'^sapage/$',views.SaPage.sapage,name='sapage'),

    # SaAddlicense
    url(r'^saaddlicense/$',views.SaAddlicense.saaddlicense,name='saaddlicense'),

    # SaAddlicenseFilter
    url(r'^saaddlicense_filter/$',views.SaAddlicenseFilter.saaddlicense_filter,name='saaddlicense_filter'),

    #SaAddlicenseConf
    url(r'^saaddlicense_conf/$',views.SaAddlicenseConf.saaddlicense_conf,name='saaddlicense_conf'),

    # QuestionAmUpLoad
    url(r'^question_am_upload/$',views.QuestioinAmUpload.question_am_upload,name='question_am_upload'),

    url(r'^cbtammain/$',views.CbtAmMain.cbtammain,name='cbtammain'),
    url(r'^cbtpmmain/$',views.CbtPmMain.cbtpmmain,name='cbtpmmain'),
    url(r'^cbtpm/$',views.CbtPm.cbtpm,name='cbtpm'),
    url(r'^ajax_cbtpm_get_q/$',views.CbtPm.ajax_cbtpm_get_q,name='ajax_cbtpm_get_q'),
    # TrainPrint
    url(r'^trainprint/$',views.TrainPrint.trainprint,name='trainprint'),
    url(r'^ajax_gettrainprint/$',views.TrainPrint.ajax_gettrainprint,name='ajax_gettrainprint'),
    url(r'^ajax_testchange/$',views.TrainPrint.ajax_testchange,name='ajax_testchange'),
    url(r'^ajax_m_id_change/$', views.TrainPrint.ajax_m_id_change, name='ajax_m_id_change'),
    url(r'^ajax_s_id_change/$', views.TrainPrint.ajax_s_id_change, name='ajax_s_id_change'),
    url(r'^get_m_list', views.get_m_list, name='get_m_list'),
    url(r'^get_s_list', views.get_m_list, name='get_m_list'),

]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
