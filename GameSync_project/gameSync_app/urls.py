from django.urls import path 

from . import views 

urlpatterns = [ 
    path('', views.index, name='index'),
    path('other/', views.other, name='other'),
]


#as aspas definem a rota / na view, se for fazia vai ser meio que a home