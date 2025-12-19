import pygame

class Textos():
    def __init__(self, tela, interface, config, clock):
        self.tela = tela
        self.interface = interface
        self.config = config

        self.clock = clock

        self.centro_x = self.config.largura // 2
        self.centro_y = self.config.altura // 2

        self.fundo_geral = 'res/sprites_textura/fundo_geral.png'
        

    # tela inicial
    def mostrar_tela_inicio(self):
        textos = [
            ("O PROJETO FINAL", self.centro_x, self.centro_y - 60),
            ("Pressione ENTER OU START para JOGAR",
             self.centro_x, self.centro_y + 40),
            ("Pressione C OU SELECT para ver os controles",
             self.centro_x, self.centro_y + 80)
        ]
        self.interface.mostrar_tela(
            self.tela, "ROGÉRIO vs WALLYSON:", textos, 'res/sprites_textura/tela_inicial.png')

    # tela de controles
    def mostrar_tela_controles(self):
        textos = [
            ("Movimento: W/A/S/D", self.centro_x, self.centro_y - 40),
            ("Atacar: ESPAÇO", self.centro_x, self.centro_y),
            ("Continuar: ENTER", self.centro_x, self.centro_y + 40)
        ]
        self.interface.mostrar_tela(
            self.tela, "CONTROLES", textos, self.fundo_geral)

    # tela de texto após checkpoint
    def mostrar_tela_checkpoint(self, item_coletado):
        if item_coletado == "hamburger":
            upgrade = "AGORA SIM EU TÔ COMIDO! ++VIDA"
        if item_coletado == "cracha":
            upgrade = "NENHUMA CATRACA ME PARA! ++VELOCIDADE"
        if item_coletado == "notebook":
            upgrade = "MEU PROJETO TÁ EM MÃOS! NADA PODE ME IMPEDIR! ++ATAQUE"

        titulo = f"Item Coletado: {item_coletado.upper()}!"
        textos = [
            (f"{upgrade}", self.centro_x, self.centro_y),
            ("Pressione ENTER ou START", self.centro_x, self.centro_y + 40)
        ]
        self.interface.mostrar_tela(self.tela, titulo, textos, self.fundo_geral)

    # tela de vitoria
    def mostrar_tela_vitoria(self):
        titulo = "WALLYSON FOI DERROTADO!"
        texto = [
            ("Você apresentou o projeto! Está APROVADO em IP!!",
             self.centro_x, self.centro_y),
            ("Parabéns pela vitória, e boa sorte no próximo período!",
             self.centro_x, self.centro_y + 40)
        ]
        self.interface.mostrar_tela(self.tela, titulo, texto, self.fundo_geral)

    # tela de derrota
    def mostrar_tela_morte(self):
        titulo = "GAME OVER"
        textos = [
            ("Você não conseguiu chegar a tempo,",
             self.centro_x, self.centro_y - 60),
            ("seu projeto não foi apresentado. Você REPROVOU.",
             self.centro_x, self.centro_y - 20),
            ('"Te vejo período que vem." - Recém-Monitor Wallyson',
             self.centro_x, self.centro_y + 20),
            ("Pressione ENTER ou START para voltar ao menu",
             self.centro_x, self.centro_y + 80)
        ]
        self.interface.mostrar_tela(self.tela, titulo, textos, self.fundo_geral)

    def mostrar_tela_historia(self, fase_historia):
        centro_x = self.config.largura // 2
        centro_y = self.config.altura // 2

        if fase_historia == 1:
            titulo = "UMA CORRIDA CONTRA O TEMPO!"

            textos = [
                ("É o dia da apresentação do projeto final de IP, Rogério.",
                 centro_x, centro_y - 120),
                ("Você desce do ônibus no NIATE, porém...", centro_x, centro_y - 80),
                ("UMA ABORDAGEM SURPRESA!", centro_x, centro_y - 40),
                ('Um homem desconhecido diz, ao roubar sua mochila:', centro_x, centro_y),
                ('"Wallyson mandou lembranças."', centro_x, centro_y + 40),
                ('"Mizinga, Wallyson! Sempre me sabotando pra eu reprovar!"',
                 centro_x, centro_y + 80),
                ("Alcance os capangas de Wallyson,", centro_x, centro_y + 120),
                ("seu CRACHA e NOTEBOOK estão com eles.", centro_x, centro_y + 160),
                ("Recupere-os antes de entrar no Cin.", centro_x, centro_y + 200),
                ("Mas antes, vá até o Churrasquito pra encher o bucho!",
                 centro_x, centro_y + 240),
                ("Pressione ENTER ou START para começar", centro_x, centro_y + 300)
            ]
            self.interface.mostrar_tela(
                self.tela, titulo, textos, self.fundo_geral)

        if fase_historia == 2:
            titulo = "O TRAIDOR APARECE!"

            textos = [
                ('"Rapaz, olha quem chegou cedo!", debochou Wallyson.',
                 centro_x, centro_y - 100),
                ('"Por hora, só nós dois estamos aqui,"', centro_x, centro_y - 60),
                ('"então vamos acabar logo com isso."', centro_x, centro_y - 20),
                ('"Meus capangas de Guabiraba não são os melhores,"',
                 centro_x, centro_y + 20),
                ('"Mas EU sou."', centro_x, centro_y + 60),
                ('"È hoje que tu volta a ser barman carpinense,"',
                 centro_x, centro_y + 100),
                ('"e nunca mais toca em um computador!"', centro_x, centro_y + 140),
                ('"E é, é?", você diz, furioso.', centro_x, centro_y + 200),
                ('"É HOJE QUE EU ACABO CONTIGO MIZINGA!"', centro_x, centro_y + 240),
                ("Pressione ENTER ou START para continuar", centro_x, centro_y + 300)
            ]
            self.interface.mostrar_tela(
                self.tela, titulo, textos, self.fundo_geral)
