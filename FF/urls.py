from django.urls import path ,include
from django.contrib import admin
from FF.views import InicioView, Usuario, Amizade, login_view, aceitar_solicitacao, enviar_solicitacao
from FF.udp_listener import udp_server_listener,parse_f1_packet_placeholder
from FF.views import UniaoView

urlpatterns = [
    path('', InicioView.as_view(), name='index'),
    path('amizade/enviar/<int:destinatario_id>/', enviar_solicitacao.as_view(), name='enviar_solicitacao'),
    path('amizade/aceitar/<int:amizade_id>/', aceitar_solicitacao.as_view(), name='aceitar_solicitacao'),
   # path('amizade/recusar/<int:amizade_id>/', recusar_solicitacao.as_view(), name='recusar_solicitacao'),
    path('login/', login_view.as_view(), name='login'),
    path('udp_listener/', udp_server_listener, name='udp_listener'),
    path('cadastro-view/', Usuario.as_view(), name='usuario'),
    path('amizade/', Amizade.as_view(), name='amizade'),
    path('união/', UniaoView.as_view(), name='uniao'),
  ]