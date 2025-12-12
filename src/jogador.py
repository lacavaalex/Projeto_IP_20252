import pygame

from personagem import Personagem
from interface import Interface

class Jogador(Personagem):
    def __init__(self, x, y, limite):
        #construtor da classe mae Personagem, e atributos herdados
        super().__init__(x, y, limite,
                         vida_max=15,
                         velocidade=3,
                         vivo=True,
                         largura_hitbox=40,
                         altura_hitbox=20,
                         nome_pasta_sprites="sprites_jogador")

        self.interface = Interface()
        
        #hitbox gerada pelo ataque
        self.hitbox_soco = pygame.Rect(0, 0, 40, 20)
    
    def update(self, keys):
        #movimento
        esta_em_movimento = False

        if keys[pygame.K_s]:
            self.hitbox.y += self.velocidade
            esta_em_movimento = True
        elif keys[pygame.K_w]:
            self.hitbox.y -= self.velocidade
            esta_em_movimento = True
        elif keys[pygame.K_a]:
            self.hitbox.x -= self.velocidade
            self.esta_virado_esquerda = True
            esta_em_movimento = True
        elif keys[pygame.K_d]:
            self.hitbox.x += self.velocidade
            self.esta_virado_esquerda = False
            esta_em_movimento = True
        
        self.imagem, self.ultima_atualizacao, self.frame_atual = self.interface.animacao_movimento(self.frames_movimento, self.frames_idle,
                                                                                                  self.ultima_atualizacao, self.frame_atual, esta_em_movimento,
                                                                                                  self.esta_virado_esquerda)

        #movimento da hitbox
        self.aplicar_limites()
        self.rect.midbottom = self.hitbox.midbottom