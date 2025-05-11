from django.urls import path ,include
from django.contrib import admin
from FF.views import InicioView, TelemetriaView,SessionData, CarStatus, LapData,Penaty, Usuario, Amizade, login_view, aceitar_solicitacao, enviar_solicitacao
from FF.udp_listener import udp_server


urlpatterns = [
    path('', InicioView.as_view(), name='index'),
    
    path('api/telemetria/', TelemetriaView.as_view(), name='telemetria'),
    path('api/sessao/', SessionData.as_view(), name='sessao'),
    path('api/status-carro/', CarStatus.as_view(), name='status_carro'),
    path('api/voltas/', LapData.as_view(), name='voltas'),
    path('api/punicoes/', Penaty.as_view(), name='punicoes'),
    path('amizade/enviar/<int:destinatario_id>/', enviar_solicitacao.as_view(), name='enviar_solicitacao'),
    path('amizade/aceitar/<int:amizade_id>/', aceitar_solicitacao.as_view(), name='aceitar_solicitacao'),
   # path('amizade/recusar/<int:amizade_id>/', recusar_solicitacao.as_view(), name='recusar_solicitacao'),
    path('login/', login_view.as_view(), name='login'),
]