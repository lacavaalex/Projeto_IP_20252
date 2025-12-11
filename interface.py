import pygame
from configuracoes import Configuracoes

config = Configuracoes()

class Interface:

    def dimensionar_tela(self):
        largura = config.largura
        altura = config.altura

        tela = pygame.display.set_mode([largura, altura])
        pygame.display.set_caption('Projeto de Ip')

        return tela