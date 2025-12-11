import pygame
import os

from configuracoes import Configuracoes

config = Configuracoes()

class Interface:

    #metodo que define as dimensoes e entao cria a tela pelo pygame
    def dimensionar_tela(self):
        largura = config.largura
        altura = config.altura

        tela = pygame.display.set_mode([largura, altura])
        pygame.display.set_caption('Projeto de Ip')

        return tela
    
    #metodos de definicao dos sprites
    def carregar_lista_imagens(self, lista_caminhos, escala):
        frames = []
        for caminho in lista_caminhos:
            try:
                img = pygame.image.load(caminho).convert_alpha()
                tamanho_novo = (int(img.get_width() * escala), int(img.get_height() * escala))
                img = pygame.transform.scale(img, tamanho_novo)
                frames.append(img)
            except Exception as e:
                print(f"ERRO: Imagem não encontrada: {caminho}")
        return frames
    
    #retorna quais sao os sprites
    def listar_sprites_individuo(self, pasta):
        pasta_imagens = os.path.join(os.getcwd(), "res", pasta)
        lista_sprites_idle = [os.path.join(pasta_imagens, f'sprite_0{i}.png') for i in range(0, 2)]
        lista_sprites_movimento = [os.path.join(pasta_imagens, f'sprite_0{i}.png') for i in range(2, 7)]
        lista_sprites_ataque = [os.path.join(pasta_imagens, f'sprite_0{i}.png') for i in range(7, 11)]

        return lista_sprites_idle, lista_sprites_movimento, lista_sprites_ataque
    
    #metodos de animacao de ataque e movimento
    def animacao_movimento(self, frames_movimento, frames_idle, ultima_atualizacao, frame_atual, esta_em_movimento, esta_virado_esquerda):
        now = pygame.time.get_ticks()
        #delay de movimento
        delay = 150

        if esta_em_movimento:
            lista_atual = frames_movimento 
        else:
            lista_atual = frames_idle

        if now - ultima_atualizacao >= delay:
            ultima_atualizacao = now
            frame_atual = (frame_atual + 1) % len(lista_atual)
        
        if frame_atual >= len(lista_atual):
            frame = lista_atual[-1]
        else:
            frame = lista_atual[frame_atual]
        
        if esta_virado_esquerda: frame = pygame.transform.flip(frame, True, False)
        
        imagem = frame

        return imagem, ultima_atualizacao, frame_atual

    def animacao_ataque(self, frames_ataque, frames_idle, ultima_atualizacao, frame_atual, esta_virado_esquerda, esta_atacando):
        now = pygame.time.get_ticks()
        #delay de animacao do soco
        delay = 90

        #esse calculo verifica se o fram precisa ser atualizado usando a passagem de ticks
        if now - ultima_atualizacao >= delay:
            ultima_atualizacao = now
            frame_atual += 1

            #fim da animacao
            if frame_atual >= len(frames_ataque):
                esta_atacando = False 
                frame_atual = 0 
                imagem = frames_idle
                return 

        #controle da frame e direcao da frame atuais
        if frames_ataque:
            frame = frames_ataque[frame_atual]
            if esta_virado_esquerda:
                frame = pygame.transform.flip(frame, True, False)
            imagem = frame

        #cria a area de ataque do soco
        soco_largura = 30
        soco_altura = 50
        self.hitbox_soco = pygame.Rect(0, 0, soco_largura, soco_altura)

        #alinha e direciona o ataque
        self.hitbox_soco.centery = self.rect.centery

        if self.esta_virado_esquerda:
            self.hitbox_soco.right = self.rect.left + 15
        else:
            self.hitbox_soco.left = self.rect.right - 15

        return imagem