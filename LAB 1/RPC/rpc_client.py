import xmlrpc.client

# Create a connection to the RPC server
proxy = xmlrpc.client.ServerProxy("http://127.0.0.1:6000/")

while True:
    print("\nChoose: palindrome / armstrong / exit")
    op = input("Enter choice: ").strip().lower()

    if op == "exit":
        print("Exiting program.")
        break

    if op not in ("palindrome", "armstrong"):
        print("Invalid choice, try again.")
        continue

    num = input("Enter number: ").strip()
    if not num.isdigit():
        print("Only digits allowed.")
        continue

    # Convert the string input to an integer
    num = int(num)

    # Call the function on the server as if it were local
    result = proxy.check(op, num)

    # Display results
    if op == "palindrome":
        print("Palindrome result:", "YES" if result else "NO")
    else:
        print("Armstrong result:", "YES" if result else "NO")