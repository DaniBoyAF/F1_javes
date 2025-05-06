from django.shortcuts import render
from .parsers import parse_session_packet, parse_car_status_packet
from .models import SessionData, CarStatus ,Telemetria, LapData, Penaty
from django.http import JsonResponse

# Create your views here.
def salvar_dados_ups(data):
    packet_id = data[5]
    if packet_id == 1:
        session_info = parse_session_packet(data)
        SessionData.objects.create(**session_info)
    elif packet_id == 7:
        carros = parse_car_status_packet(data)
        for carro in carros:
            CarStatus.objects.create(
                carro_id=carro["id"], desgaste_pneus=carro["desgaste_pneus"], temperatura_pneus=carro["temperatura_pneus"], temperatura_real=carro["temperatura_real"]
    )

def ver_status(request):
    dados = list(CarStatus.objects.order_by("-timestamp")[:10].values())
    return JsonResponse(dados,safe=False)
def ver_clima(request):
    dados = list(SessionData.objects.order_by("-timestamp")[:5].values())
    return JsonResponse(dados,safe=False)