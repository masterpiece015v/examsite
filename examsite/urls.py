from django.contrib import admin
from django.urls import include
from django.conf.urls import url

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^exam/',include( 'exam.urls')),
    url(r'^jg/', include('jg.urls')),
    url(r'^bk/', include('bk.urls')),
    url(r'^jk/', include('jk.urls')),
    url(r'^ip/',include('ip.urls')),
    url(r'^manager/',include('manager.urls')),
]