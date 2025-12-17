import pygame

from personagem import Personagem
from interface import Interface

class Inimigo(Personagem):
    def __init__(self, x, y, limite):
        #construtor da classe mae Personagem, e atributos herdados
        super().__init__(x, y, limite,
                         vida_max=7,
                         ataque=1,
                         velocidade=2,
                         vivo=True,
                         largura_hitbox=40,
                         altura_hitbox=80,
                         nome_pasta_sprites="sprites_inimigo")

        self.interface = Interface()
        
        #controle de estado
        self.estado_atual = "idle"

        #raio de visao e posicao
        self.x = x
        self.y = y
        self.RAIO_VISAO = 400
        self.RAIO_ATAQUE = 90

        #hitbox gerada pelo ataque
        self.hitbox_soco = pygame.Rect(0, 0, 60, 60)
    
    def mudar_estado(self, novo_estado):
        estados_possiveis = ["idle", "movimento", "ataque", "apanhando"]
        if novo_estado != self.estado_atual and novo_estado in estados_possiveis:
            self.estado_atual = novo_estado
            self.indice_atual = 0

    def comportamento(self, jogador):
        esta_em_movimento = False
        
        #sem comportamento em morte
        if not self.vivo:
            return
        
        if self.estado_atual == "ataque":
            return esta_em_movimento

        if self.estado_atual == "apanhando":
            return

        #logica de perseguicao
        dx = jogador.hitbox.centerx - self.hitbox.centerx
        dy = jogador.hitbox.centery - self.hitbox.centery
        distancia = (dx**2 + dy**2)**(1/2)

        if dx > 0:
            self.esta_virado_esquerda = False 
        elif dx < 0:
            self.esta_virado_esquerda = True 

        if distancia < self.RAIO_ATAQUE:
           self.mudar_estado("ataque")
           self.atacar(self.hitbox_soco, [jogador])

        elif distancia < self.RAIO_VISAO:
            self.mudar_estado("movimento")
            esta_em_movimento = True

            if distancia > 0:
                dx = dx / distancia
                dy = dy / distancia

            self.x += dx * self.velocidade
            self.y += dy * self.velocidade

            self.hitbox.x = int(self.x)
            self.hitbox.y = int(self.y)

        else:
            self.mudar_estado("idle")

        return esta_em_movimento

    def update(self, jogador):
        #movimento
        esta_em_movimento = self.comportamento(jogador)

        if self.estado_atual == "ataque":
            self.esta_atacando = True
        
        if self.esta_atacando:
            self.image, self.ultima_atualizacao, self.frame_atual, self.esta_atacando = self.interface.animacao_ataque(self.frames_ataque, self.frames_idle,
                                                                                                                        self.ultima_atualizacao, self.frame_atual,
                                                                                                                        self.esta_virado_esquerda, self.esta_atacando)

            if not self.esta_atacando:
                self.mudar_estado("idle")

        else:
            self.image, self.ultima_atualizacao, self.frame_atual = self.interface.animacao_movimento(self.frames_movimento, self.frames_idle,
                                                                                                      self.ultima_atualizacao, self.frame_atual, esta_em_movimento,
                                                                                                      self.esta_virado_esquerda)

        #movimento da hitbox
        self.aplicar_limites()
        self.rect.center = self.hitbox.center