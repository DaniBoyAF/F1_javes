import socket
import threading
import os
import django
import sys
import datetime

# --- CONFIGURAÇÃO DO LOG DE ERROS ---
LOG_FILE_PATH = '/home/ubuntu/udp_errors.log'

def log_error(message):
    """Registra uma mensagem de erro no arquivo de log com timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE_PATH, 'a') as f:
        f.write(f"{timestamp} - ERROR - {message}\n")
    print(f"ERROR logged: {message}") # Também imprime no console

# --- INICIALIZAÇÃO DO DJANGO ---
# Adiciona o caminho do projeto Django ao sys.path se necessário
# Supondo que este script está em FF/ e o manage.py está um nível acima (no diretório F1_javes)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'f1.settings') # Substitua 'f1.settings' pelo seu arquivo de settings
try:
    django.setup()
    print("Django setup successful.")
except Exception as e:
    log_error(f"Django setup failed: {e}")
    print(f"CRITICAL: Django setup failed: {e}. O listener não poderá interagir com os modelos.")
    # Decide se quer sair ou continuar sem models
    # sys.exit(1) 

# Importe seus modelos Django AQUI, APÓS django.setup()
# Certifique-se de que os modelos existem e o app FF está em INSTALLED_APPS
try:
    from FF.models import Telemetria , SessionData, CarStatus, LapData, Penaty # Adicione outros modelos conforme necessário
    print("Modelos Django importados com sucesso.")
except ImportError as e:
    log_error(f"Falha ao importar modelos Django: {e}. Verifique se o app 'FF' está em INSTALLED_APPS e os modelos estão definidos.")
    # Define um mock para Telemetria para o script não quebrar completamente se a importação falhar
    # Em um cenário real, você trataria isso de forma mais robusta ou sairia.
    class Telemetria:
        def __init__(self, **kwargs): self.kwargs = kwargs
        def save(self): log_error(f"MOCK SAVE: {self.kwargs}")
    print("Usando Mock para Telemetria devido a erro de importação.")

# --- LÓGICA DE PARSING (SIMULADA/PLACEHOLDER) ---
def parse_f1_telemetry_packet(raw_data):
    """
    Placeholder para a função de parsing dos pacotes de telemetria F1.
    Esta função deve converter os bytes brutos (raw_data) em um dicionário
    ou objeto contendo os dados estruturados.

    Retorna: Um dicionário com os dados parseados, ou None se o parsing falhar
             ou o pacote não for reconhecido.
    """
    # Exemplo MUITO SIMPLIFICADO - SUBSTITUA PELA SUA LÓGICA DE PARSING REAL!
    # Um parser real usaria o módulo 'struct' para desempacotar os bytes
    # de acordo com a especificação do formato do pacote F1.
    try:
        if len(raw_data) < 20: # Pacote muito pequeno para ser válido (exemplo)
            log_error(f"Pacote UDP muito pequeno para ser válido (tamanho: {len(raw_data)} bytes).")
            return None

        # Simulação de extração de alguns dados. Os índices e conversões são fictícios.
        # Você precisará consultar a documentação do formato de telemetria do F1.
        # Exemplo: Identificar tipo de pacote (o F1 envia vários tipos)
        # packet_id = raw_data[5] # O byte do ID do pacote geralmente está no cabeçalho

        # if packet_id == 6: # Supondo que 6 é o ID para o pacote de telemetria principal
        parsed_data = {
            'type': 'telemetry', # O parser identificaria o tipo de pacote
            'nome_piloto': 'PilotoX', # Isso viria do jogo ou de uma configuração
            'carro_id': int(raw_data[0]), # Exemplo: primeiro byte como ID do carro
            'velocidade': float(int.from_bytes(raw_data[1:3], 'little', signed=False)) / 10.0, # Exemplo
            'marcha': int(raw_data[3]),
            'rpm_motor': int.from_bytes(raw_data[4:6], 'little'),
            # Adicione mais campos conforme a estrutura real do pacote
            'freio': float(raw_data[6]) / 255.0, # Normalizado 0-1
            'Acelerador': float(raw_data[7]) / 255.0, # Normalizado 0-1
            'drs_ativo': bool(raw_data[8]),
            'nivel_combustivel': float(raw_data[9]) / 100.0 # Exemplo
        }
        print(f"Pacote parseado (simulado): {parsed_data}")
        return parsed_data
        # else:
        #     log_error(f"Tipo de pacote UDP não reconhecido ou não tratado: ID {packet_id}")
        #     return None

    except Exception as e:
        log_error(f"Erro durante o parsing do pacote UDP: {e}. Dados (primeiros 20 bytes): {raw_data[:20].hex()}")
        return None

# --- SERVIDOR UDP ---
def udp_server_listener(host="0.0.0.0", port=20777):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.bind((host, port))
        print(f"Servidor UDP escutando em {host}:{port}...")
        log_error("Servidor UDP iniciado.") # Loga o início do servidor
    except Exception as e:
        log_error(f"Falha ao iniciar o servidor UDP em {host}:{port}: {e}")
        print(f"CRITICAL: Falha ao iniciar o servidor UDP: {e}")
        return # Não continua se o bind falhar

    while True:
        try:
            data, addr = sock.recvfrom(2048) # Buffer de 2KB, ajuste se necessário
            print(f"Pacote UDP recebido de {addr}. Tamanho: {len(data)} bytes.")

            # 1. Parsear o pacote de dados
            parsed_telemetry_data = parse_f1_telemetry_packet(data)

            if parsed_telemetry_data:
                # 2. Salvar os dados no modelo Django
                #    Aqui você pode ter uma lógica para diferentes tipos de pacotes/modelos
                if parsed_telemetry_data.get('type') == 'telemetry':
                    try:
                        telemetria_obj = Telemetria(
                            nome_piloto=parsed_telemetry_data.get('nome_piloto', 'N/A'),
                            carro_id=parsed_telemetry_data.get('carro_id', 0),
                            velocidade=parsed_telemetry_data.get('velocidade', 0.0),
                            marcha=parsed_telemetry_data.get('marcha', 0),
                            freio=parsed_telemetry_data.get('freio', 0.0),
                            Acelerador=parsed_telemetry_data.get('Acelerador', 0.0),
                            rpm_motor=parsed_telemetry_data.get('rpm_motor', 0),
                            drs_ativo=parsed_telemetry_data.get('drs_ativo', False),
                            ers_disponivel=parsed_telemetry_data.get('ers_disponivel', False),
                            ers_percentagem=parsed_telemetry_data.get('ers_percentagem', 0),
                            nivel_combustivel=parsed_telemetry_data.get('nivel_combustivel', 0.0)
                            # ... preencha todos os campos do seu modelo Telemetria
                        )
                        telemetria_obj.save()
                        print(f"Dados de telemetria salvos para: {telemetria_obj.nome_piloto}")
                    except Exception as e:
                        log_error(f"Erro ao salvar dados de telemetria no banco de dados: {e}. Dados: {parsed_telemetry_data}")
                # Adicione mais blocos 'elif' para outros tipos de pacotes/modelos aqui
                elif parsed_telemetry_data.get('type') == 'session_data':
                    # Salvar no modelo SessionData
                    session_data = SessionData(
                        clima=parsed_telemetry_data.get('clima', 'N/A'),
                        temperatura_pista=parsed_telemetry_data.get('temperatura_pista', 0),
                        temperatura_ar=parsed_telemetry_data.get('temperatura_ar', 0),
                        zonas_drs=parsed_telemetry_data.get('zonas_drs', 'N/A'),
                        pista=parsed_telemetry_data.get('pista', 'N/A'),
                        tempo_total=parsed_telemetry_data.get('tempo_total', 0),
                        tipo_sessao=parsed_telemetry_data.get('tipo_sessao', 'N/A'),
                        num_voltas=parsed_telemetry_data.get('num_voltas', 0),
                        Coord_pista_x=parsed_telemetry_data.get('Coord_pista_x', 0),
                        Coord_pista_y=parsed_telemetry_data.get('Coord_pista_y', 0),
                        Coord_pista_z=parsed_telemetry_data.get('Coord_pista_z', 0),
                    )
                    session_data.save()
                    print(f"Dados de sessão salvos para: {session_data.id}")
                else:
                    pass
            else:
                # O erro já foi logado dentro de parse_f1_telemetry_packet ou se o pacote era muito pequeno
                print("Pacote não processado ou parsing falhou.")

        except Exception as e:
            log_error(f"Erro geral no loop do servidor UDP: {e}")

# --- EXECUÇÃO PRINCIPAL ---
if __name__ == "__main__":
    print("Iniciando servidor UDP para telemetria F1 em uma thread separada...")
    # Limpa o arquivo de log antigo ao iniciar (opcional)
    # with open(LOG_FILE_PATH, 'w') as f:
    #     f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Log iniciado.\n")
    
    server_thread = threading.Thread(target=udp_server_listener)
    server_thread.daemon = True # Permite que o programa principal finalize mesmo se a thread estiver rodando
    server_thread.start()

    print(f"Servidor UDP rodando em background. Logs de erro em: {LOG_FILE_PATH}")
    print("Pressione Ctrl+C para encerrar o script principal.")

    try:
        while True:
            # Mantém o script principal rodando para que a thread daemon continue
            # Você pode adicionar outras lógicas aqui se este script fizer mais coisas
            threading.Event().wait(timeout=60) # Espera, verificando a cada 60s
    except KeyboardInterrupt:
        print("Encerrando script principal...")
        log_error("Servidor UDP encerrado pelo usuário (Ctrl+C).")
    finally:
        print("Script finalizado.")

