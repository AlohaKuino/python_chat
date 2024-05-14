import socket
import threading

def handle_client(server_socket):
    while True:
        try:
            message, client_address = server_socket.recvfrom(1024)
            print(f"Received message from {client_address}: {message.decode('utf-8')}")
        except Exception as e:
            print("Error:", e)

def send_message(server_socket):
    while True:
        recipient_ip = input("Enter recipient IP (or 'bc' for broadcast): ")
        if recipient_ip.lower() == 'bc':
            try:
                message = input("Enter broadcast message: ")
                server_socket.sendto(message.encode("utf-8"), ('255.255.255.255', my_port))
            except Exception as e:
                print("Error:", e)
        else:
            recipient_port = int(input("Enter recipient port: "))
            message = input("Enter message: ")
            server_socket.sendto(message.encode("utf-8"), (recipient_ip, recipient_port))


my_ip = socket.gethostbyname(socket.gethostname())
my_port = int(input("Enter port to listen on: "))

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
server_socket.bind((my_ip, my_port))
print(f"[*] Server started on {my_ip}:{my_port}")

send_thread = threading.Thread(target=send_message, args=(server_socket,))
send_thread.start()

receive_thread = threading.Thread(target=handle_client, args=(server_socket,))
receive_thread.start()
