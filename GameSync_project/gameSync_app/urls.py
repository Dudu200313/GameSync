from django.urls import path 

from . import views 
from . import views_user
from .views import add_to_playlist, add_to_wishlist, add_to_owned

urlpatterns = [ 
    path('', views.index, name='index'),
    path('other/', views.other, name='other'),
    path('register/', views_user.register, name='register'),
    path('login/', views_user.user_login, name='login'),
    path('<int:game_id>/', views.game_detail, name='game_detail'),
    path('add-to-playlist/<int:game_id>/<str:game_name>/', add_to_playlist, name='add_to_playlist'),
    path('add-to-wishlist/<int:game_id>/<str:game_name>/', add_to_wishlist, name='add_to_wishlist'),
    path('add-to-owned/<int:game_id>/<str:game_name>/', add_to_owned, name='add_to_owned'),
    path('playlist/', views.user_playlist, name='user_playlist'),
    path('diary/', views.user_diary, name='user_diary'),
    path('wishlist/', views.user_wishlist, name='user_wishlist'),
    path('owned/', views.user_owned, name='user_owned'),
    path('user/', views.tela_usuario, name='tela_usuario'),
    path('user/<int:user_id>/', views.tela_usuario, name='tela_usuario_other'),
    path('follow/<int:user_id>/', views_user.follow_unfollow, name='follow_unfollow'),
    path('search/', views.search_results, name='search_results'),
]

#as aspas definem a rota / na view, se for fazia vai ser meio que a home