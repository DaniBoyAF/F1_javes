import socket
import threading
import os
import django
import sys
import datetime
from FF.parsers import PacketHeader,HEADER_FIELD_TO_PACKET_TYPE
import ctypes

# --- CONFIGURAÇÃO DO LOG DE ERROS ---
# Idealmente, este caminho seria configurável ou relativo ao projeto
LOG_FILE_PATH = '/home/ubuntu/f1_javes_udp_errors.log'

def log_error(message):
    """Registra uma mensagem de erro no arquivo de log com timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(LOG_FILE_PATH, 'a') as f:
            f.write(f"{timestamp} - ERROR - {message}\n")
    except Exception as e:
        print(f"CRITICAL: Falha ao escrever no arquivo de log {LOG_FILE_PATH}: {e}")
    print(f"ERROR logged: {message}") # Também imprime no console

# --- INICIALIZAÇÃO DO DJANGO ---
# Supondo que este script está em F1_javes/FF/
# e manage.py está em F1_javes/
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'f1.settings')
try:
    django.setup()
    print("Django setup successful for udp_listener.")
except Exception as e:
    log_error(f"Django setup failed in udp_listener: {e}")
    print(f"CRITICAL: Django setup failed: {e}. O listener não poderá interagir com os modelos.")
    # sys.exit(1) # Descomente para sair se o Django não puder ser configurado

# Importe seus modelos Django AQUI, APÓS django.setup()
# Certifique-se de que os modelos existem e o app FF está em INSTALLED_APPS
try:
    from FF.models import Telemetria, SessionData, CarStatus, LapData, Penaty # Atenção ao nome 'Penaty'
    print("Modelos Django (Telemetria, SessionData, CarStatus, LapData, Penaty) importados com sucesso.")
except ImportError as e:
    log_error(f"Falha ao importar modelos Django: {e}. Verifique o app 'FF' e as definições dos modelos.")
    # Define mocks para os modelos para o script não quebrar completamente se a importação falhar
    # Em um cenário real, você trataria isso de forma mais robusta ou sairia.
    class BaseMockModel:
        def __init__(self, **kwargs): self.kwargs = kwargs
        def save(self): log_error(f"MOCK SAVE para {self.__class__.__name__}: {self.kwargs}")
        def __str__(self): return f"Mock {self.__class__.__name__}"

    class Telemetria(BaseMockModel): pass
    class SessionData(BaseMockModel): pass
    class CarStatus(BaseMockModel): pass
    class LapData(BaseMockModel): pass
    class Penaty(BaseMockModel): pass # Usando o nome como está no models.py
    print("Usando Mocks para modelos Django devido a erro de importação.")

# --- LÓGICA DE PARSING (SIMULADA/PLACEHOLDER) ---
def parse_f1_packet(raw_data):
    """
    TODO: Implemente aqui o parser real dos pacotes UDP do F1 24.
    Por enquanto, retorna None para não simular dados.
    """
    return None

# --- SERVIDOR UDP ---
def udp_server_listener(host="0.0.0.0", port=20777):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.bind((host, port))
        print(f"Servidor UDP escutando em {host}:{port} para telemetria F1...")
        log_error(f"Servidor UDP F1_javes iniciado em {host}:{port}.")
    except Exception as e:
        log_error(f"Falha CRÍTICA ao iniciar o servidor UDP em {host}:{port}: {e}")
        print(f"CRITICAL: Falha ao iniciar o servidor UDP: {e}")
        return

    while True:
        try:
            data, addr = sock.recvfrom(2048) # Buffer de 2KB
            # Aqui você chama o parser real (quando implementar)
            parsed = parse_f1_packet(data)

            if not parsed:
                # Erro já logado dentro do parser ou parser não implementado
                continue

            packet_type = parsed.get('type')

            if packet_type == 'telemetry':
                obj = Telemetria(
                    nome_piloto=parsed.get('nome_piloto'),
                    carro_id=parsed.get('carro_id'),
                    velocidade=parsed.get('velocidade'),
                    marcha=parsed.get('marcha'),
                    freio=parsed.get('freio'),
                    Acelerador=parsed.get('Acelerador'),
                    rpm_motor=parsed.get('rpm_motor'),
                    drs_ativo=parsed.get('drs_ativo'),
                    ers_disponivel=parsed.get('ers_disponivel'),
                    ers_percentagem=parsed.get('ers_percentagem'),
                    nivel_combustivel=parsed.get('nivel_combustivel')
                )
                obj.save()
                print(f"Salvo: Telemetria para {obj.nome_piloto}")

            elif packet_type == 'session_data':
                obj = SessionData(
                    clima=parsed.get('clima'),
                    temperatura_pista=parsed.get('temperatura_pista'),
                    temperatura_ar=parsed.get('temperatura_ar'),
                    zonas_drs=parsed.get('zonas_drs'),
                    pista=parsed.get('pista'),
                    tempo_total=parsed.get('tempo_total'),
                    tipo_sessao=parsed.get('tipo_sessao'),
                    num_voltas=parsed.get('num_voltas'),
                    Coord_pista_x=parsed.get('Coord_pista_x'),
                    Coord_pista_y=parsed.get('Coord_pista_y'),
                    Coord_pista_z=parsed.get('Coord_pista_z')
                )
                obj.save()
                print(f"Salvo: Dados da Sessão para pista {obj.pista}")

            elif packet_type == 'car_status':
                obj = CarStatus(
                    nome_piloto=parsed.get('nome_piloto'),
                    carro_id=parsed.get('carro_id'),
                    desgaste_pneus=parsed.get('desgaste_pneus'),
                    temperatura_pneus=parsed.get('temperatura_pneus'),
                    temperatura_real=parsed.get('temperatura_real'),
                    composto_visual=parsed.get('composto_visual'),
                    tipo_pneus=parsed.get('tipo_pneus'),
                    dano_aerodinamicos_frontal=parsed.get('dano_aerodinamicos_frontal'),
                    dano_frontal_esquerdo=parsed.get('dano_frontal_esquerdo'),
                    dano_frontal_direito=parsed.get('dano_frontal_direito'),
                    dano_aerodinamicos_traseiro=parsed.get('dano_aerodinamicos_traseiro'),
                    danos_no_chassis=parsed.get('danos_no_chassis')
                )
                obj.save()
                print(f"Salvo: Status do Carro para {obj.nome_piloto}")
        
            elif packet_type == 'lap_data':
                obj = LapData(
                    carro_id=parsed.get('carro_id'),
                    nome_piloto=parsed.get('nome_piloto'),
                    volta=parsed.get('volta'),
                    tempo_volta=parsed.get('tempo_volta'),
                    tempo_setor1=parsed.get('tempo_setor1'),
                    tempo_setor2=parsed.get('tempo_setor2'),
                    tempo_setor3=parsed.get('tempo_setor3'),
                    posicao=parsed.get('posicao'),
                    volta_valida=parsed.get('volta_valida'),
                    localizacao_x=parsed.get('localizacao_x'),
                    localizacao_y=parsed.get('localizacao_y')
                )
                obj.save()
                print(f"Salvo: Dados da Volta {obj.volta} para {obj.nome_piloto}")

            elif packet_type == 'penalty_data': # Modelo é 'Penaty'
                obj = Penaty(
                    carro_id=parsed.get('carro_id'),
                    nome_piloto=parsed.get('nome_piloto'),
                    volta=parsed.get('volta'),
                    tipo_punicao=parsed.get('tipo_punicao'),
                    tempo_punicao=parsed.get('tempo_punicao'),
                    cumprida=parsed.get('cumprida')
                )
                obj.save()
                print(f"Salvo: Penalidade para {obj.nome_piloto}")
            
            else:
                log_error(f"Tipo de pacote desconhecido ou não mapeado para modelo: {packet_type}. Dados: {parsed}")

        except Exception as e:
            log_error(f"Erro geral no loop do servidor UDP: {e}. Addr: {addr}")

# --- EXECUÇÃO PRINCIPAL ---
if __name__ == "__main__":
    print("Iniciando servidor UDP para telemetria F1 (F1_javes) em uma thread separada...")
    # Opcional: Limpar/Rotacionar log antigo ao iniciar
    # with open(LOG_FILE_PATH, 'w') as f:
    #     f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Log do Listener UDP F1_javes iniciado.\n")
    
    server_thread = threading.Thread(target=udp_server_listener)
    server_thread.daemon = True
    server_thread.start()

    print(f"Servidor UDP (F1_javes) rodando em background. Logs de erro em: {LOG_FILE_PATH}")
    print("Pressione Ctrl+C para encerrar o script principal.")

    try:
        while True:
            threading.Event().wait(timeout=3600) # Mantém o script principal vivo
    except KeyboardInterrupt:
        print("Encerrando script principal do listener UDP (F1_javes)...")
        log_error("Servidor UDP (F1_javes) encerrado pelo usuário (Ctrl+C).")
    finally:
        print("Script listener UDP (F1_javes) finalizado.")

