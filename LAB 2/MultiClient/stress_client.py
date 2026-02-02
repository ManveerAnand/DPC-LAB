import socket
import threading
import time

HOST = "127.0.0.1"
PORT = 5000


def one_client(cid: int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        msg = f"Hello from client-{cid}"
        s.sendall((msg + "\n").encode("utf-8"))
        reply = s.recv(4096).decode("utf-8", errors="ignore").strip()
        print(f"[client-{cid}] {reply}")


def main():
    N = 20  # number of clients to simulate
    threads = []
    for i in range(N):
        t = threading.Thread(target=one_client, args=(i,))
        t.start()
        threads.append(t)
        time.sleep(0.02)  # small stagger

    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
