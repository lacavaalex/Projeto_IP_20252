import pygame

from configuracoes import Configuracoes
from jogador import Jogador
from inimigo import Inimigo
from chefe import Chefe
from interface import Interface
from item import Item
from textos import Textos

config = Configuracoes()


class Jogo:

    def __init__(self, tela):
        self.tela = tela
        
        # Musica de fundo
        pygame.mixer.music.set_volume(0.5)
        self.musica_fundo = pygame.mixer.music.load(
            'res/sound/In The End [Official HD Music Video] - Linkin Park [eVTXPUF4Oz4].mp3')
        pygame.mixer.music.play(-1)

        # Musica de morte do inimigo
        self.musica_morte_inimigo = pygame.mixer.Sound(
            'res/sound/morte inimigo.wav')

        # Musica de Game over
        self.musica_morte = False  # Variavel para saber quando deve ser tocada a musica
        self.musica_game_over = pygame.mixer.Sound('res/sound/game over.wav')

        #Musica de vitoria
        self.musica_vitoria = pygame.mixer.Sound('res/sound/WIN.mp3')
        self.ganhou = False

        # variavel de controle
        self.rodando = True

        # relogio interno do pygame
        self.clock = pygame.time.Clock()
        self.ultimo_input_tempo = 0
        self.cooldown_input = 500

        # game states
        self.estados_jogo = ["MENU", "HISTORIA_1", "HISTORIA_2",
                             "JOGANDO", "MORTE", "VITORIA", "CHECKPOINT", "CONTROLES"]
        self.estado = "MENU"

        # sistema de progressão
        self.fase_atual = 1
        self.liberado_para_avancar = False
        self.eh_checkpoint = False
        self.item_checkpoint_gerado = False
        self.itens_coletados = []
        self.item_checkpoint_nome = ""
        self.imagem_fundo_atual = None

        # DADOS DAS FASES
        self.dados_fases = {
            1: {"nome": "Niate", "fundo": 'res/sprites_textura/niate pixelado.png', "lixos": None,
                "inimigos": [(config.largura - 400, 450), (config.largura - 600, 500)],
                "checkpoint": False},

            2: {"nome": "Ponte", "fundo": 'res/sprites_textura/ponte pixelada.png', "lixos": [(config.largura // 2, config.altura * 3 // 4)],
                "inimigos": [(config.largura - 270, 600), (config.largura - 390, 550), (config.largura - 100, 530)],
                "checkpoint": False},

            3: {"nome": "Churrasquito", "fundo": 'res/sprites_textura/churrasquito pixelado.jpg', "lixos": [(config.largura // 4 + 100, config.altura * 3 // 4)],
                "inimigos": [(config.largura - 100, 500), (config.largura - 300, 550), (config.largura - 600, 510)],
                "checkpoint": True},

            4: {"nome": "CTG", "fundo": 'res/sprites_textura/engenharia pixelado.jpeg', "lixos": [(config.largura // 2, config.altura * 3 // 4)],
                "inimigos": [(config.largura - 400, 600), (config.largura - 700, 600)],
                "checkpoint": False},

            5: {"nome": "Caminho CIn", "fundo": 'res/sprites_textura/niate ctg pixelado.jpeg', "lixos": [(config.largura // 4, config.altura * 3 // 4), (config.largura * 3 // 4, config.altura * 6 // 7)],
                "inimigos": [(config.largura - 250, 600), (config.largura - 600, 420)],
                "checkpoint": False},

            6: {"nome": "Fachada CIn", "fundo": 'res/sprites_textura/fachada cin pixelado.png', "lixos": [(config.largura // 2, config.altura * 3 // 4)],
                "inimigos": [(config.largura // 2 - 200, 500), (config.largura - 500, 510), (config.largura - 700, 500)],
                "checkpoint": True},

            7: {"nome": "frente do cin", "fundo": 'res/sprites_textura/frente do cin pixelado.png', "lixos": [(config.largura // 4, config.altura * 3 // 4)],
                "inimigos": [(config.largura - 300, 500), (config.largura - 500, 420)],
                "checkpoint": False},

            8: {"nome": "Corredores Bloco A ", "fundo": 'res/sprites_textura/frente do cin pixelado.png', "lixos": [(config.largura // 5, config.altura * 4 // 5)],
                "inimigos": [(config.largura - 100, 400), (config.largura - 700, 450)],
                "checkpoint": False},

            9: {"nome": "Frente da Sala", "fundo": 'res/sprites_textura/praça pixelado.png', "lixos": [(config.largura // 2, config.altura * 3 // 4)],
                "inimigos": [(config.largura - 200, 400), (config.largura - 300, 500), (config.largura - 400, 400)],
                "checkpoint": True},

            10: {"nome": "Auditorio", "fundo": 'res/sprites_textura/frente do cin pixelado.png', "lixos": [(config.largura // 2, config.altura * 5 // 6), (config.largura * 3 // 4, config.altura * 3 // 4)],
                 "inimigos": [(config.largura - 600, 450)],
                 "checkpoint": False}
        }

        # define os limites de movimento do jogador
        self.limites_tela = {
            'esquerda': 0,
            'direita': config.largura,
            'topo': config.altura/3,
            'baixo': config.altura
        }

        # posicao inicial (central)
        self.x_inicial = 100 
        self.y_inicial = 550 

        self.interface = Interface()
        self.jogador = Jogador(
            self.x_inicial, self.y_inicial, self.limites_tela)
        self.textos = Textos(self.tela, self.interface, config, self.clock)

        self.jogo_iniciado = False

    def iniciar_fase(self, numero):
        self.tela.fill((0, 0, 0))

        self.item_checkpoint_gerado = False
        self.liberado_para_avancar = False

        if self.fase_atual <= len(self.dados_fases):
            caminho_fundo = self.dados_fases[numero]["fundo"]
            self.imagem_fundo_atual = self.interface.carregar_fundo(caminho_fundo)
            self.eh_checkpoint = self.dados_fases[numero]["checkpoint"]
        
        pygame.display.flip()

        # fim de jogo
        if self.fase_atual > len(self.dados_fases):
            self.estado = "VITORIA"
            return

        posicoes_inimigos = self.dados_fases[numero]["inimigos"]
        posicoes_lixos = self.dados_fases[numero]["lixos"]

        # posiciona os inimigos e os lixos, que  existem dentro de um group no pygame
        self.grupo_inimigos = pygame.sprite.Group()
        self.gerar_inimigos(posicoes_inimigos, self.limites_tela)

        self.grupo_itens = pygame.sprite.Group()
        self.gerar_itens("lixo", posicoes_lixos)

        # posiciona o jogador
        self.jogador.hitbox.topleft = (self.x_inicial, self.y_inicial)
        self.jogador.vivo = True

        self.estado = "JOGANDO"

    # geracao dos multiplos inimigos
    def gerar_inimigos(self, posicoes_inimigos, limites):
        for x, y in posicoes_inimigos:
            if self.fase_atual == len(self.dados_fases):
                self.grupo_inimigos.add(Chefe(x, y, limites))
            else:
                self.grupo_inimigos.add(Inimigo(x, y, limites))

    # geracao dos itens
    def gerar_itens(self, tipo, dados_itens):
        if dados_itens is not None:
            for x, y in dados_itens:
                self.grupo_itens.add(Item(x, y, tipo))

    # funcao que verifica se podemos passar para a proxima fase
    def checar_progresso(self):
        if not self.eh_checkpoint:
            if len(self.grupo_inimigos) == 0:
                self.liberado_para_avancar = True
        else:
            if self.fase_atual == 3:
                self.item_checkpoint_nome = "hamburger"
                tamanho_colecao = 1
            elif self.fase_atual == 6:
                self.item_checkpoint_nome = "cracha"
                tamanho_colecao = 2
            elif self.fase_atual == 9:
                self.item_checkpoint_nome = "notebook"
                tamanho_colecao = 3

            # criacao dos itens de final das fases do checkpoints, e verificacao de coleta
            if len(self.grupo_inimigos) == 0 and not self.item_checkpoint_gerado:
                self.gerar_itens(self.item_checkpoint_nome, [
                                 (config.largura // 2, 650)])
                self.item_checkpoint_gerado = True

            if len(self.grupo_inimigos) == 0 and len(self.itens_coletados) == tamanho_colecao:
                self.liberado_para_avancar = True

        if self.liberado_para_avancar:
            if self.jogador.hitbox.right >= config.largura - config.largura/11:
                self.fase_atual += 1
                if self.eh_checkpoint:
                    self.estado = "CHECKPOINT"
                else:
                    self.iniciar_fase(self.fase_atual)

    # gameloop
    def run(self):
        while self.rodando:
            now = pygame.time.get_ticks()
            pode_avancar = now - self.ultimo_input_tempo > self.cooldown_input

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.rodando = False
                    return

                if event.type == pygame.KEYDOWN:

                    if pode_avancar:

                        if self.estado == "MENU":
                            if event.key == pygame.K_RETURN:
                                self.estado = "HISTORIA_1"
                                self.ultimo_input_tempo = now
                            elif event.key == pygame.K_c:
                                self.estado = "CONTROLES"
                                self.ultimo_input_tempo = now

                        elif self.estado == "HISTORIA_1" or self.estado == "HISTORIA_2":
                            if event.key == pygame.K_RETURN:
                                self.iniciar_fase(self.fase_atual)
                                self.ultimo_input_tempo = now

                        elif self.estado == "MORTE":
                            if event.key == pygame.K_RETURN:
                                # reset
                                self.fase_atual = 1
                                self.itens_coletados = []
                                self.jogador.resetar_atributos(self)
                                self.estado = "MENU"
                                self.ultimo_input_tempo = now
                                # reseta o som
                                self.musica_morte = False
                                self.ganhou = False
                                # Volta a música de fundo do jogo
                                pygame.mixer.music.play(-1)

                        elif self.estado == "VITORIA":
                            if event.key == pygame.K_RETURN:
                                self.rodando = False
                                self.ultimo_input_tempo = now

                        elif self.estado == "CONTROLES":
                            if event.key == pygame.K_RETURN:
                                self.estado = "MENU"
                                self.ultimo_input_tempo = now

                        elif self.estado == "CHECKPOINT":
                            if event.key == pygame.K_RETURN:
                                if self.fase_atual == len(self.dados_fases):
                                    self.estado = "HISTORIA_2"
                                else:
                                    self.iniciar_fase(self.fase_atual)
                                self.ultimo_input_tempo = now

            self.clock.tick(config.fps)

            # menu inicial
            if self.estado == "MENU":
                self.textos.mostrar_tela_inicio()

            # historia
            elif self.estado == "HISTORIA_1" or self.estado == "HISTORIA_2":
                fase_historia = int(self.estado[-1])
                self.textos.mostrar_tela_historia(fase_historia)

            # loop do jogo ativo
            elif self.estado == "JOGANDO":
                self.update()
                self.draw()

            # tela de derrota
            elif self.estado == "MORTE":
                self.textos.mostrar_tela_morte()

                # IF de controle da tela de game over
                if not self.musica_morte:
                    pygame.mixer.music.stop()
                    self.musica_game_over.play(0)
                    self.musica_morte = True

            # tela de vitoria
            elif self.estado == "VITORIA":
                self.textos.mostrar_tela_vitoria()

                if not self.ganhou:
                    pygame.mixer.music.stop()
                    self.musica_vitoria.play()
                    self.ganhou = True

            # tela de instrucoes de controle
            elif self.estado == "CONTROLES":
                self.textos.mostrar_tela_controles()

            # tela de mensagem apos checkpoint
            elif self.estado == "CHECKPOINT":
                self.textos.mostrar_tela_checkpoint(self.item_checkpoint_nome)

    # atualiza os ultimos inputs dentro do gameloop
    def update(self):
        keys = pygame.key.get_pressed()

        if self.jogador.vivo:

            self.jogador.interagir_com_item(
                self.grupo_itens, self.itens_coletados)
            self.jogador.update(keys, self.grupo_inimigos,
                                self.grupo_itens, self.itens_coletados)
            for inimigo in self.grupo_inimigos:

                if inimigo.vivo:
                    inimigo.update(self.jogador)
                else:
                    self.musica_morte_inimigo.play()
                    inimigo.kill()

            self.checar_progresso()

        else:
            self.estado = "MORTE"

    # metodo contendo as funcionalidades graficas do pygame
    def draw(self):
        if self.fase_atual <= len(self.dados_fases):
            #cenario
            if self.imagem_fundo_atual:
                self.tela.blit(self.imagem_fundo_atual, (0, 0))
            self.interface.desenhar_chao(
                self.tela, self.limites_tela, self.fase_atual)

            # entidades
            self.grupo_itens.draw(self.tela)
            self.tela.blit(self.jogador.image, self.jogador.rect)
            self.grupo_inimigos.draw(self.tela)

            # layout
            if self.fase_atual == len(self.dados_fases):
                for inimigo in self.grupo_inimigos:
                    if isinstance(inimigo, Chefe) and inimigo.vivo:
                        largura_total_coracoes = 10 * 30
                        x_boss = config.largura - largura_total_coracoes - 100

                        texto_boss = self.interface.fonte.render(
                            "Wallyson", True, (255, 255, 255))
                        self.tela.blit(texto_boss, (x_boss + 20, 20))

                        self.interface.desenhar_vida(
                            self.tela, inimigo.vida, inimigo.vida_max, 4, x_boss, 40)

            self.interface.desenhar_vida(
                self.tela, self.jogador.vida, self.jogador.VIDA_MAX, self.jogador._quantidade_coracoes, 20, 40)
            self.interface.mostrar_itens_coletados(
                self.tela, self.itens_coletados)

            # texto
            self.interface.desenhar_go(self.tela, self.liberado_para_avancar)

        pygame.display.flip()
