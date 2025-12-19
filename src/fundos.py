import pygame
from configuracoes import Configuracoes

config = Configuracoes()


class Cenario():
    def __init__(self, arquivo):
        self.arquivo = pygame.image.load(arquivo)
        self.imagem = pygame.transform.scale(
            self.arquivo, (config.largura, config.altura)).convert()
