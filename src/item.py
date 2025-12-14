import pygame

from interface import Interface

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, tipo):
        super().__init__()

        self.interface = Interface()

        self.tipo = tipo
        self.nome_pasta = "sprites_itens"
        
        imagens_item = self.interface.listar_sprites_item(tipo)
        self.frames_item = self.interface.carregar_lista_imagens(imagens_item, 3)
        print(imagens_item)

        #tratamento de erro
        if self.frames_item:
            self.image = self.frames_item[0]
        else:
            self.image = pygame.Surface([30, 30])
            self.image.fill((150, 150, 150))

        LARGURA_HITBOX_ITEM = 60 
        ALTURA_HITBOX_ITEM = 70
        
        self.hitbox = pygame.Rect(0, 0, LARGURA_HITBOX_ITEM, ALTURA_HITBOX_ITEM)
        self.hitbox.topleft = (x, y) 

        self.rect = self.image.get_rect()
        self.rect.midbottom = self.hitbox.midbottom