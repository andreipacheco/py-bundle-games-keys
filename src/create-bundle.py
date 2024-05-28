import csv
import os
import random

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

# Construindo o caminho completo para o arquivo
nome_arquivo = os.path.join('data', 'games_key.csv')

# Chamando a função para ler o arquivo CSV
linhas = ler_csv(nome_arquivo)

# Filtrando apenas os jogos ativos
jogos_ativos = [jogo for jogo in linhas if jogo['active'].lower() == 'true']

# Verificando se há pelo menos 5 jogos ativos
if len(jogos_ativos) < 5:
    print("Não há jogos ativos suficientes para fazer o sorteio.")
else:
    # Sorteando 5 jogos aleatórios sem repetição
    jogos_sorteados = random.sample(jogos_ativos, 5)

    # Atualizando o status 'active' para 'False' nos jogos sorteados
    for jogo in jogos_sorteados:
        jogo['active'] = 'FALSE'

    # Chamando a função para escrever as alterações no arquivo CSV
    escrever_csv(nome_arquivo, linhas)

    print("Jogos sorteados para o bundle:")
    # Imprimindo os jogos sorteados
    for jogo in jogos_sorteados:
        print(jogo)
