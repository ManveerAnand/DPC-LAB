def time_to_seconds(time_str):
    """Helper to convert 'HH:MM:SS' to total seconds."""
    h, m, s = map(int, time_str.split(':'))
    return h * 3600 + m * 60 + s


def seconds_to_time(total_seconds):
    """Helper to convert total seconds back to 'HH:MM:SS'."""
    h = int(total_seconds // 3600)
    m = int((total_seconds % 3600) // 60)
    s = int(total_seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def berkeley_algorithm(clocks):
    print("--- Berkeley Algorithm Simulation ---")

    # Step 1: Convert all times to seconds
    clock_seconds = {node: time_to_seconds(t) for node, t in clocks.items()}

    # Let's use the Master's time as the baseline to find differences
    master_time = clock_seconds["Master"]

    differences = {node: time - master_time for node,
                   time in clock_seconds.items()}

    print("1. Differences from Master (in seconds):")
    for node, diff in differences.items():
        print(f" {node}: {diff:>3} sec ")

    # Step 2: Compute the average difference
    avg_diff = sum(differences.values()) / len(differences)
    print(f"\n2. Average Difference : {avg_diff} sec ")

    target_time_seconds = master_time + avg_diff
    print(f"Target Sync Time : {seconds_to_time(target_time_seconds)}")

    # Step 3: Calculate adjustments and apply them
    print("\n3. Adjustments and Final Clocks :")
    for node in clocks:
        adjustment = target_time_seconds - clock_seconds[node]
        new_time = clock_seconds[node] + adjustment
        print(
            f" {node}: Adjust by {adjustment:>4} sec -> New Time : {seconds_to_time(new_time)}")


if __name__ == "__main__":
    current_clocks = {
        "Master": "10:00:00",
        "Node 1": "10:00:10",
        "Node 2": "09:59:50",
        "Node 3": "10:00:20"
    }
    berkeley_algorithm(current_clocks)
