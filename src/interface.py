import pygame
import os

from configuracoes import Configuracoes

config = Configuracoes()


class Interface:
    def __init__(self):
        # fonte
        pygame.font.init()

        caminho_fonte_personalizada = os.path.join(
            os.getcwd(), "res", "fonts", "fonte.ttf")

        try:
            self.fonte = pygame.font.Font(caminho_fonte_personalizada, 30)
            self.fonte_grande = pygame.font.Font(
                caminho_fonte_personalizada, 60)
        except FileNotFoundError:
            self.fonte = pygame.font.SysFont('Arial', 30, bold=True)
            self.fonte_grande = pygame.font.SysFont('Arial', 60, bold=True)

        # chao
        caminho_chao = os.path.join(
            os.getcwd(), "res", "sprites_textura", "rua_universitaria.png")

        try:
            self.textura_chao = pygame.image.load(caminho_chao).convert()
        except pygame.error:
            pass

        caminho_laje = os.path.join(
            os.getcwd(), "res", "sprites_textura", "chao_cin.png")
        try:
            self.textura_laje = pygame.image.load(caminho_laje).convert()
        except pygame.error:
            pass

    # metodo que define as dimensoes e entao cria a tela pelo pygame
    def dimensionar_tela(self):
        largura = config.largura
        altura = config.altura

        tela = pygame.display.set_mode([largura, altura])
        pygame.display.set_caption('Projeto de Ip')

        return tela

    # metodos de definicao dos sprites
    def carregar_lista_imagens(self, lista_caminhos, escala):
        frames = []
        for caminho in lista_caminhos:
            try:
                img = pygame.image.load(caminho).convert_alpha()
                tamanho_novo = (int(img.get_width() * escala),
                                int(img.get_height() * escala))
                img = pygame.transform.scale(img, tamanho_novo)
                frames.append(img)
            except Exception as e:
                print(f"ERRO: image não encontrada: {caminho}")
        return frames

    # retorna quais sao os sprites
    def listar_sprites_individuo(self, pasta):
        pasta_imagens = os.path.join(os.getcwd(), "res", pasta)
        lista_sprites_idle = [os.path.join(
            pasta_imagens, f'sprite_0{i}.png') for i in range(0, 2)]
        lista_sprites_movimento = [os.path.join(
            pasta_imagens, f'sprite_0{i}.png') for i in range(2, 7)]
        lista_sprites_ataque = [os.path.join(
            pasta_imagens, f'sprite_0{i}.png') for i in range(7, 11)]

        return lista_sprites_idle, lista_sprites_movimento, lista_sprites_ataque

    def listar_sprites_item(self, tipo):
        pasta_imagens = os.path.join(
            os.getcwd(), "res", "sprites_itens", f'{tipo}')
        lista_sprites_item = [os.path.join(pasta_imagens, f"{tipo}_00.png")]

        return lista_sprites_item

    # metodo que faz o visual do chao
    def desenhar_chao(self, tela, limites_tela, fase_atual):
        pass
        # y = limites_tela['topo']

        # if fase_atual >= 7:
        # textura = self.textura_laje
        # else:
        # textura = self.textura_chao

        # largura_textura = textura.get_width()
        # altura_textura = textura.get_height()

        # desenha em "matriz" o chao
        # for y_pos in range(int(y), config.altura, altura_textura):
        # for x_pos in range(0, config.largura, largura_textura):
        # tela.blit(textura, (x_pos, y_pos))

    def desenhar_vida(self, tela, vida, vida_max, quantidade_coracoes, x, y):
        pasta_imagens = os.path.join(os.getcwd(), "res", "sprites_vida")
        caminhos_vida = [os.path.join(
            pasta_imagens, f'sprite_0{i}.png') for i in range(0, 3)]
        self.frames_vida = self.carregar_lista_imagens(caminhos_vida, 3)

        lista_desenho = []

        vida_por_coracao = vida_max / quantidade_coracoes

        for i in range(quantidade_coracoes):
            vida_inicio = i * vida_por_coracao

            vida_no_segmento = min(
                max(vida - vida_inicio, 0), vida_por_coracao)

            percentual_preenchido = vida_no_segmento / vida_por_coracao

            if percentual_preenchido > 1/2:
                lista_desenho.append(self.frames_vida[0])
            elif percentual_preenchido > 0:
                lista_desenho.append(self.frames_vida[1])
            else:
                lista_desenho.append(self.frames_vida[2])

        for frame in lista_desenho:
            tela.blit(frame, (x, y))
            x += frame.get_width()

    def mostrar_itens_coletados(self, tela, itens_coletados):
        caminho = [os.path.join("res", "sprites_itens",
                                "moldura", "moldura_00.png")]
        self.moldura_itens = self.carregar_lista_imagens(caminho, 4)[0]

        x = config.largura / 3
        largura_moldura = self.moldura_itens.get_width()

        for i in range(3):
            tela.blit(self.moldura_itens, (x, 20))

            if i < len(itens_coletados):
                frame = itens_coletados[i]
                item_x = x + (largura_moldura - frame.get_width()) // 2
                item_y = 20 + (self.moldura_itens.get_height() -
                               frame.get_height()) // 2
                tela.blit(frame, (item_x, item_y))

            x += largura_moldura + 10

    # metodo que mostra as telas de mensagem
    def mostrar_tela(self, tela, titulo, textos, cor_fundo):
        tela.fill(cor_fundo)

        # titulo
        texto_titulo = self.fonte_grande.render(titulo, True, (0, 0, 0))

        titulo_x = (config.largura - texto_titulo.get_width()) // 2
        titulo_y = config.altura // 7

        tela.blit(texto_titulo, (titulo_x + 5, titulo_y + 5))
        texto_titulo = self.fonte_grande.render(titulo, True, (255, 255, 255))
        tela.blit(texto_titulo, (titulo_x, titulo_y))

        # texto
        for texto, x, y in textos:
            texto_com_fonte = self.fonte.render(texto, True, (0, 0, 0))

            x_modificado = x - (texto_com_fonte.get_width() // 2)

            tela.blit(texto_com_fonte, (x_modificado + 5, y + 5))

            texto_com_fonte = self.fonte.render(texto, True, (255, 255, 255))
            tela.blit(texto_com_fonte, (x_modificado, y))

        pygame.display.flip()

    # metodos de animacao de ataque e movimento
    def animacao_movimento(self, frames_movimento, frames_idle, ultima_atualizacao, frame_atual, esta_em_movimento, esta_virado_esquerda):
        now = pygame.time.get_ticks()
        # delay de movimento
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

        if esta_virado_esquerda:
            frame = pygame.transform.flip(frame, True, False)

        image = frame

        return image, ultima_atualizacao, frame_atual

    def animacao_ataque(self, frames_ataque, frames_idle, ultima_atualizacao, frame_atual, esta_virado_esquerda, esta_atacando, delay=90):
        now = pygame.time.get_ticks()

        # esse calculo verifica se o fram precisa ser atualizado usando a passagem de ticks
        if now - ultima_atualizacao >= delay:
            ultima_atualizacao = now
            frame_atual += 1

            # fim da animacao
            if frame_atual >= len(frames_ataque):
                esta_atacando = False
                frame_atual = 0

                frame = frames_idle[0]
                if esta_virado_esquerda:
                    frame = pygame.transform.flip(frame, True, False)
                image = frame

                return image, ultima_atualizacao, frame_atual, esta_atacando

        # controle da frame e direcao da frame atuais
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
                texto_go = self.fonte_grande.render("GO >", True, (0, 0, 0))
                tela.blit(texto_go, (config.largura -
                          245, config.altura // 7 + 5))
                texto_go = self.fonte_grande.render(
                    "GO >", True, (255, 255, 255))
                tela.blit(texto_go, (config.largura - 250, config.altura // 7))
