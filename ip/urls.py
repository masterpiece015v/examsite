from django.conf.urls import url
from django.contrib import admin
from . import views

app_name = "ip"

urlpatterns = [
    url(r'^mainpage/$', views.MainPage.mainpage, name="mainpage"),
    url(r'^ip_field/$',views.Ip_Field.ip_field,name="ip_field"),
    url(r'^ajax_ip_l_field_change/$',views.Ip_Field.ajax_ip_l_field_change,name="ajax_ip_l_field_change"),
    url(r'^ajax_ip_m_field_change/$',views.Ip_Field.ajax_ip_m_field_change,name="ajax_ip_m_field_change"),
    url(r'^ajax_ip_s_field_change/$',views.Ip_Field.ajax_ip_s_field_change,name="ajax_ip_s_field_change"),

]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
