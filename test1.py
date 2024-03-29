import socket
import os

def monitor_directory():
    # Diretório a ser monitorado
    monitored_directory = "syncFolder"

    # Lista inicial de arquivos no diretório
    initial_files = set(os.listdir(monitored_directory))

    # Configurações do servidor para escutar alterações
    host_changes = '0.0.0.0'  # Escuta em todas as interfaces
    port_changes = 5555

    # Configurações do servidor para receber arquivos
    host_receive = '0.0.0.0'  # Escuta em todas as interfaces
    port_receive = 5556

    # Cria o socket TCP/IP para escutar alterações
    server_socket_changes = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket_changes.bind((host_changes, port_changes))
    server_socket_changes.listen(1)

    print(f"Aguardando conexões na porta {port_changes} para escutar alterações...")

    # Cria o socket TCP/IP para receber arquivos
    server_socket_receive = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket_receive.bind((host_receive, port_receive))
    server_socket_receive.listen(1)

    print(f"Aguardando conexões na porta {port_receive} para receber arquivos...")

    try:
        while True:
            # Aceita conexões para escutar alterações
            client_changes, addr_changes = server_socket_changes.accept()
            print(f"Conexão estabelecida para escutar alterações com {addr_changes}")

            # Lista de arquivos no diretório atual
            current_files = set(os.listdir(monitored_directory))

            # Compara a lista atual com a lista inicial
            changed_files = current_files - initial_files

            # Se houver alterações, exibe mensagem "changed file"
            if changed_files:
                print("Changed file")

            # Atualiza a lista inicial
            initial_files = current_files

            # Fecha a conexão para escutar alterações
            client_changes.close()

            # Aceita conexões para receber arquivos
            client_receive, addr_receive = server_socket_receive.accept()
            print(f"Conexão estabelecida para receber arquivos com {addr_receive}")

            # Recebe o IP da máquina que está sincronizando
            sync_ip = addr_receive[0]
            print(f"IP da máquina que está sincronizando: {sync_ip}")

            # Recebe o arquivo enviado pela outra máquina
            with open(os.path.join(monitored_directory, "received_file.txt"), "wb") as f:
                while True:
                    data = client_receive.recv(1024)
                    if not data:
                        break
                    f.write(data)

            print("Arquivo recebido com sucesso.")

            # Fecha a conexão para receber arquivos
            client_receive.close()

    except Exception as e:
        print(f"Erro no servidor: {e}")

    finally:
        # Fecha os sockets
        server_socket_changes.close()
        server_socket_receive.close()

if __name__ == "__main__":
    monitor_directory()
