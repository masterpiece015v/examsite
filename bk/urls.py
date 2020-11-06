from django.conf.urls import url
from django.contrib import admin
from . import views

app_name = "bk"

urlpatterns = [
    #url(r'^$',views.Index.index , name="index" ),
    url(r'^$',views.Mainpage.mainpage,name="mainpage"),
    url(r'^n21/$',views.N21.n21 , name="n21" ),
    url(r'^ajax_n21_getquestion/$',views.N21.ajax_n21_getquestion,name="ajax_n21_getquestion"),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
