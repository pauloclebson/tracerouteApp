
# Traceroute APP

Projeto desenvolvido na disciplina de Redes de Computadores.

## Equipe
- Iris Mayara
- Joberval
- Paulo Clebson

## Descrição
Este projeto tem como objetivo construir uma ferramenta de traceroute com interface gráfica utilizando Python e Tkinter. O traceroute é utilizado para rastrear a rota que os pacotes de rede seguem de um computador para outro através de uma rede.

## Funcionalidades
1. **Leitura do Host**: O usuário pode inserir um endereço IP ou hostname na interface gráfica.
2. **Criação de Sockets**: Dois sockets são criados, um para enviar pacotes ICMP e outro para receber as respostas ICMP.
3. **Envio de Pacotes**: Pacotes ICMP são enviados com TTL (Time To Live) incremental para determinar o caminho até o destino.
4. **Exibição de Resultados**: Os resultados são exibidos na interface gráfica, mostrando cada salto, o endereço IP, o nome do host (se disponível) e a latência.

## Como Executar
1. **Pré-requisitos**:
   - Este projeto deve ser executado em um ambiente Linux ou Windows Subsystem for Linux (WSL).
   - Python 3.x
   - Tkinter (normalmente incluído na instalação padrão do Python)

2. **Clonar o Repositório**:
   ```sh
   git clone https://github.com/pauloclebson/tracerouteApp.git
   cd tracerouteApp
   ```

3. **Executar o Script**:
   ```sh
   sudo python3 traceroute_app.py
   ```
   obs: tem que executar como administrador usando o comando sudo.

4. **Uso da Interface**:
   - Insira o endereço IP ou hostname no campo de entrada.
   - Clique em "Iniciar Traceroute" para iniciar o rastreamento.
   - Clique em "Parar Traceroute" para interromper o rastreamento.
   - Clique em "Limpar Pesquisa" para limpar os resultados e o campo de entrada.

## Estrutura do Código
- `traceroute_app.py`: Script principal que contém a lógica do traceroute e a interface gráfica.
- `README.md`: Documentação do projeto.

## Contribuidores
- Iris Mayara
- Joberval
- Paulo Clebson
