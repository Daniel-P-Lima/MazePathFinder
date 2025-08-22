import  pygame
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


linhas, colunas, celula = 15, 15, 40
largura, altura = colunas*celula, linhas*celula

pygame.init()
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Maze BFS Visualizer")
clock = pygame.time.Clock()

malha = [[VAZIO for _ in range(colunas)] for _ in range(linhas)]
modo = "parede"     # "parede" | "inicio" | "destino"
inicio = None       # (linha,coluna)
destino = None      # (linha,coluna)

algoritmo = "BFS"
estado_exec = "idle" # "idle" | "rodando" | "reconstruindo"
fronteira = deque()
parent = [[None for _ in range(colunas)] for _ in range(linhas)]
cursor_backtrack = None

def cria_parede(linha,coluna):
    if malha[linha][coluna] == VAZIO:
        malha[linha][coluna] = PAREDE
    elif malha[linha][coluna] == PAREDE:
        malha[linha][coluna] = VAZIO

def cria_inicio(linha,coluna, atual):
    if malha[linha][coluna] == PAREDE:
        return atual
    if atual:
        atual_linha, atual_coluna = atual
        if malha[atual_linha][atual_coluna] == INICIO:
            malha[atual_linha][atual_coluna] = VAZIO
    malha[linha][coluna] = INICIO
    return (linha, coluna)

def cria_destino(linha,coluna, atual):
    if malha[linha][coluna] == PAREDE:
        return atual
    if atual:
        atual_linha, atual_coluna = atual
        if malha[atual_linha][atual_coluna] == DESTINO:
            malha[atual_linha][atual_coluna] = VAZIO
    malha[linha][coluna] = DESTINO
    return (linha, coluna)

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

def reinicia_busca():
    global fronteira, parent, cursor_backtrack, estado_exec
    for linha in range(linhas):
        for coluna in range(colunas):
            if malha[linha][coluna] in (FRONTEIRA, VISITADO, CAMINHO):
                malha[linha][coluna] = VAZIO
    fronteira = deque()
    parent = [[None for _ in range(colunas)] for _ in range(linhas)]
    cursor_backtrack = None
    estado_exec = "idle"

def inicia_bfs():
    global estado_exec
    if inicio is None or destino is None:
        print("Defina INICIO (S) e DESTINO (G) antes de iniciar.")
        return
    reinicia_busca()
    fronteira.append(inicio)
    estado_exec = "rodando"

def passo_bfs():
    global estado_exec, cursor_backtrack
    if estado_exec != "rodando":
        return

    if not fronteira:
        estado_exec = "idle"
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

    for distancia_linha, distancia_coluna in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        nova_linha, nova_coluna = linha + distancia_linha, coluna + distancia_coluna

        if not (0 <= nova_linha < linhas and 0 <= nova_coluna < colunas):
            continue

        if malha[nova_linha][nova_coluna] == PAREDE:
            continue
            
        if malha[nova_linha][nova_coluna] == DESTINO:
            parent[nova_linha][nova_coluna] = (linha, coluna)
            cursor_backtrack = (nova_linha, nova_coluna)
            estado_exec = "reconstruindo"
            return


        if malha[nova_linha][nova_coluna] in (VISITADO, FRONTEIRA, INICIO):
            continue

        parent[nova_linha][nova_coluna] = (linha, coluna)
        fronteira.append((nova_linha, nova_coluna))
        malha[nova_linha][nova_coluna] = FRONTEIRA

def step_backtrack():
    global estado_exec, cursor_backtrack

    if estado_exec != "reconstruindo":
        return

    linha, coluna = cursor_backtrack

    if (linha, coluna) == INICIO:
        estado_exec = "idle"
        return

    proximo = parent[linha][coluna]

    if malha[linha][coluna] not in (INICIO, DESTINO):
        malha[linha][coluna] = CAMINHO

    if proximo is None:
        estado_exec = "idle"
        return

    cursor_backtrack = proximo


rodando = True
while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                if estado_exec == "idle": modo = "parede"
            elif event.key == pygame.K_s:
                if estado_exec == "idle": modo = "inicio"
            elif event.key == pygame.K_g:
                if estado_exec == "idle": modo = "destino"
            elif event.key == pygame.K_b:
                if estado_exec == "idle": inicia_bfs()
            elif event.key == pygame.K_r:
                reinicia_busca()
            elif event.key == pygame.K_SPACE:
                # pausa/retoma apenas quando já iniciado
                if estado_exec == "rodando":
                    estado_exec = "idle"
                elif inicio and destino and (fronteira or cursor_backtrack):
                    estado_exec = "rodando"

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and estado_exec == "idle":
            mx, my = event.pos
            c = mx // celula
            r = my // celula
            if 0 <= r < linhas and 0 <= c < colunas:
                if modo == "parede":
                    if malha[r][c] not in (INICIO, DESTINO):
                        cria_parede(r, c)
                elif modo == "inicio":
                    if malha[r][c] != DESTINO:
                        inicio = cria_inicio(r, c, inicio)
                        modo = "parede"
                elif modo == "destino":
                    if malha[r][c] != INICIO:
                        destino = cria_destino(r, c, destino)
                        modo = "parede"

    # EXECUÇÃO: um passo por frame
    if estado_exec == "rodando":
        try:
            passo_bfs()
        except NotImplementedError:
            # enquanto você não implementar, mantém parado
            estado_exec = "idle"
    elif estado_exec == "reconstruindo":
        try:
            step_backtrack()
        except NotImplementedError:
            estado_exec = "idle"

    tela.fill(WHITE)
    desenhar()
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
