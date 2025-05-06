from rest_framework import serializers
from .models import Telemetria, SessionData, CarStatus, LapData, Penaty

class TelemetriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Telemetria
        fields = '__all__'

class SessionDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionData
        fields = '__all__'

class CarStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarStatus
        fields = '__all__'

class LapDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = LapData
        fields = '__all__'

class PenatySerializer(serializers.ModelSerializer):
    class Meta:
        model = Penaty
        fields = '__all__'
