from django.conf.urls import url
from django.contrib import admin
from . import views

app_name = "exam"

urlpatterns = [
    url(r'^$',views.index , name="index" ),
    url(r'^admin/',admin.site.urls),
    url(r'^answerupload/$',views.answerupload,name='answerupload'),
    url(r'^ajax_answerupload/$',views.ajax_answerupload,name='ajax_answerupload'),
    url(r'^ajax_getquestion_period/$',views.ajax_getquestion_period,name='ajax_getquestion_period'),
    url(r'^ajax_getquestion_classify/$', views.ajax_getquestion_classify, name='ajax_getquestion_classify'),
    url(r'^analysis', views.analysis,name='analysis'),
    url(r'^a_all', views.a_all ,name='a_all'),
    url(r'^a_bunya', views.a_bunya ,name='a_bunya'),
    url(r'^answersheetprint/$', views.answersheetprint, name='answersheetprint'),
    url(r'^answersheetprint_conf/$', views.answersheetprint_conf, name='answersheetprint_conf'),
    url(r'^addlicense/$', views.addlicense, name='addlicense'),
    url(r'^addlicense_conf/$', views.addlicense_conf, name='addlicense_conf'),
    url(r'^getclass/$', views.getclass, name='getclass'),
    url(r'^getperiod/$', views.getperiod, name='getperiod'),
    url(r'^getquestion/$', views.getquestion, name='getquestion'),
    url(r'^gettestprint/$', views.gettestprint, name='gettestprint'),
    url(r'^getresult/$', views.getresult, name='getresult'),
    url(r'^get_result_bunya/$',views.get_result_bunya,name='get_result_bunya'),
    url(r'^get_m_list',views.get_m_list,name='get_m_list'),
    url(r'^get_s_list',views.get_m_list,name='get_m_list'),
    url(r'^get_test_id_list',views.get_test_id_list,name='get_test_id_list'),
    url(r'^get_test_id_result',views.get_test_id_result,name='get_test_id_result'),
    url(r'^gettid/$', views.gettid, name='gettid'),
    url(r'^inquiry/$', views.inquiry, name='inquiry'),
    url(r'^logoff/$',views.logoff,name="logoff"),
    url(r'^mainpage/$', views.mainpage, name='mainpage'),
    url(r'^newuser/$', views.newuser, name='newuser'),
    url(r'^orgregister/$',views.orgregister,name='orgregister'),
    url(r'^passchange/$',views.passchange,name='passchange'),
    url(r'^passchange_finish',views.passchange_finish,name='passchange_finish'),
    url(r'^testmake/$',views.testmake,name='testmake'),
    url(r'^testmakeperiod/$',views.testmakeperiod,name='testmakeperiod'),
    url(r'^testprint/$',views.testprint,name='testprint'),
    url(r'^testupdate/$',views.testupdate,name='testupdate'),
    url(r'^userregistercsv/$', views.userregistercsv, name='userregistercsv'),
    url(r'^userregisterweb/$', views.userregisterweb, name='userregisterweb'),
    url(r'^salogin/$',views.salogin,name='salogin'),
    url(r'^sapage/$',views.sapage,name='sapage'),
    url(r'^saaddlicense/$',views.saaddlicense,name='saaddlicense'),
    url(r'^saaddlicense_filter/$',views.saaddlicense_filter,name='saaddlicense_filter'),
    url(r'^saaddlicense_conf/$',views.saaddlicense_conf,name='saaddlicense_conf'),
    url(r'^questionpm/$',views.questionpm,name='questionpm'),
    url(r'^ajax_getquestionpm/$',views.ajax_getquestionpm,name='ajax_questionpm'),
    url(r'^question_am_upload/$',views.question_am_upload,name='question_am_upload'),
    url(r'^ajax_question_am_upload/$',views.question_am_upload,name='ajax_question_am_upload'),
    url(r'^miss_question/$',views.miss_question,name='miss_question'),
    url(r'^ajax_miss_question/$',views.ajax_miss_question,name='ajax_miss_question'),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
