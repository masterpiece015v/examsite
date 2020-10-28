from django.conf.urls import url
from django.contrib import admin
from . import views

app_name = "exam"

urlpatterns = [
    url(r'^$',views.Index.index , name="index" ),
    url(r'^admin/',admin.site.urls),
    #MainPage メインページ
    url(r'^mainpage/$', views.MainPage.mainpage, name='mainpage'),
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

]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
