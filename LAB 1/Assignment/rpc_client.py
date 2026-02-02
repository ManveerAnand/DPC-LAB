import xmlrpc.client

A = [[2, 0, 1], [3, 4, 2], [1, 2, 3]]
B = [[1, 2, 3], [0, 1, 4], [5, 6, 0]]

proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")

# Call the function directly! [cite: 269]
result = proxy.multiply(A, B)

print("Resultant Matrix from RPC Server:")
for row in result:
    print(row)