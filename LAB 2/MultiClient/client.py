import socket
import os

HOST = "127.0.0.1"
PORT = 5000


def main():
    pid = os.getpid()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            print(f"Client PID={pid} connected. Type messages:")
            while True:
                msg = input("> ")
                if not msg:
                    continue
                s.sendall((msg + "\n").encode("utf-8"))
                reply = s.recv(4096).decode("utf-8", errors="ignore")
                print(reply, end="")
        except ConnectionRefusedError:
            print(f"Could not connect to server at {HOST}:{PORT}")
        except KeyboardInterrupt:
            print("\nExiting...")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
