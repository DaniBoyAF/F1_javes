from django.urls import path
from . import views

urlpatterns =[
    path('ver_status/', views.ver_status, name='ver_status'),
    path('ver_clima/', views.ver_clima, name='ver_clima'),
    path('salvar_dados_ups/', views.salvar_dados_ups, name='salvar_dados_ups'),
]