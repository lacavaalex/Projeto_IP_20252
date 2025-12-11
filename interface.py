import pygame
from configuracoes import Configuracoes

config = Configuracoes()

class Interface:

    #metodo que define as dimensoes e entao cria a tela pelo pygame
    def dimensionar_tela(self):
        largura = config.largura
        altura = config.altura

        tela = pygame.display.set_mode([largura, altura])
        pygame.display.set_caption('Projeto de Ip')

        return tela