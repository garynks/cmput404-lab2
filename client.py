import socket

BYTES_TO_READ = 4096
def get(host, port):
    request = b"GET / HTTP/1.1\r\nHost:" + host.encode('utf-8') + b"\r\n\r\n"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(request)
        s.shutdown(socket.SHUT_WR)
        response = b""
        while True:
            chunk = s.recv(BYTES_TO_READ)
            response += chunk
            if len(chunk) == 0:
                break
        s.close()
    print(response.decode('latin-1'))

get("www.google.com", 80)