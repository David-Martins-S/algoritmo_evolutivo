import pygame
import random
import csv
import os

import genetica
from criatura import Criatura
from comida import Comida
from globais import *
from util import reiniciar_programa

class Simulacao:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("Evolução - Visão, Velocidade e Reprodução")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 20)

        self.geracao = 1
        self.passos = 0

        self.criaturas = [Criatura(random.uniform(0, LARGURA), random.uniform(0, ALTURA))
                          for _ in range(NUM_CRIATURAS_INICIAL)]
        self.comidas = [Comida() for _ in range(NUM_COMIDAS_INICIAL)]

        self.arquivo_csv = 'dados.csv'
        if not os.path.isfile(self.arquivo_csv):
            with open(self.arquivo_csv, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Geração', 'População', 'Média de Visão', 'Média de Velocidade'])

    def salvar_dados(self):
        if not self.criaturas:
            media_visao = 0
            media_velocidade = 0
        else:
            media_visao = sum(c.visao for c in self.criaturas) / len(self.criaturas)
            media_velocidade = sum(c.velocidade for c in self.criaturas) / len(self.criaturas)
        with open(self.arquivo_csv, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([self.geracao, len(self.criaturas), round(media_visao, 2), round(media_velocidade, 2)])

        geracao_finalizada = self.criaturas
        self.criaturas = genetica.nova_geracao(geracao_finalizada)
        self.comidas = [Comida() for _ in range(NUM_COMIDAS_INICIAL)]
        self.geracao += 1
        self.passos = 0

    def desenhar_estatisticas(self):
        if self.criaturas:
            media_visao = sum(c.visao for c in self.criaturas) / len(self.criaturas)
            media_vel = sum(c.velocidade for c in self.criaturas) / len(self.criaturas)
        else:
            media_visao = media_vel = 0
        texto = f"Geração: {self.geracao} | População: {len(self.criaturas)} | Média visão: {media_visao:.1f} | Média vel: {media_vel:.2f}"
        self.tela.blit(self.font.render(texto, True, (255, 255, 255)), (10, 10))

    def rodar(self):
        rodando = True
        while rodando:
            self.clock.tick(FPS)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        pygame.quit()
                        import sys
                        reiniciar_programa()

            self.tela.fill((20, 20, 20))

            # atualização das criaturas: encontrar alvo -> mover(alvo) -> comer
            for c in self.criaturas[:]:  # iteração sobre cópia
                alvo = c.encontrar_alvo(self.comidas)
                c.mover(alvo=alvo)
                c.comer(self.comidas)
                # remover criaturas sem energia
                if c.energia <= 0:
                    try:
                        self.criaturas.remove(c)
                    except ValueError:
                        pass  # já removida em outro lugar
                else:
                    c.desenhar(self.tela)

            for comida in self.comidas:
                comida.desenhar(self.tela)

            self.desenhar_estatisticas()
            pygame.display.flip()

            self.passos += 1
            # fim de geração: quando acabarem as comidas OU não houver criaturas
            if not self.comidas or not self.criaturas or self.passos >= PASSOS_GERACAO:
                # salvar dados
                self.salvar_dados()
                # debug log no terminal
                print(f"\n=== Fim da geração {self.geracao} ===")
                for idx, c in enumerate(self.criaturas):
                    print(f"Criatura #{idx+1}: comidas={c.comida_comida}, visao={c.visao}, vel={c.velocidade:.2f}, energia={c.energia:.1f}")
                # nova geração com regras de herança

                genetica.nova_geracao(self.criaturas)
