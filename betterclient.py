import socket
import threading

# Функция для чтения сообщений от других клиентов
def handle_client(server_socket):
    while True:
        try:
            # Получаем сообщение от клиента
            message, client_address = server_socket.recvfrom(1024)
            print(f"Received message from {client_address}: {message.decode('utf-8')}")
        except Exception as e:
            print("Error:", e)

# Функция для отправки сообщения конкретному клиенту
# Функция для отправки сообщения конкретному клиенту или широковещательного сообщения
def send_message(server_socket):
    while True:
        recipient_ip = input("Enter recipient IP (or 'bc' for broadcast): ")
        if recipient_ip.lower() == 'bc':
            # Если введен 'bc', отправляем широковещательное сообщение
            while True:
                try:
                    message = input("Enter broadcast message: ")
                    # Отправляем сообщение всем устройствам в сети
                    server_socket.sendto(message.encode("utf-8"), ('255.255.255.255', my_port))
                except Exception as e:
                    print("Error:", e)
        else:
            recipient_port = int(input("Enter recipient port: "))
            message = input("Enter message: ")
            # Отправляем сообщение конкретному клиенту
            server_socket.sendto(message.encode("utf-8"), (recipient_ip, recipient_port))


# Получаем свой IP-адрес и порт
my_ip = socket.gethostbyname(socket.gethostname())
my_port = int(input("Enter port to listen on: "))

# Создаем UDP сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Привязываем сокет к своему IP-адресу и порту
server_socket.bind((my_ip, my_port))
print(f"[*] Server started on {my_ip}:{my_port}")

# Запускаем поток для отправки сообщений
send_thread = threading.Thread(target=send_message, args=(server_socket,))
send_thread.start()

# Запускаем поток для чтения сообщений от клиентов
receive_thread = threading.Thread(target=handle_client, args=(server_socket,))
receive_thread.start()
