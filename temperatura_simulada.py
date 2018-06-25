# -*- coding: utf-8 -*-
import sys
import math
import numpy as np
import random
import tabulate as tabela


# Para cada linha do arquivo lido, cria uma tupla do tipo (x,y) e retorna uma lista de tuplas
def lerArquivo(linhas):
    ln = []
    for linha in linhas:
        linha = linha[0:-1].split(' ')
        i = 0
        while i < len(linha):
            linha[i] = float(linha[i])
            i += 1
        ln.append(linha)
    tuplas = []
    i = 0
    while i < len(ln)-1:
        j = 0
        while j < len(ln[i]):
            tuplas.append(tuple((ln[i][j], ln[i+1][j])))
            j += 1
        i += 1
    return tuplas

# Calcula a distância euclidiana entre duas cidades...
def distancia(x, y):
    dist = 0
    i = 0
    while i < len(x):
        dist += math.pow((x[i] - y[i]), 2)
        i += 1
    return math.sqrt(dist)

# Matriz de distâncias
def calculaMatriz(cidades):
    n = len(cidades)
    matriz = np.zeros((n, n))
    i = 0
    while i < n:
        j = 0
        while j < n:
            matriz[i][j] = (distancia(cidades[i], cidades[j]))
            j += 1
        i += 1
    return matriz

# Troca a posição de duas cidades em um estado
def operador1(estado, cidade1, cidade2):
    novo_estado = list(estado)
    indice1 = novo_estado.index(cidade1)
    indice2 = novo_estado.index(cidade2)
    cidade = estado[indice1]
    novo_estado[indice1] = novo_estado[indice2]
    novo_estado[indice2] = cidade
    return novo_estado

# Inverte as posições das cidades em um intervalo
def operador2(estado, cidade1, cidade2):
    novo_estado = list(estado)
    indice1 = novo_estado.index(cidade1)
    indice2 = novo_estado.index(cidade2)
    anterior = list(novo_estado[:indice1])
    posteior = list(novo_estado[(indice2 + 1):])
    trecho = list(novo_estado[indice1:(indice2 + 1)])
    trecho.reverse()
    return list(anterior + trecho + posteior)

# Calcula o custo total de um circuito
def calculaCusto(estado):
    custoPercurso = 0
    cidades = list(estado)
    matriz = calculaMatriz(cidades)
    i = 0
    tamanho = len(cidades)
    while i < tamanho - 1:
        custoPercurso += matriz[i][i + 1]
        i += 1
    return custoPercurso

# Gera os vizinhos do estado passado. De acordo com os operadores
def gerarVizinho(estado, operador):
    tamanho = len(estado)
    lista = []
    if operador == 1:  # Operador 1
        i = 0
        while i < tamanho:
            permu = []
            if i == (tamanho - 1):
                perm = operador1(estado, estado[-1], estado[0])
            else:
                perm = operador1(estado, estado[i], estado[i + 1])
            lista.append(perm)
            i += 1
    else:  # Operador 2
        i = 0
        while i < tamanho:
            permu = []
            if i == (tamanho - 1):
                perm = operador2(estado, estado[0], estado[-1])
            else:
                perm = operador2(estado, estado[i], estado[i + 1])
            lista.append(perm)
            i += 1
    return lista

# Algoritmo para a temperatura simulada.
# Onde f é a função de temperatura, agenda é a função de resfriamento e op é o operador a ser utilizado.
def temperaturaSimulada(estado_inicial, t_inicial, t_final, qtd_iteracoes, f, op, agenda):

    alpha = 0.99995
    T = t_inicial
    S = estado_inicial
    custo_S = calculaCusto(S)
    S_atual = S
    custo_atual = calculaCusto(S_atual)
    iteracoes = 0
    while T > t_final:
        if agenda == 1:  # Forma 1
            iteracoes = qtd_iteracoes
            cont = 1
            while cont <= qtd_iteracoes:
                if op == 1:
                    vizinhos = gerarVizinho(S,1)
                else:
                    vizinhos = gerarVizinho(S, 2)
                selecionado = random.randrange(0,len(vizinhos))
                proximo = vizinhos[selecionado]
                custo_proximo = calculaCusto(proximo)
                variacao_energia = custo_proximo - custo_S
                if variacao_energia < 0:
                    S = proximo
                    custo_S = custo_proximo
                    if custo_proximo < custo_atual:
                        S_atual = proximo
                        custo_atual = custo_proximo
                else:
                    aleatorio = random.uniform(0,1)
                    if f == 1:
                       prob_atual = F1(custo_S, custo_proximo, T)
                    elif f == 2:
                        prob_atual = F2(custo_S, custo_proximo,T)
                    else:
                        prob_atual = F3(custo_S, custo_proximo,T)
                    if aleatorio < prob_atual:
                        S = proximo
                        custo_S = custo_proximo

                print "\nEstado Atual: " + str(S) + "\nCidade: " + str(proximo) + ", Custo: " + str(custo_proximo)
                cont += 1
            T = alpha * T
        else: # Forma 2
            if op == 1:
                vizinhos = gerarVizinho(S, 1)
            else:
                vizinhos = gerarVizinho(S, 2)
            selecionado = random.randrange(0, len(vizinhos))
            proximo = vizinhos[selecionado]
            custo_proximo = calculaCusto(proximo)
            variacao_energia = custo_proximo - custo_S
            if variacao_energia < 0:
                S = proximo
                custo_S = custo_proximo
                if custo_proximo < custo_atual:
                    S_atual = proximo
                    custo_atual = custo_proximo
            else:
                aleatorio = random.uniform(0, 1)
                if f == 1:
                    prob_atual = F1(custo_S, custo_proximo, T)
                elif f == 2:
                    prob_atual = F2(custo_atual, custo_proximo, T)
                else:
                    prob_atual = F3(custo_atual, custo_proximo, T)
                if aleatorio < prob_atual:
                    S = proximo
                    custo_S = custo_proximo

            iteracoes += 1
            print "\nEstado Atual: " + str(S) + "\nCidade: " + str(proximo) + ", Custo: " + str(custo_proximo)
            T = T/(1 + 0.2 * T)

    return  S_atual, calculaCusto(S_atual), iteracoes


# A medida que a temperatura diminui sua probabilidade se
# aproxima de zero, ou seja, menos chances de ser escolhida.
# Critério de aceitação de Boltzmann, primeira função de temperatura.
def F1(p_atual, p_proximo, temperatura):
    if p_proximo > p_atual:
        return  1.0
    #Variação da energia
    dE = abs(p_proximo - p_atual)
    return math.exp(-dE/temperatura)

# Baseada no critério de aceitação de Boltzmann, segunda função de temperatura
def F2(p_atual, p_proximo,temperatura):
    if p_proximo > p_atual:
        return  1.0
    dE = abs(p_proximo - p_atual)
    if dE > 0:
        return math.log10((dE/temperatura))
    else:
        return -1

# Critério de aceitação de Kirkpatrick, terceira função de temperatura.
def F3(p_atual, p_proximo, temperatura):
    if p_proximo < p_atual:
        return  1.0
    dE = abs(p_proximo - p_atual)
    return math.exp(-dE/temperatura)

# Criando arquivo de saida
def escreverArquivo(linha, coluna):
    arquivo = open("saida_1", 'wb')
    arquivo.write((tabela.tabulate(linha, coluna, tablefmt="grid")) + "\n")
    arquivo.close()

# Principal
def main(arg):
    nome_arquivo = arg[0]
    arquivo = open(nome_arquivo, 'r')
    # Cidades do mapa
    mapa = lerArquivo(arquivo.readlines())
    # Estado Incial, Criando o estado inicial c uma permutação aleatória das cidades
    aleatorio = np.random.permutation(len(mapa))
    aleatorio = aleatorio.tolist()
    estadoInicial = []
    for elemento in aleatorio:
        estadoInicial.append(mapa[elemento])



    qtd_iteracoes = 10
    t_inicial = 10
    t_final = 0.2
    linhas = []
    colunas = ["Variacao", "Melhor Caminho", "Custo", "Quantidade de Iteracoes"]

    #Variações
    i = 0
    while i < 20:
        print "\nIteração: " + str(i+1) + " \n"
        j = 0
        while j < 12:
            if j == 0:
                print "\nVariação: " + str(j + 1)
                estado, custo, iteracoes = temperaturaSimulada(estadoInicial, t_inicial, t_final, qtd_iteracoes, 1, 1, 1) # 1°
                linhas.append([j+1, estado, custo, iteracoes])
            elif j == 1:
                print "\nVariação: " + str(j + 1)
                estado, custo, iteracoes = temperaturaSimulada(estadoInicial, t_inicial, t_final, qtd_iteracoes, 1, 1, 2) #2°
                linhas.append([j+1, estado, custo, iteracoes])
            elif j == 2:
                print "\nVariação: " + str(j + 1)
                estado, custo, iteracoes = temperaturaSimulada(estadoInicial, t_inicial, t_final, qtd_iteracoes, 1, 2, 1) #3°
                linhas.append([j+1, estado, custo, iteracoes])
            elif j == 3:
                print "\nVariação: " + str(j + 1)
                estado, custo, iteracoes = temperaturaSimulada(estadoInicial, t_inicial, t_final, qtd_iteracoes, 1, 2, 2) #4°
                linhas.append([j+1, estado, custo, iteracoes])
            elif j == 4:
                print "\nVariação: " + str(j + 1)
                estado, custo, iteracoes = temperaturaSimulada(estadoInicial, t_inicial, t_final, qtd_iteracoes, 2, 1, 1) #5°
                linhas.append([j+1, estado, custo, iteracoes])
            elif j == 5:
                print "\nVariação: " + str(j + 1)
                estado, custo, iteracoes = temperaturaSimulada(estadoInicial, t_inicial, t_final, qtd_iteracoes, 2, 1, 2) #6°
                linhas.append([j+1, estado, custo, iteracoes])
            elif j == 6:
                print "\nVariação: " + str(j + 1)
                estado, custo, iteracoes = temperaturaSimulada(estadoInicial, t_inicial, t_final, qtd_iteracoes, 2, 2, 1) #7°
                linhas.append([j+1, estado, custo, iteracoes])
            elif j == 7:
                print "\nVariação: " + str(j + 1)
                estado, custo, iteracoes = temperaturaSimulada(estadoInicial, t_inicial, t_final, qtd_iteracoes, 2, 2, 2) #8°
                linhas.append([j+1, estado, custo, iteracoes])
            elif j == 8:
                print "\nVariação: " + str(j + 1)
                estado, custo, iteracoes = temperaturaSimulada(estadoInicial, t_inicial, t_final, qtd_iteracoes, 3, 1, 1) #9°
                linhas.append([j+1, estado, custo, iteracoes])
            elif j == 9:
                print "\nVariação: " + str(j + 1)
                estado, custo, iteracoes = temperaturaSimulada(estadoInicial, t_inicial, t_final, qtd_iteracoes, 3, 1, 2) #10°
                linhas.append([j+1, estado, custo, iteracoes])
            elif j == 10:
                print "\nVariação: " + str(j + 1)
                estado, custo, iteracoes = temperaturaSimulada(estadoInicial, t_inicial, t_final, qtd_iteracoes, 3, 2, 1) #11°
                linhas.append([j+1, estado, custo, iteracoes])
            elif j == 11:
                print "\nVariação: " + str(j + 1)
                estado, custo, iteracoes = temperaturaSimulada(estadoInicial, t_inicial, t_final, qtd_iteracoes, 3, 2, 2) #12°
                linhas.append([j+1, estado, custo, iteracoes])
            j += 1
        i += 1

    escreverArquivo(linhas, colunas)



if __name__ == '__main__':
    main(sys.argv[1:3])
