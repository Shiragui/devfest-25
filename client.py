import socket

IP_ADDR = "127.0.0.1"
PORT = 12345

def run_client(action, room_code=""):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((IP_ADDR, PORT))

    if action == "create":
        server.send("create".encode())
    elif action == "join":
        server.send(room_code.encode())

    response = server.recv(1024).decode()
    
    if response.startswith("ROOM_CREATED"):
        return response.split(":")[1]
    elif response.startswith("JOIN_SUCCESS"):
        return response.split(":")[1]  
    else:
        print(response)
        return None
