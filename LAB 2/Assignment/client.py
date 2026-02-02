import socket
import sys


def send_request(host, port, request):
    """Connect to server, send request, and get response"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((host, port))
            print(f"Connected to server at {host}:{port}")

            # Send the request
            client_socket.sendall(request.encode('utf-8'))

            # Receive the response
            response = client_socket.recv(
                4096).decode('utf-8', errors='ignore')
            print(f"\nServer Response:\n{response}\n")

    except ConnectionRefusedError:
        print(f"Error: Could not connect to server at {host}:{port}")
        print("Make sure the server is running.")
    except Exception as e:
        print(f"Error: {e}")


def interactive_mode():
    """Interactive client for manual testing"""
    print("=" * 60)
    print("Multi-Server Client - Interactive Mode")
    print("=" * 60)
    print("\nAvailable Commands:")
    print("  Arithmetic: add <num1> <num2>, sub <num1> <num2>")
    print("              mul <num1> <num2>, div <num1> <num2>")
    print("  Analysis:   analyze <text>")
    print("\nAvailable Servers:")
    print("  Port 5001 - Server A")
    print("  Port 5002 - Server B")
    print("  Port 5003 - Server C")
    print("\nType 'quit' to exit\n")

    while True:
        try:
            # Get server port
            port_input = input("Select server port (5001/5002/5003): ").strip()

            if port_input.lower() == 'quit':
                print("Goodbye!")
                break

            try:
                port = int(port_input)
                if port not in [5001, 5002, 5003]:
                    print("Invalid port. Choose from 5001, 5002, or 5003.\n")
                    continue
            except ValueError:
                print("Invalid port number.\n")
                continue

            # Get request
            request = input("Enter command: ").strip()

            if request.lower() == 'quit':
                print("Goodbye!")
                break

            if not request:
                print("Empty request. Try again.\n")
                continue

            # Send request to server
            send_request('127.0.0.1', port, request)

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break


def demo_mode():
    """Run automated demo tests"""
    print("=" * 60)
    print("Multi-Server Client - Demo Mode")
    print("=" * 60)
    print("\nRunning automated tests...\n")

    test_cases = [
        (5001, "add 10 20", "Arithmetic Test (Addition)"),
        (5001, "sub 50 15", "Arithmetic Test (Subtraction)"),
        (5002, "mul 6 7", "Arithmetic Test (Multiplication)"),
        (5002, "div 40 5", "Arithmetic Test (Division)"),
        (5003, "analyze Hello Server Programming", "String Analysis Test"),
        (5001, "div 10 0", "Error Handling Test (Division by Zero)"),
    ]

    for port, request, description in test_cases:
        print(f"\n{'─' * 60}")
        print(f"Test: {description}")
        print(f"Server: Port {port}")
        print(f"Request: {request}")
        print(f"{'─' * 60}")
        send_request('127.0.0.1', port, request)
        input("Press Enter to continue to next test...")


def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo_mode()
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
