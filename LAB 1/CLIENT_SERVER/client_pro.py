import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 12345))

print("Connected! Commands: ADD:x:y, SQUARE:x, DISCONNECT")

while True:
    msg = input("Enter command: ")
    client.send(msg.encode())

    if msg == "DISCONNECT":
        break

    # Wait for the server's answer
    reply = client.recv(1024).decode()
    print(f"Server says: {reply}")

client.close()