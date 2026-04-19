class Process:
    def __init__(self, pid, total_processes):
        self.pid = pid
        # Slide 14: Lamport is a single integer
        self.lamport = 0
        # Slide 16: Vector is an array of N integers initialized to zeros
        self.vector = [0] * total_processes

    def internal_event(self, event_name):
        self.lamport += 1
        self.vector[self.pid] += 1
        self.display(f"Internal ({event_name})")

    def send_event(self, event_name):
        self.lamport += 1
        self.vector[self.pid] += 1
        self.display(f"Send ({event_name})")
        # Return a copy of the clocks to simulate sending them in a message
        return self.lamport, list(self.vector)

    def receive_event(self, event_name, msg_lamport, msg_vector):
        # Slide 14 Rule 3: C(j) = max(C(j), timestamp) + 1
        self.lamport = max(self.lamport, msg_lamport) + 1

        # Slide 16 Rule 4: V[k] = max(V[k], V_msg[k]) for all k
        for k in range(len(self.vector)):
            self.vector[k] = max(self.vector[k], msg_vector[k])
        # Then V[j] = V[j] + 1
        self.vector[self.pid] += 1

        self.display(f"Receive ({event_name})")

    def display(self, action):
        print(
            f"P{self.pid} | {action:<22} | Lamport: {self.lamport} | Vector: {self.vector}")


# --- Run the Scenario ---
if __name__ == "__main__":
    print("--- Logical Clocks Simulation ---")
    p0 = Process(pid=0, total_processes=3)
    p1 = Process(pid=1, total_processes=3)
    p2 = Process(pid=2, total_processes=3)

    # Sequence of Events
    p0.internal_event("Create Order")

    # P0 sends to P1
    l_msg1, v_msg1 = p0.send_event("To P1")
    p1.receive_event("From P0", l_msg1, v_msg1)

    # P1 sends to P2
    l_msg2, v_msg2 = p1.send_event("To P2")
    p2.receive_event("From P1", l_msg2, v_msg2)

    # P0 does something else concurrently
    p0.internal_event("Send Email")
