import socket
import json

# Testing matrices from assignment [cite: 272, 278]
A = [[2, 0, 1], [3, 4, 2], [1, 2, 3]]
B = [[1, 2, 3], [0, 1, 4], [5, 6, 0]]

client = socket.socket()
client.connect(('localhost', 12345))

# Send both matrices as a JSON string
payload = json.dumps({"A": A, "B": B})
client.send(payload.encode())

# Receive and display the result
response = client.recv(4096).decode()
result = json.loads(response)

print("Resultant Matrix from Socket Server:")
for row in result:
    print(row)

client.close()