import pygame

from configuracoes import Configuracoes
from jogador import Jogador
from inimigo import Inimigo
from interface import Interface

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
        x_inicial = config.largura // 6
        y_inicial = config.altura // 2
        
        self.interface = Interface()

        self.jogador = Jogador(x_inicial, y_inicial, limites_tela)
        
        #os inimigos existem dentro de um group no pygame
        self.grupo_inimigos = pygame.sprite.Group() 
        self.gerar_inimigos(3, limites_tela)

    #geracao dos multiplos inimigos
    def gerar_inimigos(self, num_inimigos, limites):
        for n in range(num_inimigos):
            novo_y = 100 + (200 * n)
            self.grupo_inimigos.add(Inimigo(config.largura * 4 // 5, novo_y, limites))

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

        #controle de vida e morte do jogador e dos inimigos
        if self.jogador.vivo:
            self.jogador.update(keys, self.grupo_inimigos)
        if not self.jogador.vivo:
            self.rodando = False
        for inimigo in self.grupo_inimigos:
            if inimigo.vivo:
                inimigo.update(self.jogador)
            else:
                inimigo.kill()

    #metodo contendo as funcionalidades graficas do pygame
    def draw(self):
        self.tela.fill((0, 0, 0)) 
        self.tela.blit(self.jogador.imagem, self.jogador.rect)
        self.grupo_inimigos.draw(self.tela)
        pygame.display.flip()