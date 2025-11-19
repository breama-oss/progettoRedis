# Ascolta su 127.0.0.1:6379 e supporta i comandi già definiti

import socket
import threading
from resp import RESPParser, RESPWriter
from commands import execute_command

HOST = "127.0.0.1"
PORT = 6379

def handle_client(conn, addr):
    print(f"[+] New connection from {addr}")
    parser = RESPParser()
    writer = RESPWriter()

    try:
        with conn:
            while True:
                data = conn.recv(4096)
                if not data:
                    break

                try:
                    commands = parser.feed(data)
                    for cmd in commands:
                        try:
                            response = execute_command(cmd)
                            conn.sendall(writer.encode(response))
                        except Exception as e:
                            conn.sendall(writer.encode_error(str(e)))
                except Exception as e:
                    conn.sendall(writer.encode_error(str(e)))
    finally:
        print(f"[-] Connection closed {addr}")

def start_server():
    print(f"MiniRedis AV running on {HOST}:{PORT}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()

if __name__ == "__main__":
    start_server()
