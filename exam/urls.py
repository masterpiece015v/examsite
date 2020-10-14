from django.conf.urls import url
from django.contrib import admin
from . import views

app_name = "exam"

urlpatterns = [
    url(r'^$',views.Index.index , name="index" ),
    url(r'^admin/',admin.site.urls),

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

    # Question_Pm　午後問題
    url(r'^questionpm/$', views.Question_Pm.questionpm, name='questionpm'),
    url(r'^ajax_getquestionpm/$', views.Question_Pm.ajax_getquestionpm, name='ajax_questionpm'),

    #MainPage メインページ
    url(r'^mainpage/$', views.MainPage.mainpage, name='mainpage'),
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
