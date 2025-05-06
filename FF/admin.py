from django.contrib import admin
from .models import Telemetria, SessionData, CarStatus ,LapData, Penaty
# Register your models here.
@admin.register(Telemetria)
class TelemetriaAdmin(admin.ModelAdmin):
    list_display = ('nome_piloto', 'carro_id', 'velocidade', 'rpm_motor', 'timestamp')
    search_fields = ('nome_piloto', 'carro_id')
    list_filter = ('nome_piloto',)

@admin.register(SessionData)
class SessionDataAdmin(admin.ModelAdmin):
    list_display = ('pista', 'tipo_sessao', 'clima', 'num_voltas', 'timestamp')
    search_fields = ('pista',)
    list_filter = ('tipo_sessao',)

@admin.register(CarStatus)
class CarStatusAdmin(admin.ModelAdmin):
    list_display = ('carro_id', 'tipo_pneus', 'composto_visual', 'timestamp')
    list_filter = ('tipo_pneus', 'composto_visual')

@admin.register(LapData)
class LapDataAdmin(admin.ModelAdmin):
    list_display = ('nome_piloto', 'volta', 'tempo_volta', 'posicao', 'volta_valida', 'timestamp')
    search_fields = ('nome_piloto',)
    list_filter = ('volta_valida',)

@admin.register(Penaty)
class PenatyAdmin(admin.ModelAdmin):
    list_display = ('nome_piloto', 'volta', 'tipo_punicao', 'tempo_punicao', 'cumprida', 'timestamp')
    list_filter = ('tipo_punicao', 'cumprida')
    search_fields = ('nome_piloto',)
