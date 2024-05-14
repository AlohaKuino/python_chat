import socket
import threading

def handle_client(receive_socket):
    while True:
        try:
            message, client_address = receive_socket.recvfrom(1024)
            print(f"\nReceived message from {client_address}: {message.decode('utf-8')}")
            print_prompt()
        except Exception as e:
            print("Error:", e)

def send_message(send_socket):
    while True:
        print_prompt()
        recipient_ip = input()
        if recipient_ip.lower() == 'bc':
            try:
                print("Enter broadcast message: ", end='')
                message = input()
                message += "    [*]broadcast message"
                send_socket.sendto(message.encode("utf-8"), ('255.255.255.255', my_port))
                print("[*] Broadcast message sent.")
            except Exception as e:
                print("Error:", e)
        else:
            try:
                print("Enter recipient port: ", end='')
                recipient_port = int(input())
                print("Enter message: ", end='')
                message = input()
                send_socket.sendto(message.encode("utf-8"), (recipient_ip, recipient_port))
                print(f"[*] Message sent to {recipient_ip}:{recipient_port}")
            except Exception as e:
                print("Error:", e)

def print_prompt():
    print("\nEnter recipient IP (or 'bc' for broadcast): ", end='')

my_ip = socket.gethostbyname(socket.gethostname())
my_port = int(input("Enter port to listen on: "))

# Socket for receiving messages
receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receive_socket.bind(("", my_port))
print(f"[*] Receiving socket bound on {my_ip}:{my_port}")

# Socket for sending messages
send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
print(f"[*] Sending socket created")

send_thread = threading.Thread(target=send_message, args=(send_socket,))
send_thread.start()

receive_thread = threading.Thread(target=handle_client, args=(receive_socket,))
receive_thread.start()
