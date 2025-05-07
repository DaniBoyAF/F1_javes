import django
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Telemetria, SessionData, CarStatus, LapData, Penaty
from .serializers import (
    TelemetriaSerializer,
    SessionDataSerializer,
    CarStatusSerializer,
    LapDataSerializer,
    PenatySerializer
)

@api_view(['GET', 'POST'])
def telemetria_view(request):
    if request.method == 'GET':
        dados = Telemetria.objects.all()
        serializer = TelemetriaSerializer(dados, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TelemetriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def session_data_view(request):
    if request.method == 'GET':
        dados = SessionData.objects.all()
        serializer = SessionDataSerializer(dados, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SessionDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def car_status_view(request):
    if request.method == 'GET':
        dados = CarStatus.objects.all()
        serializer = CarStatusSerializer(dados, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CarStatusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def lap_data_view(request):
    if request.method == 'GET':
        dados = LapData.objects.all()
        serializer = LapDataSerializer(dados, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = LapDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def penaty_view(request):
    if request.method == 'GET':
        dados = Penaty.objects.all()
        serializer = PenatySerializer(dados, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PenatySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
