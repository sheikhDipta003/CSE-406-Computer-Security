import socket
import pickle

## send integers
def send(num):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = "127.0.0.1"
    port = 14000

    server.bind((server_ip, port))
    server.listen(0)

    client_socket, client_address = server.accept()

    response = str(num).encode("utf-8")
    client_socket.send(response)

def receive():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = "127.0.0.1"
    server_port = 14000
    client.connect((server_ip, server_port))
    
    response = client.recv(1024)
    response = response.decode("utf-8")
    
    return int(response)


## send text
def send_text(text):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = "127.0.0.1"
    port = 8000

    server.bind((server_ip, port))
    server.listen(0)

    client_socket, client_address = server.accept()

    response = pickle.dumps(text)
    client_socket.sendall(response)

def receive_text():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = "127.0.0.1"
    server_port = 8000
    client.connect((server_ip, server_port))
    
    response = client.recv(1024)
    response = pickle.loads(response)
    
    return response