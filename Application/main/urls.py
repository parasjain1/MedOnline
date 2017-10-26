from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.app_login, name='login'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^profile.*', views.profile, name='profile'),
    url(r'^logout/$', views.app_logout, name='login'),


    url(r'^uploadProfileImage/$', views.uploadProfileImage, name='uploadProfileImage'),

]
