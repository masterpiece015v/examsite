from django.conf.urls import url
from django.contrib import admin
from . import views

app_name = "jk"

urlpatterns = [
    #url(r'^$',views.Index.index , name="index" ),
    # QuestionJs
    url(r'^questionjs/$', views.Question_Js.questionjs, name='questionjs'),
    url(r'^ajax_getquestionjs/$', views.Question_Js.ajax_getquestionjs, name='ajax_getquestionjs'),
    url(r'^ajax_gettitle/$', views.Question_Js.ajax_gettitle, name='ajax_gettitle'),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
