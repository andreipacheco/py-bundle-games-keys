import csv
import os
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Função para ler e imprimir as linhas do arquivo CSV
def ler_csv(caminho_arquivo):
    try:
        with open(caminho_arquivo, newline='') as arquivo_csv:
            leitor_csv = csv.DictReader(arquivo_csv)
            # Retornando todas as linhas como uma lista de dicionários
            return list(leitor_csv)
    except FileNotFoundError:
        print(f"O arquivo {caminho_arquivo} não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# Função para escrever as linhas atualizadas no arquivo CSV
def escrever_csv(caminho_arquivo, linhas):
    try:
        with open(caminho_arquivo, 'w', newline='') as arquivo_csv:
            escritor_csv = csv.DictWriter(arquivo_csv, fieldnames=linhas[0].keys())
            escritor_csv.writeheader()
            escritor_csv.writerows(linhas)
    except Exception as e:
        print(f"Ocorreu um erro ao escrever no arquivo CSV: {e}")

# Função para enviar email com o resultado do sorteio
def enviar_email(destinatario, assunto, corpo):
    remetente = 'seu_email@gmail.com'  # Substitua pelo seu endereço de email completo
    # Habilitar 2-Step Verification
    # Sign in with app passwords https://support.google.com/accounts/answer/185833?hl=en
    senha = 'sua_senha_de_aplicativo'  # Substitua pela sua senha de aplicativo

    # Configuração do servidor SMTP do Gmail
    servidor_smtp = 'smtp.gmail.com'
    porta_smtp = 587

    # Criando o objeto do email
    mensagem = MIMEMultipart()
    mensagem['From'] = remetente
    mensagem['To'] = destinatario
    mensagem['Subject'] = assunto

    # Adicionando o corpo do email
    mensagem.attach(MIMEText(corpo, 'plain'))

    # Iniciando a conexão com o servidor SMTP
    servidor = smtplib.SMTP(servidor_smtp, porta_smtp)
    servidor.starttls()

    try:
        # Login no servidor SMTP com a senha de aplicativo
        servidor.login(remetente, senha)

        # Enviando o email
        servidor.send_message(mensagem)

        # Log de email enviado com sucesso
        print("Email enviado com sucesso para:", destinatario)

    except smtplib.SMTPException as e:
        print("Erro ao enviar o email:", e)
        print("Resultado do bundle:")
        print(corpo)
    finally:
        # Fechando a conexão com o servidor SMTP
        servidor.quit()

# Construindo o caminho completo para o arquivo
nome_arquivo = os.path.join('data', 'games_key.csv')

# Chamando a função para ler o arquivo CSV
linhas = ler_csv(nome_arquivo)

# Verificando se há pelo menos 5 jogos ativos
jogos_ativos = [jogo for jogo in linhas if 'active' in jogo and jogo['active'].lower() == 'true']

if len(jogos_ativos) < 5:
    print("Não há jogos ativos suficientes para fazer o sorteio.")
else:
    # Sorteando 5 jogos aleatórios sem repetição
    jogos_sorteados = []
    jogos_sorteados_nomes = set()

    while len(jogos_sorteados) < 5:
        jogo_sorteado = random.choice(jogos_ativos)
        if jogo_sorteado['game'] not in jogos_sorteados_nomes:
            jogos_sorteados.append(jogo_sorteado)
            jogos_sorteados_nomes.add(jogo_sorteado['game'])
            for linha in linhas:
                if linha['game'] == jogo_sorteado['game'] and linha['key'] == jogo_sorteado['key']:
                    linha['active'] = 'FALSE'

    # Chamando a função para escrever as alterações no arquivo CSV
    escrever_csv(nome_arquivo, linhas)

    # Formatando os jogos sorteados para o corpo do email
    corpo_email = 'Jogos sorteados para o bundle:\n'
    for jogo in jogos_sorteados:
        corpo_email += f"{jogo['game']}: {jogo['key']}\n"

    # Mostrando o resultado do bundle
    print("Resultado do bundle:")
    print(corpo_email)

    # Enviando email com o resultado do sorteio
    destinatario = 'destinatario_email@gmail.com'  # Substitua pelo endereço de email do destinatário do email
    assunto = 'Resultado do sorteio do bundle de jogos'
    enviar_email(destinatario, assunto, corpo_email)
