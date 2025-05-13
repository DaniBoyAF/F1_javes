import socket
import threading
import os
import django
import sys
import datetime
import random 

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
def parse_f1_packet_placeholder(raw_data):
    """
    Placeholder MUITO SIMPLIFICADO para a função de parsing dos pacotes de telemetria F1.
    Esta função deve converter os bytes brutos (raw_data) em um dicionário
    contendo os dados estruturados e um campo 'type' para identificar o modelo alvo.

    Retorna: Um dicionário com os dados parseados, ou None se o parsing falhar.
    """
    try:
        if not raw_data or len(raw_data) < 10: # Checagem mínima
            log_error(f"Pacote UDP recebido é muito pequeno ou vazio (tamanho: {len(raw_data)} bytes).")
            return None

        # SIMULAÇÃO: Aleatoriamente escolhe um tipo de pacote para gerar dados simulados
        # Em um parser real, você identificaria o tipo de pacote pelo cabeçalho dos dados F1.
        # Ex: packet_id = struct.unpack_from('<B', raw_data, 5)[0] (o 5º byte é geralmente o packetId)
        
        # Para simulação, vamos usar um byte simulado do pacote para decidir o tipo
        # Suponha que o primeiro byte do raw_data (simulado) indica o tipo de pacote
        simulated_packet_type_id = raw_data[0] % 5 # Gera um ID de 0 a 4

        parsed_data = {'raw_header_byte_for_sim': raw_data[0]} # Apenas para depuração da simulação

        if simulated_packet_type_id == 0: # Simula Pacote de Telemetria
            parsed_data.update({
                'type': 'telemetry',
                'nome_piloto': f'Piloto_{random.randint(1,20)}',
                'carro_id': random.randint(0,19),
                'velocidade': random.uniform(0, 350.5),
                'marcha': random.randint(-1, 8),
                'freio': random.random(),
                'Acelerador': random.random(),
                'rpm_motor': random.randint(0, 15000),
                'drs_ativo': random.choice([True, False]),
                'ers_disponivel': random.uniform(0, 4000000.0),
                'ers_percentagem': random.random(),
                'nivel_combustivel': random.uniform(0, 1.0) * 100
            })
        elif simulated_packet_type_id == 1: # Simula Pacote de Dados da Sessão
            parsed_data.update({
                'type': 'session_data',
                'clima': random.choice(['Ensolarado', 'Nublado', 'Chuva Leve', 'Chuva Forte']),
                'temperatura_pista': random.uniform(15.0, 45.0),
                'temperatura_ar': random.uniform(10.0, 35.0),
                'zonas_drs': float(random.randint(1,3)),
                'pista': random.choice(['Monza', 'Silverstone', 'Spa']),
                'tempo_total': random.uniform(3600, 7200),
                'tipo_sessao': random.choice(['Treino Livre', 'Qualificação', 'Corrida']),
                'num_voltas': random.randint(10, 70),
                'Coord_pista_x': random.uniform(-5000, 5000),
                'Coord_pista_y': random.uniform(-5000, 5000),
                'Coord_pista_z': random.uniform(0, 200)
            })
        elif simulated_packet_type_id == 2: # Simula Pacote de Status do Carro
            parsed_data.update({
                'type': 'car_status',
                'nome_piloto': f'Piloto_{random.randint(1,20)}',
                'carro_id': random.randint(0,19),
                'desgaste_pneus': [random.randint(0,100) for _ in range(4)], # JSONField
                'temperatura_pneus': [random.randint(80,120) for _ in range(4)], # JSONField
                'temperatura_real': [random.randint(80,120) for _ in range(4)], # JSONField
                'composto_visual': random.choice(['Macio', 'Médio', 'Duro']),
                'tipo_pneus': random.choice(['soft', 'medium', 'hard']),
                'dano_aerodinamicos_frontal': random.random() * 100,
                'dano_frontal_esquerdo': random.random() * 100,
                'dano_frontal_direito': random.random() * 100,
                'dano_aerodinamicos_traseiro': random.random() * 100,
                'danos_no_chassis': random.random() * 100
            })
        elif simulated_packet_type_id == 3: # Simula Pacote de Dados da Volta
            parsed_data.update({
                'type': 'lap_data',
                'carro_id': random.randint(0,19),
                'nome_piloto': f'Piloto_{random.randint(1,20)}',
                'volta': random.randint(1, 70),
                'tempo_volta': random.uniform(70.0, 120.0),
                'tempo_setor1': random.uniform(20.0, 40.0),
                'tempo_setor2': random.uniform(20.0, 40.0),
                'tempo_setor3': random.uniform(20.0, 40.0),
                'posicao': random.randint(1,20),
                'volta_valida': random.choice([True, False]),
                'localizacao_x': random.uniform(-5000, 5000),
                'localizacao_y': random.uniform(-5000, 5000)
            })
        elif simulated_packet_type_id == 4: # Simula Pacote de Penalidade
            parsed_data.update({
                'type': 'penalty_data', # Nome 'Penaty' no modelo
                'numero_carro': random.randint(0,19),
                'nome_piloto': f'Piloto_{random.randint(1,20)}',
                'volta': random.randint(1, 70),
                'tipo_punicao': random.choice(['Track limits', 'Collision', 'Speeding in pitlane']),
                'tempo_punicao': random.choice([5.0, 10.0, 0.0]), # 0.0 para drive-through/stop-go
                'cumprida': random.choice([True, False])
            })
        else:
            log_error(f"Simulação: Tipo de pacote desconhecido (ID simulado: {simulated_packet_type_id}).")
            return None
        
        # print(f"Pacote parseado (simulado): {parsed_data['type']}")
        return parsed_data

    except Exception as e:
        log_error(f"Erro durante o parsing simulado do pacote UDP: {e}. Dados (primeiros 20 bytes): {raw_data[:20].hex()}")
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
            # print(f"Pacote UDP ({len(data)} bytes) recebido de {addr}")

            parsed_packet = parse_f1_packet_placeholder(data)

            if not parsed_packet:
                # Erro já logado dentro do parser
                continue

            packet_type = parsed_packet.get('type')

            if packet_type == 'telemetry':
                obj = Telemetria(
                    nome_piloto=parsed_packet.get('nome_piloto'),
                    carro_id=parsed_packet.get('carro_id'),
                    velocidade=parsed_packet.get('velocidade'),
                    marcha=parsed_packet.get('marcha'),
                    freio=parsed_packet.get('freio'),
                    Acelerador=parsed_packet.get('Acelerador'),
                    rpm_motor=parsed_packet.get('rpm_motor'),
                    drs_ativo=parsed_packet.get('drs_ativo'),
                    ers_disponivel=parsed_packet.get('ers_disponivel'),
                    ers_percentagem=parsed_packet.get('ers_percentagem'),
                    nivel_combustivel=parsed_packet.get('nivel_combustivel')
                )
                obj.save()
                print(f"Salvo: Telemetria para {obj.nome_piloto}")

            elif packet_type == 'session_data':
                obj = SessionData(
                    clima=parsed_packet.get('clima'),
                    temperatura_pista=parsed_packet.get('temperatura_pista'),
                    temperatura_ar=parsed_packet.get('temperatura_ar'),
                    zonas_drs=parsed_packet.get('zonas_drs'),
                    pista=parsed_packet.get('pista'),
                    tempo_total=parsed_packet.get('tempo_total'),
                    tipo_sessao=parsed_packet.get('tipo_sessao'),
                    num_voltas=parsed_packet.get('num_voltas'),
                    Coord_pista_x=parsed_packet.get('Coord_pista_x'),
                    Coord_pista_y=parsed_packet.get('Coord_pista_y'),
                    Coord_pista_z=parsed_packet.get('Coord_pista_z')
                )
                obj.save()
                print(f"Salvo: Dados da Sessão para pista {obj.pista}")

            elif packet_type == 'car_status':
                obj = CarStatus(
                    nome_piloto=parsed_packet.get('nome_piloto'),
                    carro_id=parsed_packet.get('carro_id'),
                    desgaste_pneus=parsed_packet.get('desgaste_pneus'),
                    temperatura_pneus=parsed_packet.get('temperatura_pneus'),
                    temperatura_real=parsed_packet.get('temperatura_real'),
                    composto_visual=parsed_packet.get('composto_visual'),
                    tipo_pneus=parsed_packet.get('tipo_pneus'),
                    dano_aerodinamicos_frontal=parsed_packet.get('dano_aerodinamicos_frontal'),
                    dano_frontal_esquerdo=parsed_packet.get('dano_frontal_esquerdo'),
                    dano_frontal_direito=parsed_packet.get('dano_frontal_direito'),
                    dano_aerodinamicos_traseiro=parsed_packet.get('dano_aerodinamicos_traseiro'),
                    danos_no_chassis=parsed_packet.get('danos_no_chassis')
                )
                obj.save()
                print(f"Salvo: Status do Carro para {obj.nome_piloto}")

            elif packet_type == 'lap_data':
                obj = LapData(
                    carro_id=parsed_packet.get('carro_id'),
                    nome_piloto=parsed_packet.get('nome_piloto'),
                    volta=parsed_packet.get('volta'),
                    tempo_volta=parsed_packet.get('tempo_volta'),
                    tempo_setor1=parsed_packet.get('tempo_setor1'),
                    tempo_setor2=parsed_packet.get('tempo_setor2'),
                    tempo_setor3=parsed_packet.get('tempo_setor3'),
                    posicao=parsed_packet.get('posicao'),
                    volta_valida=parsed_packet.get('volta_valida'),
                    localizacao_x=parsed_packet.get('localizacao_x'),
                    localizacao_y=parsed_packet.get('localizacao_y')
                )
                obj.save()
                print(f"Salvo: Dados da Volta {obj.volta} para {obj.nome_piloto}")

            elif packet_type == 'penalty_data': # Modelo é 'Penaty'
                obj = Penaty(
                    numero_carro=parsed_packet.get('numero_carro'),
                    nome_piloto=parsed_packet.get('nome_piloto'),
                    volta=parsed_packet.get('volta'),
                    tipo_punicao=parsed_packet.get('tipo_punicao'),
                    tempo_punicao=parsed_packet.get('tempo_punicao'),
                    cumprida=parsed_packet.get('cumprida')
                )
                obj.save()
                print(f"Salvo: Penalidade para {obj.nome_piloto}")
            
            else:
                log_error(f"Tipo de pacote desconhecido ou não mapeado para modelo: {packet_type}. Dados: {parsed_packet}")

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

