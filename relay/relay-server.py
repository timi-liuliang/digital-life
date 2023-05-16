import socket

# 监听 IP 地址和端口号
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 12345

# 创建 socket 连接
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 绑定服务器地址和端口号
server_socket.bind((SERVER_HOST, SERVER_PORT))

# 开始监听连接
server_socket.listen(1)

print(f"Listening on {SERVER_HOST}:{SERVER_PORT}")

while True:
    # 等待客户端连接
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

    # 接收客户端请求
    request = client_socket.recv(4096)

    # 将请求转发给目标服务器
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as target_socket:
        target_socket.connect(('target_server_host', 80))
        target_socket.sendall(request)

        # 获取目标服务器的响应
        response = target_socket.recv(4096)

    # 将响应发送回客户端
    client_socket.sendall(response)

    # 关闭连接
    client_socket.close()
