import socket

# 1. Create the socket
client_socket = socket.socket()

# 2. Connect to the server's address and port
client_socket.connect(('localhost', 12345))

# 3. Send a message (must be encoded to bytes!)
message = "Hello Server! Can you hear me?"
client_socket.send(message.encode())

# 4. Receive the server's reply and decode it
reply = client_socket.recv(1024).decode()
print(f"Server replied: {reply}")

# 5. Close the socket
client_socket.close()