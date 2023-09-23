import socket
import threading

SERVER_IP = "localhost"
SERVER_PORT = 8080
BYTES_TO_READ = 4096

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # allows previous socket addresses to be reused immediately
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((SERVER_IP, SERVER_PORT))
        s.listen(1)
        conn, addr = s.accept()
        handle_connection(conn, addr)
        s.close()

def start_threaded_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # allows previous socket addresses to be reused immediately
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((SERVER_IP, SERVER_PORT))
        s.listen(5)
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_connection, args=(conn, addr))
            thread.start()
    
def handle_connection(conn, addr):
    HOST = "www.google.com"
    PORT = 80
    with conn:
        print('Connected by', addr)
        client_request = b""
        # Receives data from proxy client
        while True:
            data = conn.recv(BYTES_TO_READ)
            client_request += data
            if not data:
                break
        # Forwards traffic to google
        server_response = send_request(HOST, PORT, client_request)
        # Returns google's response to proxy client
        conn.sendall(server_response)

def send_request(host, port, request):
    request = b"GET / HTTP/1.1\r\nHost:" + host.encode('utf-8') + b"\r\n\r\n"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_server:
        proxy_server.connect((host, port))
        proxy_server.sendall(request)
        proxy_server.shutdown(socket.SHUT_WR)
        response = b""
        while True:
            chunk = proxy_server.recv(BYTES_TO_READ)
            response += chunk
            if len(chunk) == 0:
                break
        proxy_server.close()
        return response

# start_server()
start_threaded_server()
