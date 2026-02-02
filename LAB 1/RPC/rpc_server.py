from xmlrpc.server import SimpleXMLRPCServer

# Function to check if a number is a palindrome
def is_palindrome(n):
    s = str(n)
    return s == s[::-1]

# Function to check if a number is an Armstrong number
def is_armstrong(n):
    s = str(n)
    power = len(s)
    total = sum(int(d) ** power for d in s)
    return total == n

# Dispatcher function to call the correct check based on user input
def check(operation, number):
    if operation == "palindrome":
        return is_palindrome(number)
    elif operation == "armstrong":
        return is_armstrong(number)
    else:
        return None

# Initialize the server on all available IPs at port 6000
server = SimpleXMLRPCServer(("0.0.0.0", 6000))
print("RPC Server running...")

# Register the 'check' function so clients can call it
server.register_function(check, "check")

# Keep the server running to handle incoming requests
server.serve_forever()