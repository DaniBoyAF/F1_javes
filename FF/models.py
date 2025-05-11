from django.db import models
# Create your models here.
class Usuario(models.Model):
    Nome = models.CharField(max_length=1000)
    Email = models.EmailField(max_length=1000)
    Senha = models.CharField(max_length=1000)
    
    def __str__(self):
        return self.Nome
class Amizade(models.Model):
    solicitante = models.ForeignKey(Usuario, related_name='solicitante', on_delete=models.CASCADE)
    destinatario = models.ForeignKey(Usuario, related_name='destinatario', on_delete=models.CASCADE)
    status= models.CharField(max_length=20, choices=[('pendente', 'Pendente'), ('aceito', 'Aceito'), ('recusado', 'Recusado')],
                             default='pendente')
    timestamp= models.DateTimeField(auto_now_add=True)
    def aceitar(self):
        self.status = 'aceito'
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