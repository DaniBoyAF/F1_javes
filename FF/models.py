from django.db import models
from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from django.utils import timezone
# Create your models here.
class Usuario(models.Model):
    Nome = models.CharField(max_length=1000)
    Email = models.EmailField(max_length=1000)
    Senha = models.CharField(max_length=200)
    
    def get(self,request):
        return render(request, 'FF/templates/cadastro.html')
    def save(self, *args, **kwargs):
        # Aqui você pode adicionar lógica para verificar se o email já existe
        if Usuario.objects.filter(Email=self.Email).exists():
            raise ValueError("Email já existe")
        return super().save(*args, **kwargs)
    def save(self, *args, **kwargs):
        if self.Senha:
            self.Senha = make_password(self.Senha)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.Nome
class Amizade(models.Model):
    solicitante = models.ForeignKey(Usuario, related_name='solicitante', on_delete=models.CASCADE)
    destinatario = models.ForeignKey(Usuario, related_name='destinatario', on_delete=models.CASCADE)
    status= models.CharField(max_length=20, choices=[('pendente', 'Pendente'), ('aceito', 'Aceito'), ('recusado', 'Recusado')],
                             default='pendente')
    timestamp= models.DateTimeField(auto_now_add=True)
    def salvar(self):
        self.save()
    def aceitar(self):
        self.status = 'aceito'
        self.save()
    def recusar(self):
        self.status = 'recusado'
        self.save()
    def __str__(self):
        return f"Amizade de {self.solicitante} para {self.destinatario} - {self.status}"

class Telemetria(models.Model):
    nome_piloto = models.CharField(max_length=100)
    carro_id = models.IntegerField()
    velocidade = models.FloatField()  # km/h
    marcha = models.IntegerField()
    freio = models.FloatField()
    Acelerador = models.FloatField()
    rpm_motor = models.IntegerField()
    drs_ativo = models.BooleanField()
    ers_disponivel = models.FloatField()
    ers_percentagem = models.FloatField()
    nivel_combustivel = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        # Aqui você pode adicionar lógica para verificar se o carro já existe
        if Telemetria.objects.filter(carro_id=self.carro_id).exists():
            raise ValueError("Carro já existe")
        return super().save(*args, **kwargs)
    def __str__(self):
        return f"Telemetria de {self.nome_piloto} - Carro ID: {self.carro_id} - Velocidade: {self.velocidade} km/h - Marcha: {self.marcha} - RPM: {self.rpm_motor} - DRS Ativo: {self.drs_ativo} - ERS Disponível: {self.ers_disponivel} - Combustível: {self.nivel_combustivel}"
    
class SessionData(models.Model):
    clima = models.CharField(max_length=20)
    temperatura_pista = models.FloatField()
    temperatura_ar = models.FloatField()
    zonas_drs = models.FloatField()
    pista = models.CharField(max_length=100)
    tempo_total = models.FloatField()
    tipo_sessao = models.CharField(max_length=20)
    num_voltas = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    Coord_pista_x = models.FloatField()
    Coord_pista_y = models.FloatField()
    Coord_pista_z = models.FloatField()

    def __str__(self):
        return f"Dados da Sessão - Clima: {self.clima} - Temperatura Pista: {self.temperatura_pista}°C - Temperatura Ar: {self.temperatura_ar}°C - Zonas DRS: {self.zonas_drs} - Pista: {self.pista} - Tempo Total: {self.tempo_total}s - Tipo de Sessão: {self.tipo_sessao} - Número de Voltas: {self.num_voltas} , - Coordenadas Pista: ({self.Coord_pista_x}, {self.Coord_pista_y}, {self.Coord_pista_z})"
   

class CarStatus(models.Model):
    nome_piloto = models.CharField(max_length=100)
    carro_id = models.IntegerField()
    desgaste_pneus = models.JSONField()  # lista com 4 valores
    temperatura_pneus = models.JSONField()
    temperatura_real = models.JSONField()
    composto_visual = models.CharField(max_length=20)
    tipo_pneus = models.CharField(max_length=20)  # exemplo: "soft", "medium", "hard"
    dano_aerodinamicos_frontal = models.FloatField()  # percentual de dano
    dano_frontal_esquerdo = models.FloatField()  # percentual de dano
    dano_frontal_direito = models.FloatField()  # percentual de dano
    dano_aerodinamicos_traseiro = models.FloatField()  # percentual de dano
    danos_no_chassis = models.FloatField()  # percentual de dano
    timestamp = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        # Aqui você pode adicionar lógica para verificar se o carro já existe
        if CarStatus.objects.filter(carro_id=self.carro_id).exists():
            raise ValueError("Carro já existe")
        return super().save(*args, **kwargs)
    def __str__(self):
        return f"Status do Carro - Piloto: {self.nome_piloto} - Carro ID: {self.carro_id} - Desgaste Pneus: {self.desgaste_pneus} - Temperatura Pneus: {self.temperatura_pneus} - Temperatura Real: {self.temperatura_real} - Composto Visual: {self.composto_visual} - Tipo de Pneus: {self.tipo_pneus} - Dano Aerodinâmico Frontal: {self.dano_aerodinamicos_frontal}% - Dano Frontal Esquerdo: {self.dano_frontal_esquerdo}% - Dano Frontal Direito: {self.dano_frontal_direito}% - Dano Aerodinâmico Traseiro: {self.dano_aerodinamicos_traseiro}% - Danos no Chassi: {self.danos_no_chassis}%"
   

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
    localizacao_x = models.FloatField()
    localizacao_y = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Dados da Volta - Carro ID: {self.carro_id} - Piloto: {self.nome_piloto} - Volta: {self.volta} - Tempo da Volta: {self.tempo_volta}s - Tempo Setor 1: {self.tempo_setor1}s - Tempo Setor 2: {self.tempo_setor2}s - Tempo Setor 3: {self.tempo_setor3}s - Posição: {self.posicao} - Volta Válida: {self.volta_valida}, - Localização: ({self.localizacao_x}, {self.localizacao_y})"

class Penaty(models.Model):
    carro_id = models.IntegerField()
    nome_piloto = models.CharField(max_length=100)
    volta = models.IntegerField()
    tipo_punicao = models.CharField(max_length=100)  # exemplo: "track limits", "collision"
    tempo_punicao = models.FloatField()  # em segundos
    cumprida = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Penalidade - Carro ID: {self.carro_id} - Piloto: {self.nome_piloto} - Volta: {self.volta} - Tipo de Penalidade: {self.tipo_punicao} - Tempo de Penalidade: {self.tempo_punicao}s - Cumprida: {self.cumprida}"