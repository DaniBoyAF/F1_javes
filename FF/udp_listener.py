import socket
import threading
from django.core.wsgi import get_wsgi_application
import os
import django

import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# Inicializar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'f1.settings')
django.setup()

from FF.views import salvar_dados_udp
def udp_server(host="0.0.0.0", port=20777):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    print(f"Servidor UDP escutando em {host}:{port}...")

    while True:
        data, _ = sock.recvfrom(2048)
        try:
            salvar_dados_udp(data)
        except Exception as e:
            print("Erro ao processar pacote:", e)

# Rodar em thread separada se for acoplado ao runserver
if __name__ == "__main__":
    thread = threading.Thread(target=udp_server)
    thread.daemon = True
    thread.start()

    # Mantém o script vivo
    while True:
        pass
