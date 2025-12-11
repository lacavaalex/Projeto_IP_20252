import pygame

from configuracoes import Configuracoes

config = Configuracoes()

class Jogo:

    def __init__(self, tela):
        self.tela = tela
        self.rodando = True
        self.clock = pygame.time.Clock()

    def run(self):
        while self.rodando:
            self.clock.tick(config.fps)
            self.handle_events()
            self.update()
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.rodando = False

    def update(self):
        keys = pygame.key.get_pressed()

    def draw(self):
        self.tela.fill((0, 0, 0)) 
        
        pygame.display.flip()