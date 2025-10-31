import pygame
import random
from globais import LARGURA, ALTURA


COR_COMIDA = (80, 255, 80)

class Comida:
    def __init__(self, pos_x=None, pos_y=None):
        self.x = pos_x if pos_x is not None else float(random.randint(0, LARGURA))
        self.y = pos_y if pos_y is not None else float(random.randint(0, ALTURA))
        self.raio = 3
        self.cor = (0, 255, 0)

    def desenhar(self, tela):
        pygame.draw.circle(tela, self.cor, (int(self.x), int(self.y)), self.raio)
