import pygame

from interface import Interface

class Jogador(pygame.sprite.Sprite):
    def __init__(self, x, y, limite):
        #esse construtor é para sobrepor a classe base Sprite do pygame e pode utilizar dela plenamente
        super().__init__()

        self.interface = Interface()
        
        #atributos de estado
        self.limite = limite
        self.VIDA_MAX = 15
        self.vida = self.VIDA_MAX
        self._velocidade = 3

        imagens_idle, imagens_movimento, imagens_ataque = self.interface.listar_sprites_individuo('sprites_jogador')

        #atributos de movimento
        self.delay = 150
        self.x = x
        self.y = y
        self.ESCALA = 2.5 
        self.frames_idle = self.interface.carregar_lista_imagens(imagens_idle, self.ESCALA)
        self.frames_movimento = self.interface.carregar_lista_imagens(imagens_movimento, self.ESCALA)
        self.frames_ataque = self.interface.carregar_lista_imagens(imagens_ataque, self.ESCALA)

        #controle da animacao dos sprites
        self.frame_atual = 0
        self.ultima_atualizacao = pygame.time.get_ticks()
        self.direcao = "baixo"
        self.esta_virado_esquerda = False
        self.esta_atacando = False 

        #desenho da hitbox
        self.image = self.frames_movimento[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        #hitbox de movimento
        self.hitbox = pygame.Rect(0, 0, 40, 20)
        self.hitbox.midbottom = self.rect.midbottom

        #hitbox gerada pelo ataque
        self.hitbox_soco = pygame.Rect(0, 0, 40, 20)

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
            self.esta_virado_esquerda = True
            esta_em_movimento = True
        elif keys[pygame.K_d]:
            self.hitbox.x += self.velocidade
            self.esta_virado_esquerda = False
            esta_em_movimento = True
        
        self.image, self.ultima_atualizacao, self.frame_atual = self.interface.animacao_movimento(self.frames_movimento, self.frames_idle,
                                                                                                  self.ultima_atualizacao, self.frame_atual, esta_em_movimento,
                                                                                                  self.esta_virado_esquerda)

        #movimento da hitbox
        self.aplicar_limites()
        self.rect.midbottom = self.hitbox.midbottom


    #properties
    @property
    def vida_max(self):
        return self.VIDA_MAX
    
    @property
    def vida(self):
        return self.vida
    
    @vida.setter
    def vida(self, novo_valor):
        if novo_valor > self.VIDA_MAX:
            self._vida = self.VIDA_MAX
        elif novo_valor < 0:
            self._vida = 0
        else:
            self._vida = novo_valor
    
    @property
    def velocidade(self):
        return self._velocidade
    
    @velocidade.setter
    def velocidade(self, novo_valor):
        self._velocidade = novo_valor