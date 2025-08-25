import pygame
from collections import deque

VAZIO=0
PAREDE=1
INICIO=2
DESTINO=3
FRONTEIRA=4
VISITADO=5
CAMINHO=6

WHITE=(255,255,255)
BLACK=(0,0,0)
ORANGE=(255,140,0)
RED=(220,20,60)
YELLOW=(255,215,0)
BLUE=(65,105,225)
GREEN=(60,179,113)
GRID=(40,40,40)

estado_cor = {
    VAZIO: WHITE,
    PAREDE: BLACK,
    INICIO: ORANGE,
    DESTINO: RED,
    FRONTEIRA: YELLOW,
    VISITADO: BLUE,
    CAMINHO: GREEN
}

movimentos = [(1, 0), (-1, 0), (0, 1), (0, -1)]


linhas, colunas, celula = 15, 15, 40
largura, altura = colunas*celula, linhas*celula

pygame.init()
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Maze BFS/DFS Visualizer")
clock = pygame.time.Clock()

malha = [[VAZIO for _ in range(colunas)] for _ in range(linhas)]
modo = "parede"     # "parede" | "inicio" | "destino"
inicio = None       # (linha,coluna)
destino = None      # (linha,coluna)

algoritmo = "DFS"
estado_exec = "parado" # "parado" | "rodando" | "reconstruindo"
fronteira = deque()
pai = [[None for _ in range(colunas)] for _ in range(linhas)]
cursor_backtrack = None


"""
    @:param linha - é a mouse_y // celula para encaixar na grid
    @:param coluna - é a mouse_x // celula para encaixar na grid
    verifica se está vazio, se está pinta como preto (PAREDE)
    verifica se é parede, se é pinta como branco (VAZIO)
"""
def cria_parede(linha,coluna):
    if malha[linha][coluna] == VAZIO:
        malha[linha][coluna] = PAREDE
    elif malha[linha][coluna] == PAREDE:
        malha[linha][coluna] = VAZIO
"""
    @:param linha - é a mouse_y // celula para encaixar na grid
    @:param coluna - é a mouse_x // celula para encaixar na grid
    @:param atual - passado como início
    verifica se a célula é uma parede, se sim não permite criar 
    caso o atual seja o início, pinta como branco (VAZIO)
    caso atual seja nem parede e nem início, cria como laranja (INÍCIO)
    
    @:return (linha, coluna) - retorna a linha e a coluna que o início tá localizado 
"""
def cria_inicio(linha,coluna, atual):
    if malha[linha][coluna] == PAREDE:
        return atual
    if atual:
        atual_linha, atual_coluna = atual
        if malha[atual_linha][atual_coluna] == INICIO:
            malha[atual_linha][atual_coluna] = VAZIO
    malha[linha][coluna] = INICIO
    return (linha, coluna)


"""
    @:param linha - é a mouse_y // celula para encaixar na grid
    @:param coluna - é a mouse_x // celula para encaixar na grid
    @:param atual - passado como destino
    verifica se a célula é uma parede, se sim não permite criar 
    caso o atual seja o destino, pinta como branco (VAZIO)
    caso o atual seja nem a parede e nem o destino, cria como vermelho (DESTINO)

    @:return (linha, coluna) - retorna a linha e a coluna que o destino tá localizado 
"""
def cria_destino(linha,coluna, atual):
    if malha[linha][coluna] == PAREDE:
        return atual
    if atual:
        atual_linha, atual_coluna = atual
        if malha[atual_linha][atual_coluna] == DESTINO:
            malha[atual_linha][atual_coluna] = VAZIO
    malha[linha][coluna] = DESTINO
    return (linha, coluna)

"""
    desenha o grid:
    primeiro monta ele
    coloca uma linha fina para demarcar os quadrados
"""
def desenhar():
    for linha in range(linhas):
        for coluna in range(colunas):
            cor = estado_cor[malha[linha][coluna]]
            pygame.draw.rect(tela, cor, (coluna*celula, linha*celula, celula, celula))
    for linha in range(linhas+1):
        y = linha*celula
        pygame.draw.line(tela, GRID, (0,y), (largura,y), 1)
    for coluna in range(colunas+1):
        x = coluna*celula
        pygame.draw.line(tela, GRID, (x,0), (x,altura), 1)
"""
    reinicia o estado da aplicação
    verifica se tem (FRONTEIRA, VISITADO, CAMINHO) na malha, se sim transforma tudo em branco (VAZIO)
    limpa a lista de fronteira
    limpa a lista de pai
    muda o estado para "parado"    
"""
def reinicia_busca():
    global fronteira, pai, cursor_backtrack, estado_exec
    for linha in range(linhas):
        for coluna in range(colunas):
            if malha[linha][coluna] in (FRONTEIRA, VISITADO, CAMINHO):
                malha[linha][coluna] = VAZIO
    fronteira = deque()
    pai = [[None for _ in range(colunas)] for _ in range(linhas)]
    cursor_backtrack = None
    estado_exec = "parado"

"""
    inicia a busca em largura - BFS 
    verifica se o início ou destino são nulos, se sim não inicia
    reinicia a busca
    adiciona o inicio ao final da lista de fronteira 
    muda o estado para rodando
"""
def inicia_bfs():
    global estado_exec
    if inicio is None or destino is None:
        print("Defina INICIO (S) e DESTINO (G) antes de iniciar.")
        return
    reinicia_busca()
    fronteira.append(inicio)
    estado_exec = "rodando"

"""
    executa o algortimo de busca em largura - BFS 
    remove o primeiro elemento da lista fronteira 
    faz distâncias para os movimentos do agente
"""
def passo_bfs():
    global estado_exec, cursor_backtrack
    if estado_exec != "rodando":
        return

    if not fronteira:
        estado_exec = "parado"
        return

    linha, coluna = fronteira.popleft()
    if malha[linha][coluna] == VISITADO:
        return

    if (linha, coluna) == destino or malha[linha][coluna] == DESTINO:
        cursor_backtrack = (linha, coluna)
        estado_exec = "reconstruindo"
        return

    if malha[linha][coluna] not in (INICIO, DESTINO):
        malha[linha][coluna] = VISITADO

    for distancia_linha, distancia_coluna in movimentos:
        nova_linha, nova_coluna = linha + distancia_linha, coluna + distancia_coluna

        if not (0 <= nova_linha < linhas and 0 <= nova_coluna < colunas):
            continue

        if malha[nova_linha][nova_coluna] == PAREDE:
            continue
            
        if malha[nova_linha][nova_coluna] == DESTINO:
            pai[nova_linha][nova_coluna] = (linha, coluna)
            cursor_backtrack = (nova_linha, nova_coluna)
            estado_exec = "reconstruindo"
            return


        if malha[nova_linha][nova_coluna] in (VISITADO, FRONTEIRA, INICIO):
            continue

        pai[nova_linha][nova_coluna] = (linha, coluna)
        fronteira.append((nova_linha, nova_coluna))
        malha[nova_linha][nova_coluna] = FRONTEIRA


"""
    inicia a busca em profundidade - DFS 
    verifica se o início ou destino são nulos, se sim não inicia
    reinicia a busca
    adiciona o inicio ao final da lista de fronteira 
    muda o estado para rodando
"""
def inicia_dfs():
    global estado_exec
    if inicio is None or destino is None:
        print("Defina INICIO (S) e DESTINO (G) antes de iniciar.")
        return
    reinicia_busca()
    fronteira.append(inicio)
    estado_exec = "rodando"

"""
    executa o algortimo de busca em profundidade - DFS 
    remove o primeiro elemento da lista fronteira 
    faz distâncias para os movimentos do agente
"""
def passo_dfs():
    global estado_exec, cursor_backtrack
    if estado_exec != "rodando":
        return

    if not fronteira:
        estado_exec = "parado"
        return

    linha, coluna = fronteira.pop()
    if malha[linha][coluna] == VISITADO:
        return

    if (linha, coluna) == destino or malha[linha][coluna] == DESTINO:
        cursor_backtrack = (linha, coluna)
        estado_exec = "reconstruindo"
        return

    if malha[linha][coluna] not in (INICIO, DESTINO):
        malha[linha][coluna] = VISITADO

    for distancia_linha, distancia_coluna in reversed(movimentos):
        nova_linha, nova_coluna = linha + distancia_linha, coluna + distancia_coluna

        if not (0 <= nova_linha < linhas and 0 <= nova_coluna < colunas):
            continue

        if malha[nova_linha][nova_coluna] == PAREDE:
            continue

        if malha[nova_linha][nova_coluna] == DESTINO:
            pai[nova_linha][nova_coluna] = (linha, coluna)
            cursor_backtrack = (nova_linha, nova_coluna)
            estado_exec = "reconstruindo"
            return

        if malha[nova_linha][nova_coluna] in (VISITADO, FRONTEIRA, INICIO):
            continue

        pai[nova_linha][nova_coluna] = (linha, coluna)
        fronteira.append((nova_linha, nova_coluna))
        malha[nova_linha][nova_coluna] = FRONTEIRA

"""
    executa o caminho de volta para identificar o caminho
    o proximo sempre será o pai da linha e coluna
    para todos os vértices que não são INÍCIO E DESTINO adiciona no caminho
"""
def passo_backtrack():
    global estado_exec, cursor_backtrack

    if estado_exec != "reconstruindo":
        return
    if cursor_backtrack is None:
        estado_exec = "parado"
        return

    linha, coluna = cursor_backtrack

    if (linha, coluna) == inicio:
        estado_exec = "parado"
        return

    proximo = pai[linha][coluna]

    if malha[linha][coluna] not in (INICIO, DESTINO):
        malha[linha][coluna] = CAMINHO

    if proximo is None:
        estado_exec = "parado"
        return

    cursor_backtrack = proximo


rodando = True
while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                if estado_exec == "parado": modo = "parede"
            elif event.key == pygame.K_s:
                if estado_exec == "parado": modo = "inicio"
            elif event.key == pygame.K_g:
                if estado_exec == "parado": modo = "destino"
            elif event.key == pygame.K_b:
                if estado_exec == "parado":
                    if algoritmo == "BFS":
                        inicia_bfs()
                    else :
                        inicia_dfs()
            elif event.key == pygame.K_r:
                reinicia_busca()
            elif event.key == pygame.K_SPACE:
                if estado_exec == "rodando":
                    estado_exec = "parado"
                elif inicio and destino and (fronteira or cursor_backtrack):
                    estado_exec = "rodando"

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and estado_exec == "parado":
            mouse_x, mouse_y = event.pos
            coluna = mouse_x // celula
            linha = mouse_y // celula
            if 0 <= linha < linhas and 0 <= coluna < colunas:
                if modo == "parede":
                    if malha[linha][coluna] not in (INICIO, DESTINO):
                        cria_parede(linha, coluna)
                elif modo == "inicio":
                    if malha[linha][coluna] != DESTINO:
                        inicio = cria_inicio(linha, coluna, inicio)
                        modo = "parede"
                elif modo == "destino":
                    if malha[linha][coluna] != INICIO:
                        destino = cria_destino(linha, coluna, destino)
                        modo = "parede"

    if estado_exec == "rodando":
        try:
            if algoritmo == "BFS":
                passo_bfs()
            else:
                passo_dfs()
        except NotImplementedError:
            estado_exec = "parado"
    elif estado_exec == "reconstruindo":
        try:
            passo_backtrack()
        except NotImplementedError:
            estado_exec = "parado"

    tela.fill(WHITE)
    desenhar()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
