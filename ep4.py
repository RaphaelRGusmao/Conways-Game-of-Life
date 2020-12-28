################################################################################
#                                IME-USP (2016)                                #
#                   MAC0110 - Introducao a Computacao - EP4                    #
#                                                                              #
#                            Conway's Game of Life                             #
#                                                                              #
#                              Raphael R. Gusmao                               #
################################################################################

import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import math

################################################################################
def leEntrada(nome):
    tipoGrade = -1 # Tipo de grade (0 = grade quadrada, 1 = grade hexagonal)
    listaPosicoes = set() # Conjunto de posicoes das celulas vivas (par ordenado)

    # Le o arquivo
    with open(nome,"r") as file:
        # Identifica o tipo de grade
        tipoGrade = 1 if (file.readline().strip() == 'H') else 0
        # Adiciona as coordenadas no conjunto de posicoes
        for linha in file :
            listaPosicoes.add(tuple(map(int, linha.strip().split(','))))

    return tipoGrade, list(listaPosicoes)

################################################################################
def simulaQuad(n,m,lista,t):
    return simulaQuadGenerica(n,m,lista,t,3,23) # N3S23

################################################################################
def simulaHex(n,m,lista,t):
    return simulaHexGenerica(n,m,lista,t,35,2) # N35S2

################################################################################
def desenhaQuad(n,m,lista,figura):
    lista = set(lista) # Transforma a lista em um conjunto

    # Inicializa a figura
    fig = plt.figure(figsize=(m/2, n/2), dpi=72)
    ax = fig.add_subplot(111, xlim=(0,m), ylim=(0,n), aspect='equal')
    ax.set_title("Conway's Game of Life - " + figura)
    plt.axis('off')

    # Inicializa o tabuleiro (cria todas as celulas com a cor padrao)
    tabuleiro = []
    for i in range(n):
        tabuleiro.append([])
        for j in range(m):
            verts = [
                (j  , i  ),
                (j  , i+1),
                (j+1, i+1),
                (j+1, i  ),
                (0,0),
            ]
            codes = [Path.MOVETO,
                     Path.LINETO,
                     Path.LINETO,
                     Path.LINETO,
                     Path.CLOSEPOLY,
            ]
            patch = patches.PathPatch(Path(verts, codes), alpha=0.4, facecolor='white', edgecolor='black', lw=2)
            tabuleiro[i].append(patch)
            ax.add_patch(patch)

    # Pinta as celulas vivas
    for celula in lista:
        lin, col = celula
        if (lin<n and col<m):
            tabuleiro[lin][col].set_facecolor('green')
            tabuleiro[lin][col].set_alpha(1.0)

    # Salva a figura
    plt.savefig(figura + ".png", bbox_inches='tight')

################################################################################
def desenhaHex(n,m,lista,figura):
    lista = set(lista) # Transforma a lista em um conjunto

    # Inicializa a figura
    w = 2/math.sqrt(3) # Largura da celula
    fig = plt.figure(figsize=(m/2, n/2), dpi=72)
    ax = fig.add_subplot(111, xlim=(0,w*(3*m+1)/4), ylim=(0,n+0.55), aspect='equal')
    ax.set_title("Conway's Game of Life - " + figura)
    plt.axis('off')

    # Inicializa o tabuleiro (cria todas as celulas com a cor padrao)
    tabuleiro = []
    for i in range(n):
        tabuleiro.append([])
        for j in range(m):
            verts = [
                (j*w*0.75+w*0.25, i+1  +(0.5 if j%2==0 else 0)),
                (j*w*0.75       , i+0.5+(0.5 if j%2==0 else 0)),
                (j*w*0.75+w*0.25, i    +(0.5 if j%2==0 else 0)),
                (j*w*0.75+w*0.75, i    +(0.5 if j%2==0 else 0)),
                (j*w*0.75+w     , i+0.5+(0.5 if j%2==0 else 0)),
                (j*w*0.75+w*0.75, i+1  +(0.5 if j%2==0 else 0)),
                (0,0),
            ]
            codes = [Path.MOVETO,
                     Path.LINETO,
                     Path.LINETO,
                     Path.LINETO,
                     Path.LINETO,
                     Path.LINETO,
                     Path.CLOSEPOLY,
            ]
            patch = patches.PathPatch(Path(verts, codes), alpha=0.4, facecolor='white', edgecolor='black', lw=2)
            tabuleiro[i].append(patch)
            ax.add_patch(patch)

    # Pinta as celulas vivas
    for celula in lista:
        lin, col = celula
        if (lin<n and col<m):
            tabuleiro[lin][col].set_facecolor('green')
            tabuleiro[lin][col].set_alpha(1.0)

    # Salva a figura
    plt.savefig(figura + ".png", bbox_inches='tight')

################################################################################
# Funcao que gera os vizinhos de uma celula numa grade quadrada
def vizinhosQuad(celula, n, m):
    x, y = celula
    yield x+(1 if x+1<n else 1-n), y
    yield x+(1 if x+1<n else 1-n), y+(1 if y+1<m else 1-m)
    yield x                      , y+(1 if y+1<m else 1-m)
    yield x-(1 if x>0 else 1-n)  , y+(1 if y+1<m else 1-m)
    yield x-(1 if x>0 else 1-n)  , y
    yield x-(1 if x>0 else 1-n)  , y-(1 if y>0 else 1-m)
    yield x                      , y-(1 if y>0 else 1-m)
    yield x+(1 if x+1<n else 1-n), y-(1 if y>0 else 1-m)

################################################################################
# Funcao que gera os vizinhos de uma celula numa grade hexagonal
def vizinhosHex(celula, n, m):
    x, y = celula
    yield x+(1 if x+1<n else 1-n)                   , y
    yield x+(0 if y%2==1 else (1 if x+1<n else 1-n)), y+((1 if y+1<m else 1-m) if m%2==0 else (1 if y+1<=m else 1-m))
    yield x-((1 if x>0 else 1-n) if y%2==1 else 0)  , y+((1 if y+1<m else 1-m) if m%2==0 else (1 if y+1<=m else 1-m))
    yield x-(1 if x>0 else 1-n)                     , y
    yield x-((1 if x>0 else 1-n) if y%2==1 else 0)  , y-((1 if y>0 else 1-m) if m%2==0 else (1 if y>0 else -m))
    yield x+(0 if y%2==1 else (1 if x+1<n else 1-n)), y-((1 if y>0 else 1-m) if m%2==0 else (1 if y>0 else -m))

################################################################################
def simulaQuadGenerica(n,m,lista,t,b,s):
    lista = set(lista) # Transforma a lista em um conjunto
    nasce = list(map(int, str(b))) # Celulas nascem se "nasce" vizinhos estao vivos
    sobrevive = list(map(int, str(s))) # Celulas sobrevivem se "sobrevive" vizinhos estao vivos

    # Garante o posicionamento das celulas vivas (da lista inicial) dentro do tabuleiro
    for celula in lista:
        lin, col = celula
        if (lin>=n or col>=m):
            lista.discard(celula)
            lista.add((lin%n, col%m))

    while (t):
        todosVizinhos = set() # Conjunto de todos os vizinhos de todas as celulas vivas
        celulasParaNascer = set() # Conjunto das celulas que irao nascer
        celulasParaMorrer = set() # Conjunto das celulas que irao morrer

        # Todos os vizinhos de todas as celulas vivas
        for celula in lista:
            for vizinho in vizinhosQuad(celula, n, m):
                todosVizinhos.add(vizinho)

        # Celulas que irao nascer
        for celula in todosVizinhos:
            vizinhosVivos = 0
            for vizinho in vizinhosQuad(celula, n, m):
                if (celula not in lista and vizinho in lista):
                    vizinhosVivos += 1
            for x in nasce:
                if (vizinhosVivos == x):
                    celulasParaNascer.add(celula)
                    break

        # Celulas que irao morrer
        for celula in lista:
            vizinhosVivos = 0
            for vizinho in vizinhosQuad(celula, n, m):
                if (vizinho in lista):
                    vizinhosVivos += 1
            vaiMorrer = True
            for x in sobrevive:
                if (vizinhosVivos == x):
                    vaiMorrer = False
                    break
            if (vaiMorrer):
                celulasParaMorrer.add(celula)

        listaAnterior = lista
        lista = lista - celulasParaMorrer | celulasParaNascer # Celulas morrem e outras nascem

        # Para se a lista for igual a lista anterior (repeticao)
        if (lista == listaAnterior):
            break
        t -= 1 # Proxima iteracao

    return list(lista)

################################################################################
def simulaHexGenerica(n,m,lista,t,b,s):
    lista = set(lista) # Transforma a lista em um conjunto
    nasce = list(map(int, str(b))) # Celulas nascem se "nasce" vizinhos estao vivos
    sobrevive = list(map(int, str(s))) # Celulas sobrevivem se "sobrevive" vizinhos estao vivos

    # Garante o posicionamento das celulas vivas (da lista inicial) dentro do tabuleiro
    for celula in lista:
        lin, col = celula
        if (lin>=n or col>=m):
            lista.discard(celula)
            lista.add((lin%n, col%m))

    while (t):
        todosVizinhos = set() # Conjunto de todos os vizinhos de todas as celulas vivas
        celulasParaNascer = set() # Conjunto das celulas que irao nascer
        celulasParaMorrer = set() # Conjunto das celulas que irao morrer

        # Todos os vizinhos de todas as celulas vivas
        for celula in lista:
            for vizinho in vizinhosHex(celula, n, m):
                todosVizinhos.add(vizinho)

        # Celulas que irao nascer
        for celula in todosVizinhos:
            vizinhosVivos = 0
            for vizinho in vizinhosHex(celula, n, m):
                if (celula not in lista and vizinho in lista):
                    vizinhosVivos += 1
            for x in nasce:
                if (vizinhosVivos == x):
                    celulasParaNascer.add(celula)
                    break

        # Celulas que irao morrer
        for celula in lista:
            vizinhosVivos = 0
            for vizinho in vizinhosHex(celula, n, m):
                if (vizinho in lista):
                    vizinhosVivos += 1
            vaiMorrer = True
            for x in sobrevive:
                if (vizinhosVivos == x):
                    vaiMorrer = False
                    break
            if (vaiMorrer):
                celulasParaMorrer.add(celula)

        listaAnterior = lista
        lista = lista - celulasParaMorrer | celulasParaNascer # Celulas morrem e outras nascem

        # Para se a lista for igual a lista anterior (repeticao)
        if (lista == listaAnterior):
            break
        t -= 1 # Proxima iteracao

    return list(lista)

################################################################################
# Funcao que retorna uma tupla com os elementos da lista normalizados ou seja, a
# celula com menor x,y vai para a posicao 0,0 e as demais celulas a acompanham
def normaliza(lista):
    listaNormal = ()
    lista = sorted(lista)
    linMin, colMin = lista[0]
    for celula in lista:
        x, y = celula
        listaNormal += ((x-linMin, y-colMin),)
    return listaNormal

################################################################################
# Identifica se algum PADRAO se repete pelo menos uma vez em uma quantidade fixa
# de iteracoes na grade quadrada, ou seja, identifica  se  algum  movimento  das
# celulas se repete em qualquer posicao do tabuleiro
def haRepeticoes(n,m,lista,t):
    padroes = set() # Conjunto de padroes
    padroes.add(normaliza(lista)) # Normaliza a lista original e adiciona no conjunto de padroes
    temRepeticoes = False

    while (t):
        lista = simulaQuad(n, m, lista, 1) # Aplica uma iteracao
        if (not lista): # Se a lista estiver vazia e a execucao chegar ate aqui, entao nao ha repeticoes de padrao
            break
        normal = normaliza(lista) # Normaliza a lista
        if (normal in padroes):
            temRepeticoes = True
            break
        padroes.add(normal) # Adiciona o padrao no conjunto de padroes
        t -= 1 # Proxima iteracao

    return temRepeticoes

################################################################################
# Identifica se algum PADRAO se repete pelo menos uma vez em uma quantidade fixa
# de iteracoes na grade hexagonal ou seja, identifica  se  algum  movimento  das
# celulas se repete em qualquer posicao do tabuleiro
def haRepeticoesHex(n,m,lista,t):
    padroes = set() # Conjunto de padroes
    padroes.add(normaliza(lista)) # Normaliza a lista original e adiciona no conjunto de padroes
    temRepeticoes = False

    while (t):
        lista = simulaHex(n, m, lista, 1) # Aplica uma iteracao
        if (not lista): # Se a lista estiver vazia e a execucao chegar ate aqui, entao nao ha repeticoes de padrao
            break
        normal = normaliza(lista) # Normaliza a lista
        if (normal in padroes):
            temRepeticoes = True
            break
        padroes.add(normal) # Adiciona o padrao no conjunto de padroes
        t -= 1 # Proxima iteracao

    return temRepeticoes

################################################################################
# Identifica se algum ESTADO se repete pelo menos uma vez em uma quantidade fixa
# de iteracoes na grade quadrada (Diferente da repeticao de padrao. Neste  caso,
# as celulas precisam  estar  na  mesma  posicao  do  tabuleiro  para  que  haja
# repeticao)
def haRepeticoesEstado(n,m,lista,t):
    estados = set() # Conjunto de estados do jogo
    estados.add(tuple(sorted(lista))) # Adiciona o estado original no conjunto de estados
    temRepeticoes = False

    while (t):
        lista = simulaQuad(n, m, lista, 1) # Aplica uma iteracao
        if (tuple(sorted(lista)) in estados):
            print("repeticao aqui:", t)
            temRepeticoes = True
            break
        estados.add(tuple(sorted(lista))) # Adiciona o estado no conjunto de estados

        t -= 1 # Proxima iteracao

    return temRepeticoes

################################################################################
# Identifica se algum ESTADO se repete pelo menos uma vez em uma quantidade fixa
# de iteracoes na grade hexagonal (Diferente da repeticao de padrao. Neste caso,
# as celulas precisam  estar  na  mesma  posicao  do  tabuleiro  para  que  haja
# repeticao)
def haRepeticoesEstadoHex(n,m,lista,t):
    estados = set() # Conjunto de estados do jogo
    estados.add(tuple(sorted(lista))) # Adiciona o estado original no conjunto de estados
    temRepeticoes = False

    while (t):
        lista = simulaHex(n, m, lista, 1) # Aplica uma iteracao
        if (tuple(sorted(lista)) in estados):
            temRepeticoes = True
            break
        estados.add(tuple(sorted(lista))) # Adiciona o estado no conjunto de estados

        t -= 1 # Proxima iteracao

    return temRepeticoes

################################################################################
def main():
    n = 20 # Linhas
    m = 20 # Colunas
    t = 100 # Iteracoes
    entrada = "inputs/20x20_glider.txt"

    # Le o arquivo de entrada
    tipoGrade, listaPosicoes = leEntrada(entrada)
    print("Lista inicial: ", listaPosicoes)

    # Verifica se ha repeticoes de padrao
    temRepeticoesPadrao = haRepeticoesHex(n, m, listaPosicoes, t) if tipoGrade else haRepeticoes(n, m, listaPosicoes, t)
    print("Nao tem" if not temRepeticoesPadrao else "Tem", "repeticao de PADRAO")

    # Verifica se ha repeticoes de estado
    temRepeticoesEstado = haRepeticoesEstadoHex(n, m, listaPosicoes, t) if tipoGrade else haRepeticoesEstado(n, m, listaPosicoes, t)
    print("Nao tem" if not temRepeticoesEstado else "Tem", "repeticao de ESTADO")

    # Executa as iteracoes
    newLista = simulaHex(n, m, listaPosicoes, t) if tipoGrade else simulaQuad(n, m, listaPosicoes, t)
    print("Lista final: ", newLista)

    # Gera e salva uma figura com o estado do jogo
    nomeFigura = str(n) + "x" + str(m) + ("_hex" if tipoGrade else "_quad") + "_iteracao" + str(t)
    desenhaHex(n, m, newLista, nomeFigura) if tipoGrade else desenhaQuad(n, m, newLista, nomeFigura)

main()
