"""
CS-302 | Distributed & Parallel Computing Lab Assignment
Distributed Bank Backend - Latency and Inter-Process Communication

Run with:
    mpiexec -n 2 py joint_fd_mpi.py
"""

from mpi4py import MPI
import random
import time

# =============================================================================
#  CONFIGURATION  <-- Change P1 and P2 to your actual phone number digits
# =============================================================================
P1          = 6555      # Last 4 digits of Client 1 (YOUR phone number)
P2          = 5191      # Last 4 digits of Client 2 (PARTNER's phone number)
N_YEARS     = 2         # Timeframe in years
AUDIT_DELAY = 0.002     # Regulatory audit delay per day in seconds (2 ms)
BASE_RATE   = 0.07      # 7.0% annual base interest rate
# =============================================================================


def divider(char="=", width=65):
    print(char * width, flush=True)


def compute_maturity(principal, seed, n_years, node_label):
    """
    Phase 1 + Phase 2:
    Processes compound interest day-by-day with:
      - A unique random market bonus per day (seeded by phone number)
      - A mandatory audit delay each day (simulates cryptographic check)
    """
    random.seed(seed)
    amount     = float(principal)
    total_days = n_years * 365

    print(f"  |  Starting: Principal = ${principal:,.2f}  |  Seed = {seed}  |  Days = {total_days}", flush=True)
    divider("-", 65)

    for day in range(1, total_days + 1):

        # --- Phase 2: Random market fluctuation (unique per node via seed) ---
        bonus      = random.uniform(0.001, 0.009)
        rate_daily = (BASE_RATE + bonus) / 365.0

        # --- Phase 1: Apply daily compound interest ---
        amount *= (1 + rate_daily)

        # --- Phase 1: Mandatory regulatory audit delay ---
        time.sleep(AUDIT_DELAY)

        # Print progress every 30 days and on the final day
        if day % 30 == 0 or day == total_days:
            annual_equiv = (BASE_RATE + bonus) * 100
            print(
                f"  [{node_label}]  Day {day:>4}/{total_days}"
                f"  |  Rate: {annual_equiv:.3f}%"
                f"  |  Balance: ${amount:>12,.4f}",
                flush=True
            )

    divider("-", 65)
    return amount


def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()   # Rank 0 = Node A, Rank 1 = Node B
    size = comm.Get_size()

    # -------------------------------------------------------------------------
    # Validate process count
    # -------------------------------------------------------------------------
    if size != 2:
        if rank == 0:
            print("ERROR: This program requires exactly 2 MPI processes.")
            print("       Run with:  mpiexec -n 2 py joint_fd_mpi.py")
        return

    # -------------------------------------------------------------------------
    # Assign identity based on MPI rank
    # -------------------------------------------------------------------------
    if rank == 0:
        node_label = "Node A"
        principal  = float(P1)
        seed       = P1
    else:
        node_label = "Node B"
        principal  = float(P2)
        seed       = P2

    # -------------------------------------------------------------------------
    # Print header (Node A only, after sync)
    # -------------------------------------------------------------------------
    comm.Barrier()
    if rank == 0:
        divider("=")
        print("        CS-302 | Distributed Bank Backend")
        print("        Joint Fixed Deposit Account Processing")
        divider("=")
        print(f"  Client 1 (Node A)  |  Principal: ${P1:>8,.2f}  |  Seed: {P1}")
        print(f"  Client 2 (Node B)  |  Principal: ${P2:>8,.2f}  |  Seed: {P2}")
        print(f"  Timeframe          |  {N_YEARS} year(s) = {N_YEARS * 365} days")
        print(f"  Base Annual Rate   |  {BASE_RATE*100:.1f}% + random daily bonus (0.1%-0.9%)")
        print(f"  Audit Delay/Day    |  {AUDIT_DELAY*1000:.0f} ms  (regulatory cryptographic check)")
        divider("=")
        print()
        print("  >> PHASE 1 & 2: Both nodes processing transactions in parallel...")
        print()
    comm.Barrier()

    # -------------------------------------------------------------------------
    # PHASE 1 + 2: Each node independently computes its maturity value
    # (Both run simultaneously - this is the parallel processing phase)
    # -------------------------------------------------------------------------
    print(f"[{node_label}] Starting day-by-day compound interest simulation...", flush=True)
    t_start  = time.time()
    maturity = compute_maturity(principal, seed, N_YEARS, node_label)
    elapsed  = time.time() - t_start

    print(
        f"[{node_label}] DONE  |  "
        f"Final Maturity = ${maturity:,.6f}  |  "
        f"Time taken = {elapsed:.2f}s",
        flush=True
    )
    print(flush=True)

    comm.Barrier()

    # -------------------------------------------------------------------------
    # PHASE 3: Inter-Process Communication (Message Passing)
    # Node A and Node B exchange their maturity values via MPI send/recv
    # -------------------------------------------------------------------------
    comm.Barrier()
    if rank == 0:
        print("  >> PHASE 3: Inter-Process Communication (IPC) - Message Passing...")
        print()
    comm.Barrier()

    if rank == 0:
        # Node A: sends MatA to Node B, then waits to receive MatB
        comm.send(maturity, dest=1, tag=10)
        partner_maturity = comm.recv(source=1, tag=20)
        print(f"  [Node A]  Sent    MatA = ${maturity:>14,.6f}  -->  to   Node B", flush=True)
        print(f"  [Node A]  Received MatB = ${partner_maturity:>14,.6f}  <--  from Node B", flush=True)
    else:
        # Node B: receives MatA from Node A first, then sends MatB back
        # (This ordering prevents deadlock)
        partner_maturity = comm.recv(source=0, tag=10)
        comm.send(maturity, dest=0, tag=20)
        print(f"  [Node B]  Received MatA = ${partner_maturity:>14,.6f}  <--  from Node A", flush=True)
        print(f"  [Node B]  Sent    MatB = ${maturity:>14,.6f}  -->  to   Node A", flush=True)

    comm.Barrier()

    # -------------------------------------------------------------------------
    # PHASE 4: Consensus Check
    # Both nodes independently compute the total - they must match exactly
    # -------------------------------------------------------------------------
    total = maturity + partner_maturity

    if rank == 0:
        mat_a = maturity
        mat_b = partner_maturity
    else:
        mat_a = partner_maturity
        mat_b = maturity

    # Gather both computed totals to Node A for verification
    all_totals = comm.gather(total, root=0)

    comm.Barrier()
    if rank == 0:
        print()
        print("  >> PHASE 4: Consensus Check - Verifying both nodes agree on total...")
        print()
    comm.Barrier()

    print(
        f"  [{node_label}]  My total = MatA + MatB = "
        f"${mat_a:,.6f} + ${mat_b:,.6f} = ${total:,.6f}",
        flush=True
    )

    comm.Barrier()

    # -------------------------------------------------------------------------
    # Final Report (Node A prints on behalf of both)
    # -------------------------------------------------------------------------
    if rank == 0:
        consensus_ok = abs(all_totals[0] - all_totals[1]) < 1e-9

        print()
        divider("=")
        print("        JOINT FIXED DEPOSIT - FINAL SETTLEMENT REPORT")
        divider("=")
        print(f"  Client 1 Principal (P1)       : ${P1:>12,.2f}")
        print(f"  Client 2 Principal (P2)       : ${P2:>12,.2f}")
        print(f"  Combined Principal            : ${P1 + P2:>12,.2f}")
        divider("-")
        print(f"  Node A Maturity Value (MatA)  : ${mat_a:>14,.6f}")
        print(f"  Node B Maturity Value (MatB)  : ${mat_b:>14,.6f}")
        divider("-")
        print(f"  Total Maturity (MatA + MatB)  : ${total:>14,.6f}")
        print(f"  Total Interest Earned         : ${total - (P1 + P2):>14,.6f}")
        print(f"  Effective Return              : {((total/(P1+P2))-1)*100:>13,.4f}%")
        divider("-")
        print(f"  Node A computed total         : ${all_totals[0]:>14,.6f}")
        print(f"  Node B computed total         : ${all_totals[1]:>14,.6f}")
        divider("=")

        if consensus_ok:
            print(f"  Node A Final Total : ${all_totals[0]:>14,.6f}")
            print(f"  Node B Final Total : ${all_totals[1]:>14,.6f}")
            divider("-")
            print("  CONSENSUS  : [ACHIEVED] Both nodes agree on the final total.")
            print("  TRANSACTION: [SUCCESS]  Joint FD account has been created.")
        else:
            print(f"  Node A Final Total : ${all_totals[0]:>14,.6f}")
            print(f"  Node B Final Total : ${all_totals[1]:>14,.6f}")
            divider("-")
            print("  CONSENSUS  : [FAILED]   Nodes disagree. Transaction aborted.")

        divider("=")
        print()


if __name__ == "__main__":
    main()