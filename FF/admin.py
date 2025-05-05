from django.contrib import admin
from .models import Telemetria, SessionData, CarStatus
# Register your models here.
@admin.register(Telemetria)
class TelemetriaAdmin(admin.ModelAdmin):
    list_display = ("nome_piloto", "volta", "numero_carro", "tempo", "posicao", "velocidade", "tipo_pneus")
    search_fields = ("nome_piloto", "numero_carro")
    list_filter=("tipo_pneus",)

@admin.register(SessionData)
class SessionDataAdmin(admin.ModelAdmin):
    list_display = ("clima","temperatura_pista", "temperatura_ar", "timestamp")
    list_filter = ("clima", "timestamp")

@admin.register(CarStatus)
class CarStatusAdmin(admin.ModelAdmin):
    list_display = ("carro_id", "desgaste_pneus", "temperatura_pneus", "temperatura_real", "timestamp")
    list_filter = ("carro_id", "timestamp")
