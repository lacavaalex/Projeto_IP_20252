import pygame

from configuracoes import Configuracoes
from jogador import Jogador
from inimigo import Inimigo

config = Configuracoes()

class Jogo:

    def __init__(self, tela):
        self.tela = tela

        #variavel de controle
        self.rodando = True
        
        #relogio interno do pygame
        self.clock = pygame.time.Clock()

        #define os limites de movimento do jogador
        limites_tela = {
            'esquerda': 0, 
            'direita': config.largura, 
            'topo': 0, 
            'baixo': config.altura
        }
        
        #posicao inicial (central)
        x_inicial = config.largura // 2
        y_inicial = config.altura // 2
        
        self.jogador = Jogador(x_inicial, y_inicial, limites_tela)
        self.inimigo = Inimigo(x_inicial + config.largura // 2, y_inicial, limites_tela)

    #gameloop
    def run(self):
        while self.rodando:
            self.clock.tick(config.fps)
            self.handle_events()
            self.update()
            self.draw()

    #recebe inputs de teclado pelo modulo event
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.rodando = False

    #atualiza os ultimos inputs dentro do gameloop
    def update(self):
        keys = pygame.key.get_pressed()
        self.jogador.update(keys)
        self.inimigo.update(self.jogador)

    #metodo contendo as funcionalidades graficas do pygame
    def draw(self):
        self.tela.fill((0, 0, 0)) 
        self.tela.blit(self.jogador.imagem, self.jogador.rect)
        self.tela.blit(self.inimigo.imagem, self.inimigo.rect)
        pygame.display.flip()