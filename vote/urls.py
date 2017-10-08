from django.conf.urls import include, url
from . import views
from django.contrib.auth.views import login,logout

urlpatterns = [
    #ホーム画面
    url(r'^$', views.index, name='home'),
    #投票部屋入室画面
    url(r'^room_list/$', views.room_list, name='room_list'),
    #入室処理
    url(r'^room_enter$', views.room_enter, name='room_enter'),
    #投票部屋作成画面
    url(r'^room_create/$', views.room_create, name='room_create'),
    #投票選択肢作成画面(選出形式)
    url(r'^room_create_elect/$', views.room_create_elect, name='room_create_elect'),
    #投票処理
    url(r'^vote_elect/$', views.vote_elect, name='vote_elect'),
    #会員登録画面
    url(r'^register/$', views.register, name='register'),
    #ログイン画面
    url(r'^login/$', login, {'template_name' : 'vote/login.html'}, name='login'),
    #ログアウト処理
    url(r'^logout/$', logout, {'template_name' : 'vote/logout.html'}, name='logout'),
]
