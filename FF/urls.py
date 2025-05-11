from django.urls import path
from FF.views import views
from FF.udp_listener import udp_server

urlpatterns = [
    path('', views.InicioView.as_view(), name='index'),
    path('api/telemetria/', views.telemetria_view, name='telemetria'),
    path('api/sessao/', views.session_data_view, name='sessao'),
    path('api/status-carro/', views.car_status_view, name='status_carro'),
    path('api/voltas/', views.lap_data_view, name='voltas'),
    path('api/punicoes/', views.penaty_view, name='punicoes'),
    path('amizade/enviar<int:destinatario_id>/', views.enviar_solicitacao.as_view(), name='enviar_solicitacao'),
    path('amizade/aceitar<int:amizade_id>/', views.aceitar_solicitacao.as_view(), name='aceitar_solicitacao'),
    path('amizade/recusar<int:amizade_id>/', views.recusar_solicitacao.as_view(), name='recusar_solicitacao'),

]