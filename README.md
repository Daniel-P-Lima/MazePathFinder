---

# Maze Pathfinding Visualizer

Este projeto é um **visualizador interativo de algoritmos de busca em labirintos** desenvolvido em **Python com Pygame**.
Ele permite que você construa um labirinto, defina pontos de início e destino e veja passo a passo como o algoritmo encontra o caminho.

## 🎯 Funcionalidades

* Construção manual do labirinto (paredes, início e destino).
* Visualização em tempo real do algoritmo de **Busca em Largura (BFS)**.
* Representação visual clara com cores distintas para cada estado:

  * **Branco** → Espaço vazio
  * **Preto** → Parede
  * **Laranja** → Ponto de início
  * **Vermelho** → Ponto de destino
  * **Amarelo** → Fronteira (nós na fila de expansão)
  * **Azul** → Nós visitados
  * **Verde** → Caminho encontrado

## 🛠️ Tecnologias

* [Python 3](https://www.python.org/)
* [Pygame](https://www.pygame.org/)

## 🚀 Como executar

1. Clone este repositório:

   ```bash
   git clone https://github.com/seu-usuario/maze-visualizer.git
   cd maze-visualizer
   ```

2. Instale as dependências:

   ```bash
   pip install pygame
   ```

3. Execute o programa:

   ```bash
   python gui.py
   ```

## 🎮 Como usar

* **Botões do mouse**:

  * Clique para adicionar/remover **paredes**.
  * Mude o modo para definir **início (TECLA S)** e **destino (TECLA G)**.
  * Iniciar (TECLA B): inicia a execução do algoritmo.
  * Reiniciar (TECLA R) 
  * O caminho será destacado em **verde** quando encontrado.

## 📌 Estrutura do projeto

* `gui.py` → Código principal do visualizador.

## 🔮 Possíveis melhorias

* Adicionar suporte a **DFS, A\*** e outros algoritmos.
* Permitir ajuste dinâmico do tamanho do grid.
* Interface gráfica com botões de seleção de modo (parede/início/destino).

---
