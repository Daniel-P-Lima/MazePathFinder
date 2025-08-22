import pygame
from pygame import mouse

# cores (seja consistente)
WHITE=(255,255,255)
BLACK=(0,0,0)
ORANGE=(255,140,0)
RED=(220,20,60)
YELLOW=(255,215,0)
BLUE=(65,105,225)
GREEN=(60,179,113)

VAZIO = 0
PAREDE = 1
INICIO = 2
DESTINO = 3
FRONTEIRA = 4
VISITADO = 5
CAMINHO = 6

estado_cor = {
    VAZIO: WHITE,
    PAREDE: BLACK,
    INICIO: ORANGE,
    DESTINO: RED,
    FRONTEIRA: YELLOW,
    VISITADO: BLUE,
    CAMINHO: GREEN,
}

linhas = 15
colunas = 15
celula = 40
largura = colunas * celula
altura = linhas * celula
malha = [[VAZIO for _ in range(colunas)] for _ in range(linhas)]



def cria_parede(malha, linha, coluna):
    if malha[linha][coluna] == VAZIO:
        malha[linha][coluna] = PAREDE
    elif malha[linha][coluna] == PAREDE:
        malha[linha][coluna] = VAZIO

def set_inicio(malha, linha, coluna, inicio):
    if malha[linha][coluna] == PAREDE:
        return inicio  # não coloca start em parede
    # limpa o anterior
    if inicio:
        linha_inicial, coluna_inicial = inicio
        if malha[linha_inicial][coluna_inicial] == INICIO:
            malha[linha_inicial][coluna_inicial] = VAZIO
    malha[linha][coluna] = INICIO
    return (linha, coluna)

def cria_destino(malha, linha, coluna, destino):
    if malha[linha][coluna] == PAREDE:
        return destino
    if destino:
        dr, dc = destino
        if malha[dr][dc] == DESTINO:
            malha[dr][dc] = VAZIO
    malha[linha][coluna] = DESTINO
    return (linha, coluna)

def carregar_malha(tela, malha, estado_cor, celula):
    linhas = len(malha)
    colunas = len(malha[0])
    for r in range(linhas):
        for c in range(colunas):
            cor = estado_cor[ malha[r][c] ]
            x = c * celula
            y = r * celula
            pygame.draw.rect(tela, cor, (x, y, celula, celula))
    # (opcional) grid lines finas
    for r in range(linhas + 1):
        y = r * celula
        pygame.draw.line(tela, (40, 40, 40), (0, y), (colunas * celula, y), 1)
    for c in range(colunas + 1):
        x = c * celula
        pygame.draw.line(tela, (40, 40, 40), (x, 0), (x, linhas * celula), 1)

modo = "parede"   # "parede" | "inicio" | "destino"
inicio = None
destino = None

pygame.init()
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Maze")
clock = pygame.time.Clock()

rodando = True

while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                modo = "parede"
            elif event.key == pygame.K_s:
                modo = "inicio"
            elif event.key == pygame.K_g:
                modo = "destino"

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            col = mouse_x // celula
            row = mouse_y // celula
            if 0 <= row < linhas and 0 <= col < colunas:
                if modo == "parede":
                    # não permitir apagar start/dest
                    if malha[row][col] not in (INICIO, DESTINO):
                        cria_parede(malha, row, col)
                elif modo == "inicio":
                    inicio = set_inicio(malha, row, col, inicio)
                    modo = "parede"
                elif modo == "destino":
                    destino = cria_destino(malha, row, col, destino)
                    modo = "parede"

    carregar_malha(tela, malha, estado_cor, celula)
    pygame.display.flip()
    clock.tick(60)
