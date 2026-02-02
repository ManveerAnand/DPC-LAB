import socket

# 1. Create the socket (the "phone")
server_socket = socket.socket()

# 2. Bind to an address and port (the "phone number")
# 'localhost' means your own computer, 12345 is the port
server_socket.bind(('localhost', 12345))

# 3. Listen for incoming calls
server_socket.listen(1)
print("Server is waiting for a connection...")

# 4. Accept the connection (pick up the phone)
# This line stops and waits until a client connects
client_conn, addr = server_socket.accept()
print(f"Connected by {addr}")

# 5. Receive the message and decode it from bytes to text
data = client_conn.recv(1024).decode()
print(f"Client sent: {data}")

# 6. Send a response back
response = "Hello Client! I received your message."
client_conn.send(response.encode())

# 7. Close the connection
client_conn.close()
server_socket.close()