import pygame
from personagem import Personagem

class Chefe(Personagem):
    def __init__(self, x, y, limite):
        super().__init__(x, y, limite,
                         vida_max=50,
                         ataque=3,
                         velocidade=2,
                         vivo=True,
                         largura_hitbox=50,
                         altura_hitbox=90,
                         nome_pasta_sprites="sprites_boss")
        
        #atributos
        self.vida = self.vida_max
        self.RAIO_VISAO = 800
        self.ESCALA = 3
        
        imagens_idle, imagens_movimento, imagens_ataque = self.interface.listar_sprites_individuo(self.pasta_sprites)
        self.frames_idle = self.interface.carregar_lista_imagens(imagens_idle, self.ESCALA)
        self.frames_movimento = self.interface.carregar_lista_imagens(imagens_movimento, self.ESCALA)
        self.frames_ataque = self.interface.carregar_lista_imagens(imagens_ataque, self.ESCALA)
        
        self.hitbox = pygame.Rect(0, 0, 80, 60)
        self.hitbox.topleft = (x, y)
        self.hitbox_soco = pygame.Rect(0, 0, 80, 80)

    #atualizacao similar a do inimigo comum
    def update(self, jogador):
        dx = jogador.hitbox.centerx - self.hitbox.centerx
        dy = jogador.hitbox.centery - self.hitbox.centery
        distancia = (dx**2 + dy**2)**0.5

        self.esta_virado_esquerda = dx < 0

        if distancia < 100:
            if not self.esta_atacando:
                self.esta_atacando = True
                self.frame_atual = 0
                self.atacar(self.hitbox_soco, [jogador])

        elif distancia < self.RAIO_VISAO:
            if distancia > 0:
                self.hitbox.x += (dx / distancia) * self.velocidade
                self.hitbox.y += (dy / distancia) * self.velocidade

        if self.esta_atacando:
            self.image, self.ultima_atualizacao, self.frame_atual, self.esta_atacando = self.interface.animacao_ataque(
                self.frames_ataque, self.frames_idle, self.ultima_atualizacao, self.frame_atual, 
                self.esta_virado_esquerda, self.esta_atacando, delay=200)
        
        else:
            esta_em_movimento = distancia < self.RAIO_VISAO and distancia > 100
            self.image, self.ultima_atualizacao, self.frame_atual = self.interface.animacao_movimento(
                self.frames_movimento, self.frames_idle, self.ultima_atualizacao, self.frame_atual, 
                esta_em_movimento, self.esta_virado_esquerda)

        self.aplicar_limites()
        self.rect.center = self.hitbox.center