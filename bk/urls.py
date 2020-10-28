from django.conf.urls import url
from django.contrib import admin
from . import views

app_name = "bk"

urlpatterns = [
    #url(r'^$',views.Index.index , name="index" ),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
