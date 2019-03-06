# chatapp/urls.py
from django.urls import path, re_path
from . import views, modalview


urlpatterns = [
	path('', views.mylogin, name='view-login'),
    path('index', views.index, name='view-index'),
    path('modalview', modalview.modal, name='view-modal'),
    path('logout', views.mylogout, name='view-logout'),
    path('logup', views.mylogup, name='view-logup'),
    re_path(r'^(?P<room_name>[^/]+)/$', views.room, name='view-room'),
    re_path(r'^(?P<room_name>[^/]+)/fileupload/$', views.fileupload, name='view-upload'),
    re_path(r'^(?P<room_name>[^/]+)/chatupdate/$', views.chatupdate, name='view-update'),

]
