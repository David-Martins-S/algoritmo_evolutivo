import pygame
import random
import math
from globais import *

class Criatura:

    def __init__(self, x, y, visao=None, velocidade=None, cor=None):
        self.x = float(x)
        self.y = float(y)
        self.raio = 5
        self.cor = cor if cor is not None else COR_INICIAL  # azul
        self.visao = visao if visao is not None else random.randint(20, 60)
        self.velocidade = velocidade if velocidade is not None else random.uniform(MINIMO_VELOCIDADE, MAXIMO_VELOCIDADE)
        self.energia = 100.0
        self.comida_comida = 0

        # Direção persistente (ângulo em radianos)
        self.direcao = random.uniform(0, 2 * math.pi)
        self.passo_atual = 0
        self.passos_antes_de_mudar = random.randint(20, 80)

    def encontrar_alvo(self, comidas):
        """Retorna a comida mais próxima dentro do raio de visão (ou None)."""
        alvo = None
        menor_dist = float('inf')
        for comida in comidas:
            dist = math.dist((self.x, self.y), (comida.x, comida.y))
            if dist <= self.visao and dist < menor_dist:
                menor_dist = dist
                alvo = comida
        return alvo

    def mover(self, alvo=None):
        """Move a criatura. Se houver alvo, move em direção a ele.
           Caso contrário mantém direção persistente por alguns passos."""
        if alvo is not None:
            # movimento direto e suave em direção ao alvo
            dx = alvo.x - self.x
            dy = alvo.y - self.y
            dist = math.hypot(dx, dy)
            if dist > 0.001:
                # move com velocidade limitada
                passo_x = (dx / dist) * self.velocidade
                passo_y = (dy / dist) * self.velocidade
                self.x += passo_x
                self.y += passo_y
        else:
            # mantém direção por um número de passos antes de ajustar
            if self.passo_atual >= self.passos_antes_de_mudar:
                self.direcao += random.uniform(-0.7, 0.7)  # muda suavemente
                self.passos_antes_de_mudar = random.randint(20, 80)
                self.passo_atual = 0
            self.passo_atual += 1

            # deslocamento na direção atual
            self.x += math.cos(self.direcao) * self.velocidade
            self.y += math.sin(self.direcao) * self.velocidade

        # Mantém dentro da tela (rebate nas bordas refletindo a direção)
        colidiu = False
        if self.x < self.raio:
            self.x = self.raio
            self.direcao = math.pi - self.direcao
            colidiu = True
        elif self.x > LARGURA - self.raio:
            self.x = LARGURA - self.raio
            self.direcao = math.pi - self.direcao
            colidiu = True

        if self.y < self.raio:
            self.y = self.raio
            self.direcao = -self.direcao
            colidiu = True
        elif self.y > ALTURA - self.raio:
            self.y = ALTURA - self.raio
            self.direcao = -self.direcao
            colidiu = True

        # Consumo de energia proporcional ao deslocamento (leve relação com velocidade)
        self.energia -= 0.05 + (self.velocidade - 1.0) * 0.01
        if self.energia < 0:
            self.energia = 0.0

    def comer(self, comidas):
        """Verifica colisão com comida e consome apenas uma por frame."""
        for comida in comidas:
            if math.dist((self.x, self.y), (comida.x, comida.y)) < (self.raio + comida.raio):
                comidas.remove(comida)
                self.comida_comida += 1
                self.energia = min(self.energia + 30.0, 100.0)
                break

    def desenhar(self, tela):
        pygame.draw.circle(tela, self.cor, (int(self.x), int(self.y)), self.raio)
        # Desenha o círculo de visão sutil
        if CIRCULO_VISAO:
            pygame.draw.circle(tela, (125, 125, 255), (int(self.x), int(self.y)), int(self.visao), 1)
        # Barra de energia pequena acima
        #barra_larg = 16
        #barra_alt = 3
        #x0 = int(self.x - barra_larg // 2)
        #y0 = int(self.y - self.raio - 8)
        #pygame.draw.rect(tela, (40, 40, 40), (x0, y0, barra_larg, barra_alt))
        #pct = max(0.0, self.energia / 100.0)
        #pygame.draw.rect(tela, (50, 200, 50), (x0, y0, int(barra_larg * pct), barra_alt))