import pygame

from interface import Interface

#classe mae para implementar o paradigma da herança
class Personagem(pygame.sprite.Sprite):
    def __init__(self, x, y, limite, vida_max, velocidade, vivo, largura_hitbox, altura_hitbox, nome_pasta_sprites):
        #esse construtor é para sobrepor a classe base Sprite do pygame e pode utilizar dela plenamente
        super().__init__()
        
        self.interface = Interface()

        #atributos comuns a todas as classes filhas
        #estado
        self.limite = limite
        self.VIDA_MAX = vida_max
        self._vida = self.VIDA_MAX 
        self._velocidade = velocidade
        self._vivo = vivo
    
        #hitbox
        self.hitbox = pygame.Rect(0, 0, largura_hitbox, altura_hitbox)
        self.hitbox.topleft = (x, y) 

        #imagens de sprite
        self.pasta_sprites = nome_pasta_sprites
        self.ESCALA = 2.5

        imagens_idle, imagens_movimento, imagens_ataque = self.interface.listar_sprites_individuo(nome_pasta_sprites)
        self.frames_idle = self.interface.carregar_lista_imagens(imagens_idle, self.ESCALA)
        self.frames_movimento = self.interface.carregar_lista_imagens(imagens_movimento, self.ESCALA)
        self.frames_ataque = self.interface.carregar_lista_imagens(imagens_ataque, self.ESCALA)

        #movimento do personagem e controle da animação
        self.delay = 150
        self.frame_atual = 0
        self.ultima_atualizacao = pygame.time.get_ticks()

        self.direcao = "baixo"
        self.esta_virado_esquerda = False
        self.esta_atacando = False 

        #desenho da hitbox
        self.imagem = self.frames_movimento[0]
        self.rect = self.imagem.get_rect()
        self.rect.midbottom = self.hitbox.midbottom

    
    #limites da hitbox
    def aplicar_limites(self):
        if self.hitbox.left < self.limite['esquerda']: self.hitbox.left = self.limite['esquerda']
        elif self.hitbox.right > self.limite['direita']: self.hitbox.right = self.limite['direita']
        
        if self.hitbox.top < self.limite['topo']: self.hitbox.top = self.limite['topo']
        elif self.hitbox.bottom > self.limite['baixo']: self.hitbox.bottom = self.limite['baixo']

    #metodo de OVERRIDE obrigatorio
    def update(self):
        raise NotImplementedError("Override necessário, não pode ser usado diretamente pela classe-mãe")

    #properties
    @property
    def vida(self):
        return self._vida
    
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

    @property
    def vida_max(self):
        return self.VIDA_MAX
    
    @property
    def vivo(self):
        return self._vivo
    
    @vivo.setter
    def vivo(self, novo_estado):
        self._vivo = novo_estado