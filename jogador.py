import pygame

class Jogador():
    def __init__(self, x, y, limite):
        self.x = x
        self.y = y
        self.limite = limite
        self.velocidade = 3

        #desenho do retangulo temporario
        self.largura = 50
        self.altura = 50
        self.cor = (255, 0, 0)
        self.image = pygame.Surface((self.largura, self.altura))
        self.image.fill(self.cor)

        #desenho da hitbox
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        #hitbox de movimento
        self.hitbox = pygame.Rect(0, 0, 40, 20)
        self.hitbox.midbottom = self.rect.midbottom

    #limites da hitbox
    def aplicar_limites(self):
        if self.hitbox.left < self.limite['esquerda']: self.hitbox.left = self.limite['esquerda']
        elif self.hitbox.right > self.limite['direita']: self.hitbox.right = self.limite['direita']
        
        if self.hitbox.bottom < self.limite['topo']: self.hitbox.bottom = self.limite['topo']
        elif self.hitbox.bottom > self.limite['baixo']: self.hitbox.bottom = self.limite['baixo']

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
            self.facing_left = True
            esta_em_movimento = True
        elif keys[pygame.K_d]:
            self.hitbox.x += self.velocidade
            self.facing_left = False
            esta_em_movimento = True
        
        #movimento da hitbox
        self.aplicar_limites()
        self.rect.midbottom = self.hitbox.midbottom