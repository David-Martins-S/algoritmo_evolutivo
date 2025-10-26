import pygame
import random
import csv

from criatura import Criatura
from comida import Comida
from globais import *
from gerenciador_estados import GerenciadorDeEstado

import genetica


pygame.init()
FONT = pygame.font.SysFont("Arial", 20)
BIG_FONT = pygame.font.SysFont("Arial", 48)

estado = GerenciadorDeEstado()


class Simulacao:
    def __init__(self):
        self.tela = pygame.display.get_surface()
        if self.tela is None:
            # criar surface caso main não tenha criado
            self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("Evolução - Simulação")
        self.clock = pygame.time.Clock()
        self.font = FONT

        self.geracao = 1
        self.passos = 0
        self.maior_geracao_atual = 0
        self.total_filhos_geracao = 0

        # populações
        self.criaturas = [Criatura(random.uniform(0, LARGURA), random.uniform(0, ALTURA))
                          for _ in range(NUM_CRIATURAS_INICIAL)]
        self.comidas = [Comida() for _ in range(NUM_COMIDAS_INICIAL)]

        # CSV
        if not os.path.isfile(CSV_ARQUIVO):
            with open(CSV_ARQUIVO, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Geração', 'População', 'Média de Visão', 'Média de Velocidade'])

    def salvar_dados(self):
        if not self.criaturas:
            media_visao = 0
            media_vel = 0
        else:
            media_visao = sum(c.visao for c in self.criaturas) / len(self.criaturas)
            media_vel = sum(c.velocidade for c in self.criaturas) / len(self.criaturas)
        with open(CSV_ARQUIVO, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([self.geracao, len(self.criaturas), round(media_visao, 2), round(media_vel,2)])

    def nova_geracao(self):
        novas = genetica.nova_geracao(self.criaturas, self.geracao)
        self.criaturas = novas
        self.comidas = [Comida() for _ in range(NUM_COMIDAS_INICIAL)]
        self.geracao += 1
        self.passos = 0

    def handle_event(self, evento):
        # captura ESC dentro da simulação
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                print("[Simulação] ESC pressionado — pausando")
                estado.pausar_jogo()

    def update(self):
        # Atualiza criaturas (movimento/comida)
        for c in self.criaturas[:]:
            alvo = None
            # tenta método encontrar_alvo/encontrar_comida compatível com sua Criatura
            if hasattr(c, 'encontrar_alvo'):
                alvo = c.encontrar_alvo(self.comidas)
            c.mover(alvo=alvo) if hasattr(c, 'mover') else None
            if hasattr(c, 'comer'):
                c.comer(self.comidas)

            # Evitar colisões e perceber vizinhos
            c.evitar_colisoes(self.criaturas)
            c.vizinhos = c.perceber_vizinhos(self.criaturas)

            # remove mortos por energia
            if hasattr(c, 'energia') and c.energia <= 0:
                try:
                    self.criaturas.remove(c)
                except ValueError:
                    pass

        self.passos += 1
        # fim de geração
        if not self.comidas or not self.criaturas or self.passos >= PASSOS_GERACAO:
            print(f"[Simulação] Fim da geração {self.geracao}")
            self.salvar_dados()
            self.nova_geracao()

    def draw(self, surface):
        surface.fill((20,20,20))
        # comida
        for comida in self.comidas:
            if hasattr(comida, 'desenhar'):
                comida.desenhar(surface)
            else:
                pygame.draw.circle(surface, (200,200,0), (int(getattr(comida,'x',0)), int(getattr(comida,'y',0))), getattr(comida,'raio',3))
        # criaturas
        for c in self.criaturas:
            if hasattr(c, 'desenhar'):
                c.desenhar(surface)
            else:
                pygame.draw.circle(surface, COR_INICIAL, (int(c.x), int(c.y)), 6)
        # estatísticas
        self.desenhar_estatisticas(surface)

    # def desenhar_estatisticas(self, surface):
    #     if self.criaturas:
    #         # === Estatísticas médias ===
    #         media_visao = sum(c.visao for c in self.criaturas) / len(self.criaturas)
    #         media_vel = sum(c.velocidade for c in self.criaturas) / len(self.criaturas)
    #         media_autoexploracao = sum(getattr(c, "autoexploracao", 0) for c in self.criaturas) / len(self.criaturas)
    #
    #         # === Geração mais recente ===
    #         maior_geracao = max(c.geracao for c in self.criaturas)
    #         total_filhos_geracao = sum(1 for c in self.criaturas if c.geracao == maior_geracao)
    #         self.maior_geracao_atual = maior_geracao
    #         self.total_filhos_geracao = total_filhos_geracao
    #
    #     else:
    #         media_visao = media_vel = media_autoexploracao = 0
    #         maior_geracao = 0
    #         total_filhos_geracao = 0
    #
    #     # === Texto exibido na tela ===
    #     texto = (
    #         f"Geração:{self.geracao} | "
    #         f"População:{len(self.criaturas)} | "
    #         f"Visão:{media_visao:.1f} | "
    #         f"Vel:{media_vel:.2f} | "
    #         # f"Aleatoriedade:{media_autoexploracao:.2f} | "
    #         # f"maior geração:{maior_geracao} | "
    #         f"Filhos:{total_filhos_geracao}"
    #     )
    #
    #     surf = self.font.render(texto, True, (255, 255, 255))
    #     surface.blit(surf, (10, 10))

    def desenhar_estatisticas(self, surface):
        if self.criaturas:
            # === Estatísticas médias ===
            media_visao = sum(c.visao for c in self.criaturas) / len(self.criaturas)
            media_vel = sum(c.velocidade for c in self.criaturas) / len(self.criaturas)
            media_autoexploracao = sum(getattr(c, "autoexploracao", 0) for c in self.criaturas) / len(self.criaturas)

            # === Contagem de sexos ===
            total_machos = sum(1 for c in self.criaturas if c.sexo == 'M')
            total_femeas = sum(1 for c in self.criaturas if c.sexo == 'F')

            # === Geração mais recente ===
            maior_geracao = max(c.geracao for c in self.criaturas)
            total_filhos_geracao = sum(1 for c in self.criaturas if c.geracao == maior_geracao)
            self.maior_geracao_atual = maior_geracao
            self.total_filhos_geracao = total_filhos_geracao

        else:
            media_visao = media_vel = media_autoexploracao = 0
            maior_geracao = 0
            total_filhos_geracao = 0
            total_machos = total_femeas = 0

        # === Texto exibido na tela ===
        texto = (
            f"Geração:{self.geracao} | "
            f"População:{len(self.criaturas)} "
            f"(M:{total_machos} / F:{total_femeas}) | "
            f"Visão:{media_visao:.1f} | "
            f"Vel:{media_vel:.2f} | "
            f"Filhos:{total_filhos_geracao}"
        )

        surf = self.font.render(texto, True, (255, 255, 255))
        surface.blit(surf, (10, 10))


