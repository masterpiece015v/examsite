from django.conf.urls import url
from django.contrib import admin
from . import views

app_name = "bk"

urlpatterns = [
    #url(r'^$',views.Index.index , name="index" ),
    url(r'^$',views.Mainpage.mainpage,name="mainpage"),
    url(r'^n21/$',views.N21.n21 , name="n21" ),
    url(r'^ajax_n21_gettimes/$', views.N21.ajax_n21_gettimes, name="ajax_n21_gettimes"),
    url(r'^ajax_n21_getquestion/$',views.N21.ajax_n21_getquestion,name="ajax_n21_getquestion"),

    url(r'^n22/$', views.N22.n22, name="n22"),
    url(r'^ajax_n22_gettimes/$', views.N22.ajax_n22_gettimes, name="ajax_n22_gettimes"),
    url(r'^ajax_n22_getquestion/$', views.N22.ajax_n22_getquestion, name="ajax_n22_getquestion"),

    url(r'^n23/$', views.N23.n23, name="n23"),
    url(r'^ajax_n23_gettimes/$', views.N23.ajax_n23_gettimes, name="ajax_n23_gettimes"),
    url(r'^ajax_n23_getquestion/$', views.N23.ajax_n23_getquestion, name="ajax_n23_getquestion"),

    url(r'^n24/$', views.N24.n24, name="n24"),
    url(r'^ajax_n24_gettimes/$', views.N24.ajax_n24_gettimes, name="ajax_n24_gettimes"),
    url(r'^ajax_n24_getquestion/$', views.N24.ajax_n24_getquestion, name="ajax_n24_getquestion"),

    url(r'^n25/$', views.N25.n25, name="n25"),
    url(r'^ajax_n25_gettimes/$', views.N25.ajax_n25_gettimes, name="ajax_n25_gettimes"),
    url(r'^ajax_n25_getquestion/$', views.N25.ajax_n25_getquestion, name="ajax_n25_getquestion"),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
