import socket
import threading
import random

PORT = 12345
LOCAL_IP = "127.0.0.1"
rooms = {}
restaraunt_names = {}
votes = {}

def voting_complete(room_code):
    if room_code in rooms:
        return votes[room_code] == len(rooms[room_code])

def get_restaraunts(room_code):
    if room_code in restaraunt_names:
        return restaraunt_names[room_code]

def concat_restaraunts(restaraunts, room_code):
    if room_code in restaraunt_names:
        votes[room_code] += 1
        restaraunt_names[room_code] += restaraunts

def get_names(room):
    if room not in rooms:
        return []
    names = []
    for (_,name) in rooms[room]:
        names += [name]
    print(names)
    return names

def generate_code():
    return ''.join(random.choices('0123456789', k=6))

def handle_client(client_socket):
    try:
        room_code = client_socket.recv(1024).decode().strip()

        if room_code.lower() == "create":
            room_code = generate_code()
            rooms[room_code] = []
            restaraunt_names[room_code] = []
            votes[room_code] = 0
            client_socket.send(f"ROOM_CREATED:{room_code}".encode())
            print(f"New room created: {room_code}")
        elif room_code in rooms:
            client_socket.send(f"JOIN_SUCCESS:{room_code}".encode())
            print(f"Client joined room: {room_code}")
        else:
            client_socket.send("ERROR:Invalid room code".encode())
            client_socket.close()
            return
        
        name = client_socket.recv(1024).decode().strip()
        if name:
            rooms[room_code].append((client_socket, name))

        print(f"Current rooms: {rooms}")

    except Exception as e:
        print(f"Error: {e}")
    # finally:
    #     # if room_code in rooms and client_socket in rooms[room_code]:
    #     #     rooms[room_code].remove(client_socket)
    #     # client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((LOCAL_IP, PORT))
    server.listen(100)
    print("Server started on port", PORT)

    while True:
        conn, addr = server.accept()
        print(f"New connection from {addr}")
        threading.Thread(target=handle_client, args=(conn,)).start()
