import pygame
import random

LARGURA, ALTURA = 800, 600
COR_COMIDA = (80, 255, 80)

class Comida:
    def __init__(self):
        self.x = float(random.randint(0, LARGURA))
        self.y = float(random.randint(0, ALTURA))
        self.raio = 3
        self.cor = (0, 255, 0)

    def desenhar(self, tela):
        pygame.draw.circle(tela, self.cor, (int(self.x), int(self.y)), self.raio)
