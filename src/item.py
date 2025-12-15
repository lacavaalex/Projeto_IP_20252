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
        
        #definir item
        self._eh_coletavel = self.definir_coletavel()
        if not self._eh_coletavel:
            self.durabilidade = 20

        #tratamento de erro
        if self.frames_item:
            self.image = self.frames_item[0]
        else:
            self.image = pygame.Surface([30, 30])
            self.image.fill((150, 150, 150))

        if self.eh_coletavel:
            LARGURA_HITBOX_ITEM = 110
            ALTURA_HITBOX_ITEM = 90
        else:
            LARGURA_HITBOX_ITEM = 60 
            ALTURA_HITBOX_ITEM = 70
        
        self.hitbox = pygame.Rect(0, 0, LARGURA_HITBOX_ITEM, ALTURA_HITBOX_ITEM)
        self.hitbox.topleft = (x, y) 

        self.rect = self.image.get_rect()
        self.rect.midbottom = self.hitbox.midbottom

    #definir se o item é quebravel ou coletavel
    def definir_coletavel(self):
        if self.tipo == "lixo":
            eh_coletavel = False
        else:
            eh_coletavel = True
        return eh_coletavel

    #se o objeto for quebravel ele leva dano igual os inimigos
    def quebrar_objeto(self, dano):
        self.durabilidade -= dano

        if self.durabilidade <= 0:
            if self.tipo == "lixo":
                novo_item = Item(self.hitbox.centerx - 20, self.hitbox.centery - 20, "coracao")
                
                for grupo in self.groups():
                    grupo.add(novo_item)
            
            self.kill()
            

    @property
    def eh_coletavel(self):
        return self._eh_coletavel
    
    @eh_coletavel.setter
    def eh_coletavel(self, valor):
        self._eh_coletavel = valor