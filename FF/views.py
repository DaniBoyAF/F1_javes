from django.shortcuts import get_object_or_404
from django.shortcuts import render ,redirect
from django.views import View
from FF.models import Telemetria, SessionData, CarStatus, LapData, Penaty, Usuario, Amizade
from django.http import JsonResponse

class InicioView(View):
    def get(self, request):
        # Renderizar a página inicial
        return render(request, 'index.html')
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
        telemetria.save()
        return JsonResponse({'status': 'success'})
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
                num_voltas = request.POST.get('num_voltas')
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
              desgaste_pneus = request.POST.get('desgaste_pneus')
              temperatura_pneus = request.POST.get('temperatura_pneus')
              temperatura_real = request.POST.get('temperatura_real')
              composto_visual = request.POST.get('composto_visual')
              tipo_pneus = request.POST.get('tipo_pneus')

              carStatus = CarStatus(
                  carro_id=carro_id,
                  desgaste_pneus=desgaste_pneus,
                  temperatura_pneus=temperatura_pneus,
                  temperatura_real=temperatura_real,
                  composto_visual=composto_visual,
                  tipo_pneus=tipo_pneus
              )
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
             tempo_volta = request.POST.get('tempo_volta')
             tempo_setor1 = request.POST.get('tempo_setor1')
             tempo_setor2 = request.POST.get('tempo_setor2')
             tempo_setor3 = request.POST.get('tempo_setor3')
             posicao = request.POST.get('posicao')
             volta_valida = request.POST.get('volta_valida')

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
             volta = request.POST.get('volta')
             tipo_punicao = request.POST.get('tipo_punicao')
             tempo_punicao = request.POST.get('tempo_punicao')

             penalty = Penaty(
                 numero_carro=numero_carro,
                 nome_piloto=nome_piloto,
                 volta=volta,
                 tipo_punicao=tipo_punicao,
                 tempo_punicao=tempo_punicao
             )
             penalty.save()
             return redirect('/penalty/')