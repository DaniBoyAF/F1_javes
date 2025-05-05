from django.db import models
# Create your models here.
class Telemetria(models.Model):
    nome_piloto = models.CharField(max_length=100)
    volta = models.IntegerField()
    numero_carro = models.IntegerField()
    tempo = models.FloatField()
    posicao= models.IntegerField()
    velocidade = models.FloatField()
    tipo_pneus = models.CharField(max_length=20)
    
class SessionData(models.Model):
    clima = models.CharField(max_length=20)
    temperatura_pista = models.IntegerField()
    temperatura_ar = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
class CarStatus(models.Model):
    carro_id = models.IntegerField()
    desgaste_pneus = models.JSONField()  # lista com 4 valores
    temperatura_pneus = models.JSONField()
    temperatura_real = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)

