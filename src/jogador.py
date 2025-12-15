import pygame

from personagem import Personagem
from interface import Interface

class Jogador(Personagem):
    def __init__(self, x, y, limite):
        #construtor da classe mae Personagem, e atributos herdados
        super().__init__(x, y, limite,
                         vida_max=15,
                         ataque=5,
                         velocidade=3,
                         vivo=True,
                         largura_hitbox=40,
                         altura_hitbox=20,
                         nome_pasta_sprites="sprites_jogador")

        self.interface = Interface()

        #hitbox criada para colisao
        self.hitbox_anterior = self.hitbox.copy()
        
        #hitbox gerada pelo ataque
        self.hitbox_soco = pygame.Rect(0, 0, 60, 60)
    
    #ESSENCIAL metodo de interacao com itens
    def interagir_com_item(self, grupo_itens):
        for item in grupo_itens:
            #o modulo colliderect do pygame é o que faz com que a interacao seja detectada
            if self.hitbox.colliderect(item.hitbox):

                if item.tipo == "lixo": 
                    self.bloquear_movimento()

                elif item.tipo == "coracao":
                    self.recuperar_vida(item)

    #bloqueia o movimento por colisao
    def bloquear_movimento(self):
        self.hitbox.topleft = self.hitbox_anterior.topleft
        self.rect.midbottom = self.hitbox.midbottom

    #metodo que recupera a vida ao pegar um corqacao
    def recuperar_vida(self, item):
        print(self.vida)
        cura = self.VIDA_MAX / 3
        self.vida += cura 
        print(self.vida)
            
        item.kill()

    def update(self, keys, grupo_inimigos, grupo_itens):
        self.hitbox_anterior = self.hitbox.copy()
        
        #velociadade em ataque
        if self.esta_atacando:
            self.velocidade = 2
        else:
            self.velocidade = 3
        
        #movimento
        esta_em_movimento = False

        if keys[pygame.K_s]:
            self.hitbox.y += self.velocidade
            esta_em_movimento = True
        elif keys[pygame.K_w]:
            self.hitbox.y -= self.velocidade
            esta_em_movimento = True
        if keys[pygame.K_a]:
            self.hitbox.x -= self.velocidade
            self.esta_virado_esquerda = True
            esta_em_movimento = True
        elif keys[pygame.K_d]:
            self.hitbox.x += self.velocidade
            self.esta_virado_esquerda = False
            esta_em_movimento = True
        
        #ataque
        if keys[pygame.K_SPACE]:
            if not self.esta_atacando:
                self.esta_atacando = True
                self.frame_atual = 0
                self.atacar(self.hitbox_soco, list(grupo_inimigos) + list(grupo_itens))
        
        if self.esta_atacando:
            self.image, self.ultima_atualizacao, self.frame_atual, self.esta_atacando = self.interface.animacao_ataque(self.frames_ataque, self.frames_idle,
                                                                                                                        self.ultima_atualizacao, self.frame_atual,
                                                                                                                        self.esta_virado_esquerda, self.esta_atacando)

        else:
            self.image, self.ultima_atualizacao, self.frame_atual = self.interface.animacao_movimento(self.frames_movimento, self.frames_idle,
                                                                                                      self.ultima_atualizacao, self.frame_atual, esta_em_movimento,
                                                                                                      self.esta_virado_esquerda)

        #movimento da hitbox
        self.aplicar_limites()
        self.rect.midbottom = self.hitbox.midbottom