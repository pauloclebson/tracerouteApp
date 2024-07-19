import tkinter as tk
from tkinter import scrolledtext, ttk
import socket
import struct
import time
import threading

# Variável global para controlar o estado de execução do traceroute
parar_traceroute = False

# Calcular o checksum do ICMP
def calcular_checksum(dados_fonte):
    soma = 0
    tamanho = len(dados_fonte)

    # Os dados são divididos em palavras de 16 bits. Se o número total de bytes não for par, um byte extra é adicionado ao final para completar a última palavra.

    # Soma os 16 bits
    for i in range(0, tamanho - 1, 2):
        soma += (dados_fonte[i] << 8) + dados_fonte[i + 1]
        soma = (soma & 0xffff) + (soma >> 16)

    # Adiciona o último byte se o comprimento for ímpar
    if tamanho % 2 != 0:
        soma += dados_fonte[-1]
        soma = (soma & 0xffff) + (soma >> 16)

    soma = ~soma & 0xffff
    return soma

# Função para verificar o ping.
def criar_pacote(id):
    cabecalho = struct.pack('bbHHh', 8, 0, 0, id, 1)
    dados = struct.pack('d', time.time())  # Dados do pacote (timestamp atual)
    valor_checksum = calcular_checksum(cabecalho + dados)  # Calcula o checksum
    cabecalho = struct.pack('bbHHh', 8, 0, socket.htons(valor_checksum), id, 1)  # Reconstrói o cabeçalho com o checksum correto
    return cabecalho + dados

# Função para executar o traceroute
def executar_traceroute(destino, area_texto, max_saltos=30, tempo_limite=2):
    global parar_traceroute
    try:
        endereco_destino = socket.gethostbyname(destino)
    except socket.gaierror:
        inserir_texto(area_texto, f"IP ou hostname inválido: {destino}\n")
        return

    icmp = socket.getprotobyname('icmp')  # Obtém o protocolo ICMP

    ttl = 1
    while ttl <= max_saltos and not parar_traceroute:  # Continua até o máximo de saltos ou até parar
        try:
            socket_receptor = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)  #socket para recebimento
            socket_envio = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)  #socket para envio
            socket_envio.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, struct.pack('I', ttl))  # Define a opção de TTL no socket de envio

            pacote = criar_pacote(ttl)
            socket_receptor.settimeout(tempo_limite)  # Define o tempo limite para o socket de recepção
            socket_receptor.bind(("", 0))  # Liga o socket de recepção a qualquer endereço

            tempo_envio = time.time()  # Captura o tempo de envio do pacote ICMP
            socket_envio.sendto(pacote, (endereco_destino, 0))  # Envia o pacote ICMP para o destino

            try:
                receber_dados, endereco_atual = socket_receptor.recvfrom(512)  # Tenta receber a resposta ICMP
                tempo_recebimento = time.time()  # Captura o tempo de recebimento da resposta ICMP
                rtt = (tempo_recebimento - tempo_envio) * 1000  # Calcula o RTT em milissegundos

                endereco_atual = endereco_atual[0]  # Obtém o endereço atual

                try:
                    nome_atual = socket.gethostbyaddr(endereco_atual)[0]
                except socket.error:
                    nome_atual = endereco_atual

                host_atual = f"{nome_atual} ({endereco_atual}) - {rtt:.1f} ms"
                inserir_texto(area_texto, f"{ttl}\t{host_atual}\n")

                if endereco_atual == endereco_destino:
                    break  # Sai do loop se chegou ao destino final

            except socket.timeout:
                inserir_texto(area_texto, f"{ttl}\t* * *\n")  #Caso n ache o ip insere 3 *

            # Finaliza os socktes de envio e recepção
            finally:
                socket_envio.close()
                socket_receptor.close()

        except Exception as e:
            inserir_texto(area_texto, f"Ocorreu uma exceção: {e}\n")  # Em caso de exceção, insere a mensagem de erro na área de texto

        ttl += 1

# Função para inserir texto na área de texto
def inserir_texto(area_texto, texto):
    area_texto.configure(state='normal')
    area_texto.insert(tk.END, texto)
    area_texto.configure(state='disabled')

# Função para iniciar o traceroute em uma thread separada
def iniciar_traceroute(entrada_destino, area_texto, rotulo_status):
    global parar_traceroute
    parar_traceroute = False  # Define para não parar o traceroute
    destino = entrada_destino.get().strip()  # Obtém o nome do destino
    if not destino:
        rotulo_status.config(text="Digite um IP ou hostname válido.")
        return

    area_texto.configure(state='normal')
    area_texto.delete('1.0', tk.END)
    area_texto.configure(state='disabled')
    rotulo_status.config(text="Traceroute iniciado.")
    threading.Thread(target=executar_traceroute, args=(destino, area_texto)).start()  # Inicia uma nova thread para o traceroute

# Função para parar o traceroute
def parar_traceroute_func(rotulo_status):
    global parar_traceroute
    parar_traceroute = True
    rotulo_status.config(text="Traceroute parado.")

# Função para iniciar o traceroute ao pressionar a tecla Enter
def ao_pressionar_enter(evento, entrada_destino, area_texto, rotulo_status):
    iniciar_traceroute(entrada_destino, area_texto, rotulo_status)

# Função para limpar a área de texto e o campo de entrada
def limpar_area_texto(area_texto, entrada_destino):
    area_texto.configure(state='normal')
    area_texto.delete('1.0', tk.END)
    area_texto.configure(state='disabled')
    entrada_destino.delete(0, tk.END)

# Função para criar a interface gráfica
def criar_interface_grafica():
    janela = tk.Tk()
    janela.title("Traceroute APP")

    frame = ttk.Frame(janela, padding="10 10 10 10")
    frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    rotulo_destino = ttk.Label(frame, text="Digite o IP ou hostname para tracar a rota:")
    rotulo_destino.grid(column=0, row=0, columnspan=2, sticky=(tk.W, tk.E))

    entrada_destino = ttk.Entry(frame, width=50)
    entrada_destino.grid(column=0, row=1, columnspan=2, sticky=(tk.W, tk.E))

    entrada_destino.bind("<Return>", lambda evento: ao_pressionar_enter(evento, entrada_destino, area_texto, rotulo_status))

    frame_botoes = ttk.Frame(frame)
    frame_botoes.grid(column=0, row=2, columnspan=2, pady=10, sticky=(tk.W, tk.E))

    botao_iniciar = ttk.Button(frame_botoes, text="Iniciar Traceroute", command=lambda: iniciar_traceroute(entrada_destino, area_texto, rotulo_status))
    botao_iniciar.pack(side=tk.LEFT, padx=5)

    botao_parar = ttk.Button(frame_botoes, text="Parar Traceroute", command=lambda: parar_traceroute_func(rotulo_status))
    botao_parar.pack(side=tk.LEFT, padx=5)

    botao_limpar = ttk.Button(frame_botoes, text="Limpar Pesquisa", command=lambda: limpar_area_texto(area_texto, entrada_destino))
    botao_limpar.pack(side=tk.LEFT, padx=5)

    area_texto = scrolledtext.ScrolledText(janela, width=70, height=20, state='disabled')
    area_texto.grid(column=0, row=1, sticky=(tk.W, tk.E), padx=10, pady=10)

    rotulo_status = ttk.Label(janela, text="")
    rotulo_status.grid(column=0, row=2, pady=5, sticky=(tk.W, tk.E))

    for child in frame.winfo_children():
        child.grid_configure(padx=5, pady=5)

    janela.mainloop()

if __name__ == "__main__":
    criar_interface_grafica()
