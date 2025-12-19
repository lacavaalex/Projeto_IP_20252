import pygame

from personagem import Personagem
from interface import Interface

class Jogador(Personagem):
    def __init__(self, x, y, limite):
        #construtor da classe mae Personagem, e atributos herdados
        super().__init__(x, y, limite,
                         vida_max=16,
                         ataque=5,
                         velocidade=5,
                         vivo=True,
                         largura_hitbox=40,
                         altura_hitbox=80,
                         nome_pasta_sprites="sprites_jogador")

        self.interface = Interface()

        #barulho de soco
        self.musica_soco = pygame.mixer.Sound('res/sound/[Efeito Sonoro] Soco _ Punch [TEzFJEOdsR8].mp3')
        
        #hitbox criada para colisao
        self.hitbox_anterior = self.hitbox.copy()
        
        #hitbox gerada pelo ataque
        self.hitbox_soco = pygame.Rect(0, 0, 60, 60)

        #atributos para serem atualizados
        self.velocidade_inicial = self.velocidade
        self.ataque_inicial = self.ataque
        self._quantidade_coracoes = 3
    
    #resetar atributos apos morte
    def resetar_atributos(self, jogo):
        self.vivo = True
        self.ataque = self.ataque_inicial
        self.velocidade = self.velocidade_inicial
        self.VIDA_MAX = 16
        self.quantidade_coracoes = 3
        self.vida = self.VIDA_MAX

    #ESSENCIAL metodo de interacao com itens
    def interagir_com_item(self, grupo_itens, itens_coletados):
        for item in grupo_itens:
            #o modulo colliderect do pygame é o que faz com que a interacao seja detectada
            if self.hitbox.colliderect(item.hitbox):

                if item.tipo == "lixo": 
                    self.bloquear_movimento()

                else:
                    self.coletar_item(item, itens_coletados)              

    #bloqueia o movimento por colisao
    def bloquear_movimento(self):
        self.hitbox.topleft = self.hitbox_anterior.topleft
        self.rect.midbottom = self.hitbox.midbottom

    #metodo que recupera a vida ao pegar um corqacao e coleta os itens de passagem de fase
    def coletar_item(self, item, itens_coletados):
        if item.tipo == "coracao":
            cura = self.VIDA_MAX / 3
            self.vida += cura
        
        else:
            itens_coletados.append(item.image)
            
        item.kill()

    def update(self, keys, grupo_inimigos, grupo_itens, itens_coletados):
        self.hitbox_anterior = self.hitbox.copy()

        #hamburger na lista
        if len(itens_coletados) > 0:
            self._quantidade_coracoes = 4

        #cracha na lista
        if len(itens_coletados) > 1:
            self.velocidade_base = self.velocidade_inicial * 1.5
        else:
            self.velocidade_base = self.velocidade_inicial

        #notebook na lista
        if len(itens_coletados) > 2:
            self.ataque = self.ataque_inicial * 2

        #velociadade em ataque
        if self.esta_atacando:
            self.velocidade = self.velocidade_base - 1
        else:
            self.velocidade = self.velocidade_base
        
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
            self.musica_soco.set_volume(0.1)
            self.musica_soco.play()

        else:
            self.image, self.ultima_atualizacao, self.frame_atual = self.interface.animacao_movimento(self.frames_movimento, self.frames_idle,
                                                                                                      self.ultima_atualizacao, self.frame_atual, esta_em_movimento,
                                                                                                      self.esta_virado_esquerda)

        #movimento da hitbox
        self.aplicar_limites()
        self.rect.center = self.hitbox.center

    @property
    def quantidade_coracoes(self):
        return self._quantidade_coracoes

    @quantidade_coracoes.setter
    def quantidade_coracoes(self, nova_qnt):
        if nova_qnt != self._quantidade_coracoes:
            vida_percentual = self.vida / self.VIDA_MAX
            self._quantidade_coracoes = nova_qnt
            self.VIDA_MAX = nova_qnt * 5
            self.vida = vida_percentual * self.VIDA_MAX
