import socket
import threading

# This function runs in a separate 'thread' for every person who connects
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    
    connected = True
    while connected:
        try:
            # Receive the raw bytes and turn to string
            message = conn.recv(1024).decode()
            
            if not message or message == "DISCONNECT":
                connected = False
                break
            
            print(f"[{addr}] says: {message}")

            # LOGIC: Split the command (e.g., "ADD:5:10" -> ["ADD", "5", "10"])
            parts = message.split(":")
            command = parts[0].upper()

            if command == "ADD":
                result = int(parts[1]) + int(parts[2])
                response = f"Result is: {result}"
            elif command == "SQUARE":
                result = int(parts[1]) ** 2
                response = f"Result is: {result}"
            else:
                response = "Unknown Command! Use ADD:x:y or SQUARE:x"

            # Send the answer back
            conn.send(response.encode())
            
        except:
            # If the client closes the window abruptly
            break

    print(f"[DISCONNECT] {addr} disconnected.")
    conn.close()

# --- Main Server Setup ---
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 12345))
server.listen()

print("Server is LISTENING on Port 12345...")

while True:
    # Wait for a new client
    conn, addr = server.accept()
    
    # Create a new thread to handle this specific person
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
    
    # Print how many active people are talking to the server
    print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")