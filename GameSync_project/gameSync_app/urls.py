from django.urls import path 

from . import views 
from . import views_user

urlpatterns = [ 
    path('', views.index, name='index'),
    path('other/', views.other, name='other'),
    path('register/', views_user.register, name='register'),
    path('login/', views_user.user_login, name='login'),
]


#as aspas definem a rota / na view, se for fazia vai ser meio que a home