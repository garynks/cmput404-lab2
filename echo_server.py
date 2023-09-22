import socket

HOST = "localhost"
PORT = 8000
BYTES_TO_READ = 4096

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # allows previous socket addresses to be reused immediately
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        conn, addr = s.accept()
        handle_connection(conn, addr)
        s.close()
    
def handle_connection(conn, addr):
    with conn:
        print('Connected by', addr)
        response = b""
        while True:
            data = conn.recv(BYTES_TO_READ)
            response += data
            if not data:
                break
            conn.sendall(data)
        print(response.decode('latin-1'))

start_server()