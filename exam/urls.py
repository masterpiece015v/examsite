from django.conf.urls import url
from django.contrib import admin
from . import views

app_name = "exam"

urlpatterns = [
    url(r'^$',views.index , name="index" ),
    url(r'^admin/',admin.site.urls),
    url(r'^answerupload/$',views.answerupload,name='answerupload'),
    url(r'^analysis', views.analysis,name='analysis'),
    url(r'^answersheetprint/$', views.answersheetprint, name='answersheetprint'),
    url(r'^answersheetprint_conf/$', views.answersheetprint_conf, name='answersheetprint_conf'),
    url(r'^addlicense/$', views.addlicense, name='addlicense'),
    url(r'^addlicense_conf/$', views.addlicense_conf, name='addlicense_conf'),
    url(r'^getclass/$', views.getclass, name='getclass'),
    url(r'^getperiod/$', views.getperiod, name='getperiod'),
    url(r'^getquestion/$', views.getquestion, name='getquestion'),
    url(r'^gettestprint/$', views.gettestprint, name='gettestprint'),
    url(r'^inquiry/$', views.inquiry, name='inquiry'),
    url(r'^logoff/$',views.logoff,name="logoff"),
    url(r'^mainpage/$', views.mainpage, name='mainpage'),
    url(r'^newuser/$', views.newuser, name='newuser'),
    url(r'^orgregister/$',views.orgregister,name='orgregister'),
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

]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
