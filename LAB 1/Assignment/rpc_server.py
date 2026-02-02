from xmlrpc.server import SimpleXMLRPCServer

def multiply_matrices_rpc(A, B):
    rows_A, cols_A = len(A), len(A[0])
    cols_B = len(B[0])
    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
    return result

server = SimpleXMLRPCServer(("localhost", 8000))
print("RPC Matrix Server running on port 8000...")

# Register the function
server.register_function(multiply_matrices_rpc, "multiply")
server.serve_forever()