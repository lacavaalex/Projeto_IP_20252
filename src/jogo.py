import pygame

from configuracoes import Configuracoes
from jogador import Jogador
from inimigo import Inimigo
from interface import Interface
from item import Item

config = Configuracoes()

class Jogo:

    def __init__(self, tela):
        self.tela = tela

        #variavel de controle
        self.rodando = True
        
        #relogio interno do pygame
        self.clock = pygame.time.Clock()

        #sistema de progressão
        self.fase_atual = 1
        self.liberado_para_avancar = False

         # DADOS DAS FASES
        self.dados_fases = {
            1: { "nome": "Niate", "cor": (50, 50, 100), "lixos": None,
                 "inimigos": [(config.largura - 400, 450), (config.largura - 600, 500)]},
            
            2: { "nome": "Ponte", "cor": (60, 60, 120), "lixos": [(config.largura // 2, config.altura * 3 // 4)],
                 "inimigos": [(config.largura - 200, 450), (config.largura - 700, 450), (config.largura - 400, 400)]},
            
            3: { "nome": "Churrasquito", "cor": (100, 60, 40), "lixos": [(config.largura * 3 // 4 + 100, config.altura * 3 // 4 - 100)],
                 "inimigos": [(config.largura - 100, 400), (config.largura - 300, 500), (config.largura - 500, 350)]},

            4: { "nome": "CAC", "cor": (40, 40, 40), "lixos": None,
                 "inimigos": [(config.largura - 400, 450), (config.largura - 500, 500)]},
            
            5: { "nome": "CTG", "cor": (30, 50, 30), "lixos": [(config.largura // 4, config.altura * 3 // 4), (config.largura * 3 // 4 + 100, config.altura * 3 // 4 - 100)],
                 "inimigos": [(config.largura - 200, 400), (config.largura - 600, 400)]},
            
            6: { "nome": "Caminho CIn", "cor": (20, 20, 20), "lixos": [(config.largura // 2, config.altura * 3 // 4)],
                 "inimigos": [(config.largura - 100, 450), (config.largura - 300, 450), (config.largura - 500, 450)]},

            7: { "nome": "Fachada CIn", "cor": (100, 200, 100), "lixos": None,
                 "inimigos": [(config.largura - 300, 500), (config.largura - 500, 500)]},
            
            8: { "nome": "Bloco A", "cor": (200, 200, 200), "lixos": [(config.largura // 5, config.altura * 4 // 5)],
                 "inimigos": [(config.largura - 100, 400), (config.largura - 700, 450)]},
            
            9: { "nome": "Grad 5", "cor": (50, 50, 200), "lixos": None,
                 "inimigos": [(config.largura - 200, 400), (config.largura - 300, 500), (config.largura - 400, 400)]},

            10: { "nome": "BOSS: WALLYSON", "cor": (100, 0, 0), "lixos": None,
                  "inimigos": [(config.largura - 600, 450)]}
        }

        #define os limites de movimento do jogador
        self.limites_tela = {
            'esquerda': 0, 
            'direita': config.largura, 
            'topo': 0, 
            'baixo': config.altura
        }
        
        #posicao inicial (central)
        self.x_inicial = config.largura // 7
        self.y_inicial = config.altura // 2
        
        self.interface = Interface()
        self.jogador = Jogador(self.x_inicial, self.y_inicial, self.limites_tela)

        self.iniciar_fase(self.fase_atual)

    def iniciar_fase(self, numero):
        self.liberado_para_avancar = False
        
        #fim de jogo
        if numero > len(self.dados_fases):
            print("ZEROU O JOGO!")
            return

        posicoes_inimigos = self.dados_fases[numero]["inimigos"]
        posicoes_lixos = self.dados_fases[numero]["lixos"]

        #posiciona os inimigos e os lixos, que  existem dentro de um group no pygame
        self.grupo_inimigos = pygame.sprite.Group() 
        self.gerar_inimigos(posicoes_inimigos, self.limites_tela)

        self.grupo_itens = pygame.sprite.Group()
        self.gerar_itens("lixo", posicoes_lixos)

        #posiciona o jogador
        self.jogador.hitbox.topleft = (self.x_inicial, self.y_inicial)
        self.jogador.vivo = True
        self.jogador.vida = self.jogador.VIDA_MAX

    #geracao dos multiplos inimigos
    def gerar_inimigos(self, posicoes_inimigos, limites):
        for x, y in posicoes_inimigos:
            self.grupo_inimigos.add(Inimigo(x, y, limites))

    #geracao dos itens
    def gerar_itens(self, tipo, dados_itens):
        if dados_itens is not None:
            for x, y in dados_itens:
                self.grupo_itens.add(Item(x, y, tipo))

    #funcao que verifica se podemos passar para a proxima fase
    def checar_progresso(self):
        if len(self.grupo_inimigos) == 0:
            self.liberado_para_avancar = True 
            
            if self.liberado_para_avancar:
                if self.jogador.hitbox.right >= config.largura - config.largura/7:
                    self.fase_atual += 1
                    self.iniciar_fase(self.fase_atual)

    #gameloop
    def run(self):
        while self.rodando:
            self.clock.tick(config.fps)
            self.handle_events()
            self.update()
            #fim
            if self.fase_atual == 11:
                self.rodando = False
            else:
                self.draw(self.dados_fases[self.fase_atual])

    #recebe inputs de teclado pelo modulo event
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.rodando = False

    #atualiza os ultimos inputs dentro do gameloop
    def update(self):
        keys = pygame.key.get_pressed()

        #controle de vida e morte do jogador e dos inimigos
        if self.jogador.vivo:
            self.jogador.update(keys, self.grupo_inimigos, self.grupo_itens)
        if not self.jogador.vivo:
            self.rodando = False
        for inimigo in self.grupo_inimigos:
            if inimigo.vivo:
                inimigo.update(self.jogador)
            else:
                inimigo.kill()
        
        for item in self.grupo_itens:
            if self.jogador.hitbox.colliderect(item.hitbox):
                if item.tipo == "lixo": 
                    self.jogador.bloquear_movimento()

        self.checar_progresso()

    #metodo contendo as funcionalidades graficas do pygame
    def draw(self, fase_atual):
        self.tela.fill(fase_atual["cor"]) 
        self.grupo_itens.draw(self.tela)
        self.interface.desenhar_go(self.tela, self.liberado_para_avancar)
        self.tela.blit(self.jogador.image, self.jogador.rect)
        self.grupo_inimigos.draw(self.tela)
        pygame.display.flip()