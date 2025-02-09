import socket
import threading
import random

PORT = 12345
LOCAL_IP = "127.0.0.1"
rooms = {}

def generate_code():
    return ''.join(random.choices('0123456789', k=6))

def handle_client(client_socket):
    try:
        room_code = client_socket.recv(1024).decode().strip()

        if room_code.lower() == "create":
            room_code = generate_code()
            rooms[room_code] = []
            client_socket.send(f"ROOM_CREATED:{room_code}".encode())
            print(f"New room created: {room_code}")
        elif room_code in rooms:
            rooms[room_code].append(client_socket)
            client_socket.send(f"JOIN_SUCCESS:{room_code}".encode())
            print(f"Client joined room: {room_code}")
        else:
            client_socket.send("ERROR:Invalid room code".encode())
            client_socket.close()
            return

        rooms[room_code].append(client_socket)

        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            # Broadcast the message to all clients in the same room
            for client in rooms[room_code]:
                if client != client_socket:
                    client.send(message.encode())

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if room_code in rooms and client_socket in rooms[room_code]:
            rooms[room_code].remove(client_socket)
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((LOCAL_IP, PORT))
    server.listen(100)
    print("Server started on port", PORT)

    while True:
        conn, addr = server.accept()
        print(f"New connection from {addr}")
        threading.Thread(target=handle_client, args=(conn,)).start()
