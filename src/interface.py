import pygame
import os

from configuracoes import Configuracoes

config = Configuracoes()

class Interface:
    def __init__(self):
        #fonte
        pygame.font.init()
        self.fonte = pygame.font.SysFont('Arial', 30, bold=True)
        self.fonte_go = pygame.font.SysFont('Arial', 60, bold=True) 

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
                print(f"ERRO: image não encontrada: {caminho}")
        return frames
    
    #retorna quais sao os sprites
    def listar_sprites_individuo(self, pasta):
        pasta_imagens = os.path.join(os.getcwd(), "res", pasta)
        lista_sprites_idle = [os.path.join(pasta_imagens, f'sprite_0{i}.png') for i in range(0, 2)]
        lista_sprites_movimento = [os.path.join(pasta_imagens, f'sprite_0{i}.png') for i in range(2, 7)]
        lista_sprites_ataque = [os.path.join(pasta_imagens, f'sprite_0{i}.png') for i in range(7, 11)]

        return lista_sprites_idle, lista_sprites_movimento, lista_sprites_ataque
    
    def listar_sprites_item(self, tipo):
        pasta_imagens = os.path.join(os.getcwd(), "res", "sprites_itens", f'{tipo}')
        lista_sprites_item = [os.path.join(pasta_imagens, f"{tipo}_00.png")]

        return lista_sprites_item
    
    def desenhar_vida(self, tela, vida, vida_max, quantidade_coracoes):
        pasta_imagens = os.path.join(os.getcwd(), "res", "sprites_vida")
        caminhos_vida = [os.path.join(pasta_imagens, f'sprite_0{i}.png') for i in range(0, 3)]
        self.frames_vida = self.carregar_lista_imagens(caminhos_vida, 3)

        lista_desenho = []
        
        vida_por_coracao = vida_max / quantidade_coracoes
        
        for i in range(quantidade_coracoes):
            vida_inicio = i * vida_por_coracao
            vida_fim = (i + 1) * vida_por_coracao
            
            vida_no_segmento = min(max(vida - vida_inicio, 0), vida_por_coracao)
            
            percentual_preenchido = vida_no_segmento / vida_por_coracao
            
            if percentual_preenchido > 2/3: 
                lista_desenho.append(self.frames_vida[0])
            elif percentual_preenchido > 1/3:
                lista_desenho.append(self.frames_vida[1])
            else:
                lista_desenho.append(self.frames_vida[2])

        x = 50
        for frame in lista_desenho:
            tela.blit(frame, (x, 50))
            x += frame.get_width()

    def mostrar_itens_coletados(self, tela, itens_coletados):
        caminho = [os.path.join("res", "sprites_itens", "moldura", "moldura_00.png")]
        self.moldura_itens = self.carregar_lista_imagens(caminho, 4)[0]
            
        x = 50
        largura_moldura = self.moldura_itens.get_width()
        
        for i in range(3):
            tela.blit(self.moldura_itens, (x, config.altura - 150))
            
            if i < len(itens_coletados):
                frame = itens_coletados[i]
                item_x = x + (largura_moldura - frame.get_width()) // 2
                item_y = config.altura - 150 + (self.moldura_itens.get_height() - frame.get_height()) // 2
                tela.blit(frame, (item_x, item_y))
            
            x += largura_moldura + 10

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
        
        image = frame

        return image, ultima_atualizacao, frame_atual

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

                frame = frames_idle[0]
                if esta_virado_esquerda: 
                    frame = pygame.transform.flip(frame, True, False)
                image = frame

                return image, ultima_atualizacao, frame_atual, esta_atacando

        #controle da frame e direcao da frame atuais
        if frames_ataque:
            if frame_atual >= len(frames_ataque):
                frame = frames_ataque[0]
            else:
                frame = frames_ataque[frame_atual]
            if esta_virado_esquerda:
                frame = pygame.transform.flip(frame, True, False)
            image = frame

        return image, ultima_atualizacao, frame_atual, esta_atacando
    
    def desenhar_go(self, tela, liberado_para_avancar):
        if liberado_para_avancar:
            if (pygame.time.get_ticks() // 500) % 2 == 0: 
                texto_go = self.fonte_go.render("GO ->", True, (0, 255, 0)) 
                tela.blit(texto_go, (config.largura - 250, config.altura // 2))