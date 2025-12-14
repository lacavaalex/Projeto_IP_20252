import pygame
from interface import Interface
from jogo import Jogo

def main():
    pygame.init()
    
    #instancia interface para poder instanciar jogo e dar inicio ao loop
    interface = Interface()
    tela = interface.dimensionar_tela()

    jogo = Jogo(tela)

    jogo.run() 

    pygame.quit()

if __name__ == '__main__':
    main()