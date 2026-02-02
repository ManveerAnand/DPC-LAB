import socket
import threading
import json  # Used to convert lists to strings easily

def multiply_matrices(A, B):
    rows_A, cols_A = len(A), len(A[0])
    cols_B = len(B[0])
    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
    return result

def handle_client(conn, addr):
    print(f"Connected to {addr}")
    try:
        # 1. Receive matrix data from client
        data = conn.recv(4096).decode()
        matrices = json.loads(data) # Convert string back to list
        
        A = matrices['A']
        B = matrices['B']
        
        # 2. Calculate result 
        result = multiply_matrices(A, B)
        
        # 3. Send result back [cite: 269]
        conn.send(json.dumps(result).encode())
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

# Main Server Setup
server = socket.socket()
server.bind(('localhost', 12345))
server.listen(5)
print("Socket Matrix Server is running...")

while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
