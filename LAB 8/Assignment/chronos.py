import json
import time
import os

# ANSI Color codes for terminal beauty


class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_banner(text):
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.HEADER}  {text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.HEADER}{'='*60}{Colors.RESET}")


def process_messages():
    # Attempt to enable ANSI escape sequences in Windows terminal
    if os.name == 'nt':
        os.system('color')

    print_banner("Project Chronos: When Clocks Lie and Messages Wander")
    print(f"{Colors.CYAN}[*] Reading seed.json...{Colors.RESET}")

    with open("seed.json", "r") as f:
        data = json.load(f)

    theta = data["theta"]
    clocks = data["clocks"]
    queues = data["queues"]

    N = 5

    print(
        f"\n{Colors.BOLD}[Step 1] Initial Clocks & parameters:{Colors.RESET}")
    print(f"  {Colors.BLUE}Clocks:{Colors.RESET} {clocks}")
    print(f"  {Colors.BLUE}Tolerance Threshold (θ):{Colors.RESET} {theta}")

    # --- STEP 1: The Clock Alignment (Fault-Tolerant Berkeley) ---
    print_banner("STEP 1: The Clock Alignment (Fault-Tolerant Berkeley)")
    print(f"{Colors.CYAN}[Node 0] Polling clocks...{Colors.RESET}\n")
    time.sleep(0.5)

    T0 = clocks[0]
    S = []  # Trusted set indices

    for i in range(N):
        diff = abs(clocks[i] - T0)
        if diff <= theta:
            S.append(i)
            print(
                f"  Node {i} (Time {clocks[i]:<4}): {Colors.GREEN}TRUSTED{Colors.RESET} (diff = {diff})")
        else:
            print(
                f"  Node {i} (Time {clocks[i]:<4}): {Colors.RED}IGNORED{Colors.RESET} (diff = {diff} > θ)")
        time.sleep(0.3)

    # Calculate target time using floor division
    T_target = sum(clocks[i] for i in S) // len(S)
    print(
        f"\n{Colors.BOLD}{Colors.YELLOW}[Node 0] Calculated Target Time:{Colors.RESET} {T_target}")
    time.sleep(0.5)

    # Calculate offsets and aligned clocks
    T_sync = clocks.copy()

    print(f"\n{Colors.CYAN}[*] Applying Clock Corrections:{Colors.RESET}")
    for i in range(N):
        if i in S:
            offset = T_target - clocks[i]
            T_sync[i] = clocks[i] + offset
            print(
                f"  Node {i}: {Colors.GREEN}Trusted{Colors.RESET} -> Offset = {offset:>4} | New aligned clock = {Colors.BOLD}{T_sync[i]}{Colors.RESET}")
        else:
            # Ignored: receives 0 offset
            offset = 0
            T_sync[i] = clocks[i] + offset
            print(
                f"  Node {i}: {Colors.RED}Ignored{Colors.RESET} -> Offset = {offset:>4} | Clock remains     = {Colors.BOLD}{T_sync[i]}{Colors.RESET}")
        time.sleep(0.3)

    # --- STEP 2: The Message Ordering ---
    print_banner("STEP 2: Processing Message Queues (Causal Delivery)")

    # Initialize Vector clocks to zero
    V = [[0] * N for _ in range(N)]
    final_payloads = [0] * N

    # Process each node independently
    for i in range(N):
        print(
            f"\n{Colors.BOLD}{Colors.BLUE}[--- Node {i} Wakeup ---]{Colors.RESET}")
        node_queue = queues[i]
        buffer = []

        for idx, msg in enumerate(node_queue):
            sender = msg["sender"]
            v_msg = msg["v_msg"]

            print(
                f"  {Colors.CYAN}Req {idx+1}:{Colors.RESET} Received from Node {sender} with TS: {v_msg}")
            time.sleep(0.25)

            # Check causal conditions
            cond1 = (v_msg[sender] == V[i][sender] + 1)
            cond2 = all(v_msg[k] <= V[i][k] for k in range(N) if k != sender)

            if cond1 and cond2:
                # Process message
                print(
                    f"         {Colors.GREEN}↳ Causal conditions met. Processing.{Colors.RESET}")
                for k in range(N):
                    V[i][k] = max(V[i][k], v_msg[k])
                print(
                    f"         {Colors.BOLD}Node {i} config updated to:{Colors.RESET} {V[i]}")
                time.sleep(0.2)

                # Immediately check buffer
                buffer_checked = True
                while buffer_checked:
                    buffer_checked = False
                    for b_msg in buffer[:]:  # slice to iterate copy while modifying
                        b_sender = b_msg["sender"]
                        b_v_msg = b_msg["v_msg"]

                        b_cond1 = (b_v_msg[b_sender] == V[i][b_sender] + 1)
                        b_cond2 = all(b_v_msg[k] <= V[i][k]
                                      for k in range(N) if k != b_sender)

                        if b_cond1 and b_cond2:
                            print(
                                f"         {Colors.YELLOW}↳ Unleashing buffered msg from Node {b_sender}: {b_v_msg}{Colors.RESET}")
                            for k in range(N):
                                V[i][k] = max(V[i][k], b_v_msg[k])
                            print(
                                f"         {Colors.BOLD}Node {i} config updated to:{Colors.RESET} {V[i]}")
                            buffer.remove(b_msg)
                            buffer_checked = True
                            time.sleep(0.2)
                            break  # restart loop over updated buffer
            else:
                print(
                    f"         {Colors.RED}↳ Causal constraints fail (early arrival). Buffering.{Colors.RESET}")
                buffer.append(msg)
                time.sleep(0.1)

        if len(buffer) > 0:
            print(
                f"  {Colors.RED}Warning:{Colors.RESET} Ended with {len(buffer)} unprocessable messages lingering in buffer.")
        else:
            print(
                f"  {Colors.GREEN}Success:{Colors.RESET} All messages processed and buffer completely emptied.")

        time.sleep(0.3)

        # --- STEP 3: The Final Payload ---
        vector_sum = sum(V[i])
        Pi = (T_sync[i] * vector_sum) % 9973
        final_payloads[i] = Pi

        print(f"  {Colors.BOLD}Final Local Results:{Colors.RESET}")
        print(f"    - Vector Clock: {V[i]} (Sum: {vector_sum})")
        print(f"    - Sync Clock:   {T_sync[i]}")
        print(f"    - Payload:      {Colors.YELLOW}{Pi}{Colors.RESET}")

    print_banner("STEP 3: The Final Payloads")
    print(f"\n{Colors.BOLD}Calculated values to send to Portal:{Colors.RESET}")
    for i, payload in enumerate(final_payloads):
        print(
            f"  Node {i} -> {Colors.GREEN}{Colors.BOLD}{payload:04d}{Colors.RESET}")


if __name__ == "__main__":
    process_messages()
