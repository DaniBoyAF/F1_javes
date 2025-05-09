from django.db import models
# Create your models here.
class Telemetria(models.Model):
    nome_piloto = models.CharField(max_length=100)
    carro_id = models.IntegerField()
    velocidade = models.FloatField()  # km/h
    marcha = models.IntegerField()
    freio = models.FloatField()
    Acelerador = models.FloatField()
    rpm_motor = models.IntegerField()
    rpm_max = models.IntegerField()
    rpm_ideal = models.IntegerField()
    drs_ativo = models.BooleanField()
    ers_disponivel = models.FloatField()
    nivel_combustivel = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
class SessionData(models.Model):
    clima = models.CharField(max_length=20)
    temperatura_pista = models.IntegerField()
    temperatura_ar = models.IntegerField()
    zonas_drs = models.IntegerField()
    pista = models.CharField(max_length=100)
    tempo_total = models.FloatField()
    tipo_sessao = models.CharField(max_length=20)
    num_voltas = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
class CarStatus(models.Model):
    carro_id = models.IntegerField()
    desgaste_pneus = models.JSONField()  # lista com 4 valores
    temperatura_pneus = models.JSONField()
    temperatura_real = models.JSONField()
    composto_visual = models.CharField(max_length=20)
    tipo_pneus = models.CharField(max_length=20)  # exemplo: "soft", "medium", "hard"
    
    timestamp = models.DateTimeField(auto_now_add=True)
   

class LapData(models.Model):
    carro_id = models.IntegerField()
    nome_piloto = models.CharField(max_length=100)
    volta = models.IntegerField()
    tempo_volta = models.FloatField()
    tempo_setor1 = models.FloatField()
    tempo_setor2 = models.FloatField()
    tempo_setor3 = models.FloatField()
    posicao = models.IntegerField()
    volta_valida = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Penaty(models.Model):
    numero_carro = models.IntegerField()
    nome_piloto = models.CharField(max_length=100)
    volta = models.IntegerField()
    tipo_punicao = models.CharField(max_length=100)  # exemplo: "track limits", "collision"
    tempo_punicao = models.FloatField()  # em segundos
    cumprida = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)