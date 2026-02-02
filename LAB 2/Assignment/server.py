import socket
import threading
from datetime import datetime


def handle_arithmetic(operation, operands):
    """Process arithmetic operations"""
    try:
        num1, num2 = float(operands[0]), float(operands[1])

        if operation == "add":
            result = num1 + num2
        elif operation == "sub":
            result = num1 - num2
        elif operation == "mul":
            result = num1 * num2
        elif operation == "div":
            if num2 == 0:
                return "Error: Division by zero"
            result = num1 / num2
        else:
            return "Error: Unknown arithmetic operation"

        return f"Result: {result}"
    except (ValueError, IndexError):
        return "Error: Invalid operands for arithmetic operation"


def handle_string_analysis(text):
    """Analyze string: convert to uppercase and count characters and words"""
    uppercase_text = text.upper()
    char_count = len(text)
    word_count = len(text.split())

    return f"Uppercase: {uppercase_text}\nCharacter Count: {char_count}\nWord Count: {word_count}"


def process_request(request):
    """Parse and process client request"""
    parts = request.strip().split(maxsplit=1)

    if not parts:
        return "Error: Empty request"

    command = parts[0].lower()

    # Arithmetic operations
    if command in ["add", "sub", "mul", "div"]:
        if len(parts) < 2:
            return "Error: Missing operands"
        try:
            operands = parts[1].split()
            if len(operands) < 2:
                return "Error: Need two operands"
            return handle_arithmetic(command, operands)
        except Exception as e:
            return f"Error: {str(e)}"

    # String analysis
    elif command == "analyze":
        if len(parts) < 2:
            return "Error: Missing text to analyze"
        return handle_string_analysis(parts[1])

    else:
        return "Error: Unknown command. Use 'add', 'sub', 'mul', 'div', or 'analyze'"


def handle_client(conn, addr, server_id):
    """Handle individual client connection"""
    print(
        f"[Server {server_id}][{datetime.now().strftime('%H:%M:%S')}] Client connected: {addr}")

    try:
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break

                request = data.decode('utf-8', errors='ignore').strip()
                print(
                    f"[Server {server_id}][{datetime.now().strftime('%H:%M:%S')}] Request from {addr}: {request}")

                # Process the request
                response = process_request(request)

                # Send response back to client
                conn.sendall(response.encode('utf-8'))

    except Exception as e:
        print(f"[Server {server_id}] Error with client {addr}: {e}")
    finally:
        print(
            f"[Server {server_id}][{datetime.now().strftime('%H:%M:%S')}] Client disconnected: {addr}")


def start_server(port, server_id):
    """Start a single server instance on a specific port"""
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('127.0.0.1', port))
        server_socket.listen(5)

        print(f"[Server {server_id}] Started on port {port}")

        while True:
            conn, addr = server_socket.accept()
            # Create a new thread for each client connection
            client_thread = threading.Thread(
                target=handle_client,
                args=(conn, addr, server_id),
                daemon=True
            )
            client_thread.start()

    except Exception as e:
        print(f"[Server {server_id}] Error: {e}")


def main():
    """Launch multiple servers on different ports"""
    # Define server configurations: (port, server_id)
    server_configs = [
        (5001, "A"),
        (5002, "B"),
        (5003, "C")
    ]

    print("=" * 60)
    print("Multi-Server System Starting...")
    print("=" * 60)

    # Create and start threads for each server
    server_threads = []
    for port, server_id in server_configs:
        thread = threading.Thread(
            target=start_server,
            args=(port, server_id),
            daemon=True
        )
        thread.start()
        server_threads.append(thread)

    print("\nAll servers are running. Press Ctrl+C to stop.\n")

    try:
        # Keep the main thread alive
        for thread in server_threads:
            thread.join()
    except KeyboardInterrupt:
        print("\n\nShutting down all servers...")
        print("Goodbye!")


if __name__ == "__main__":
    main()
