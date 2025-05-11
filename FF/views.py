from django.shortcuts import get_object_or_404
from django.shortcuts import render ,redirect
from django.views import View
from FF.models import Telemetria, SessionData, CarStatus, LapData, Penaty, Usuario, Amizade 
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from django.contrib import messages

class InicioView(View):
    def get(self, request):
        # Renderizar a página inicial
        return render(request, 'index.html')
class login_view(View):
    def get(self,request):
        # Renderizar a página de login
        return render(request, 'login.html')
    def post(self,request):
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        if not email or not senha:
           return JsonResponse({'status': 'error', 'message': 'Email e senha são obrigatórios.'})
        try:
            usuario= Usuario.objects.get(Email=email)
            if check_password(senha, usuario.Senha):
               return redirect('index')
            else:
             messages.error(request, 'Senha incorreta')
        except Usuario.DoesNotExist:
             messages.error(request, 'Usuário não encontrado')
        return render(request, 'login.html')
class salvar_dados_udp(View):
    def post(self,request):
        # Obtem todos os dados de telemetria
        nome_piloto = request.POST.get('nome_piloto')
        carro_id = request.POST.get('carro_id')
        velocidade = request.POST.get('velocidade')
        marcha = request.POST.get('marcha')
        freio = request.POST.get('freio')
        acelerador = request.POST.get('acelerador')
        rpm_motor = request.POST.get('rpm_motor')
        rpm_max = request.POST.get('rpm_max')
        rpm_ideal = request.POST.get('rpm_ideal')
        drs_ativo = request.POST.get('drs_ativo') == 'true'
        ers_disponivel = request.POST.get('ers_disponivel')
        nivel_combustivel = request.POST.get('nivel_combustivel')

        # Criar um novo registro de telemetria
        telemetria = Telemetria(
            nome_piloto=nome_piloto,
            carro_id=carro_id,
            velocidade=velocidade,
            marcha=marcha,
            freio=freio,
            Acelerador=acelerador,
            rpm_motor=rpm_motor,
            rpm_max=rpm_max,
            rpm_ideal=rpm_ideal,
            drs_ativo=drs_ativo,
            ers_disponivel=ers_disponivel,
            nivel_combustivel=nivel_combustivel
        )
        if not nome_piloto or not carro_id:
          return JsonResponse({'status': 'error', 'message': 'Dados obrigatórios estão faltando.'})
        telemetria.save()
        return JsonResponse({'status': 'success'})
class aceitar_solicitacao(View):
    def post(self, request, amizade_id):
        amizade = get_object_or_404(Amizade, id=amizade_id)
        amizade.aceitar()
        return redirect('/home/')

class enviar_solicitacao(View):
    def __init__(self, redirect, destinatario_id):
        self.redirect = redirect
        self.destinatario_id = destinatario_id

    def post(self, request):
        # Enviar solicitação de amizade para o destinatário
        destinatario = get_object_or_404(Usuario, id=self.destinatario_id)
        # Criar um novo registro de amizade
        amizade = Amizade(solicitante=request.user, destinatario=destinatario)
        amizade.save()
        return JsonResponse({'status': 'success'})

class TelemetriaView(View):
     def get(self,request):
        # Obtem todos os dados de telemetria
        telemetria = Telemetria.objects.all()
        return render(request, 'telemetria.html', {'telemetria': telemetria})
     
     def post(self,request):
        # Cria um novo registro de telemetria
        nome_piloto = request.POST.get('nome_piloto')
        carro_id = request.POST.get('carro_id')
        velocidade = int(request.POST.get('velocidade'))
        marcha = int(request.POST.get('marcha'))
        freio = int(request.POST.get('freio'))
        acelerador = int(request.POST.get('acelerador'))
        rpm_motor = int(request.POST.get('rpm_motor'))
        drs_ativo = request.POST.get('drs_ativo') == 'true'
        ers_disponivel = request.POST.get('ers_disponivel') =='true'
        # Adicionei o campo ers_percentagem
        ers_percentagem = int(request.POST.get('ers_percentagem'))
        nivel_combustivel = float(request.POST.get('nivel_combustivel'))

        telemetria = Telemetria(
            nome_piloto=nome_piloto,
            carro_id=carro_id,
            ers_percentagem=ers_percentagem,
            velocidade=velocidade,
            marcha=marcha,
            freio=freio,
            Acelerador=acelerador,
            rpm_motor=rpm_motor,
            drs_ativo=drs_ativo,
            ers_disponivel=ers_disponivel,
            nivel_combustivel=nivel_combustivel
        )
        if not nome_piloto or not carro_id:
         return JsonResponse({'status': 'error', 'message': 'Dados obrigatórios estão faltando.'})
        telemetria.save()
        return redirect('/telemetria/')
     class SessionDataView(View):
            def get(self,request):
                # Obter todos os dados da sessão
                sessionData= SessionData.objects.all()
                return render(request, 'sessionData.html', {'sessionData': sessionData})
            def post(self,request):
                # dados da sessão
                clima = request.POST.get('clima')
                temperatura_pista = request.POST.get('temperatura_pista')
                temperatura_ar = request.POST.get('temperatura_ar')
                zonas_drs = request.POST.get('zonas_drs')
                pista = request.POST.get('pista')
                tempo_total = request.POST.get('tempo_total')
                tipo_sessao = request.POST.get('tipo_sessao')
                num_voltas = int(request.POST.get('num_voltas', 0))
                sessionData = SessionData(
                    clima=clima,
                    temperatura_pista=temperatura_pista,
                    temperatura_ar=temperatura_ar,
                    zonas_drs=zonas_drs,
                    pista=pista,
                    tempo_total=tempo_total,
                    tipo_sessao=tipo_sessao,
                    num_voltas=num_voltas
                )
                sessionData.save()
                return redirect('/sessionData/')
      
     class CarStatusView(View):
          def get(self, request):
              # Obter todos os dados de status do carro
              carStatus = CarStatus.objects.all()
              return render(request, 'carStatus.html', {'carStatus': carStatus})

          def post(self, request):
              # Criar um novo registro de status do carro
              carro_id = request.POST.get('carro_id')
              nome_piloto = request.POST.get('nome_piloto')
              desgaste_pneus = int(request.POST.get('desgaste_pneus'))
              temperatura_pneus = float(request.POST.get('temperatura_pneus'))
              temperatura_real = float(request.POST.get('temperatura_real'))
              composto_visual = request.POST.get('composto_visual')
              tipo_pneus = request.POST.get('tipo_pneus')

              carStatus = CarStatus(
                  carro_id=carro_id,
                  nome_piloto=nome_piloto,
                  desgaste_pneus=desgaste_pneus,
                  temperatura_pneus=temperatura_pneus,
                  temperatura_real=temperatura_real,
                  composto_visual=composto_visual,
                  tipo_pneus=tipo_pneus
              )
              if not nome_piloto or not carro_id:
                return JsonResponse({'status': 'error', 'message': 'Dados obrigatórios estão faltando.'})
              carStatus.save()
              return redirect('/carStatus/')
     class LapDataView(View):
         def get(self, request):
             # Obter todos os dados de volta
             lapData = LapData.objects.all()
             return render(request, 'lapData.html', {'lapData': lapData})

         def post(self, request):
             # Criar um novo registro de volta
             carro_id = request.POST.get('carro_id')
             nome_piloto = request.POST.get('nome_piloto')
             volta = request.POST.get('volta')
             tempo_volta = float(request.POST.get('tempo_volta'))
             tempo_setor1 = float(request.POST.get('tempo_setor1'))
             tempo_setor2 = float(request.POST.get('tempo_setor2'))
             tempo_setor3 = float(request.POST.get('tempo_setor3'))
             posicao = int(request.POST.get('posicao'))
             volta_valida = request.POST.get('volta_valida') == 'true'

             lapData = LapData(
                 carro_id=carro_id,
                 nome_piloto=nome_piloto,
                 volta=volta,
                 tempo_volta=tempo_volta,
                 tempo_setor1=tempo_setor1,
                 tempo_setor2=tempo_setor2,
                 tempo_setor3=tempo_setor3,
                 posicao=posicao,
                 volta_valida=volta_valida
             )
             lapData.save()
             return redirect('/lapData/')
     class PenatyView(View):
         def get(self, request):
             # Obter todos os dados de penalidade
             penalty = Penaty.objects.all()
             return render(request, 'penalty.html', {'penalty': penalty})

         def post(self, request):
             # Criar um novo registro de penalidade
             numero_carro = request.POST.get('numero_carro')
             nome_piloto = request.POST.get('nome_piloto')
             volta = int(request.POST.get('volta'))
             tipo_punicao = int(request.POST.get('tipo_punicao'))
             tempo_punicao = int(request.POST.get('tempo_punicao'))

             penalty = Penaty(
                 numero_carro=numero_carro,
                 nome_piloto=nome_piloto,
                 volta=volta,
                 tipo_punicao=tipo_punicao,
                 tempo_punicao=tempo_punicao
             )
             penalty.save()
             return redirect('/penalty/')