import socket
import os
import time

HOST = "127.0.0.1"
PORT = 5000  # Connects to Load Balancer


def main():
    pid = os.getpid()
    print(
        f"Client PID={pid} attempting to connect to Load Balancer at {HOST}:{PORT}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            print(f"Connected! Type messages to see which server handles them.")

            while True:
                msg = input("> ")
                if not msg:
                    continue
                s.sendall((msg + "\n").encode("utf-8"))
                reply = s.recv(4096).decode("utf-8", errors="ignore")
                print(reply, end="")

        except ConnectionRefusedError:
            print(f"Could not connect. Is the Load Balancer running?")
        except KeyboardInterrupt:
            print("\nExiting...")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
