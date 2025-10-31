import pygame
import random
import csv
import os

from estatisticas import Estatisticas
import globais

from criatura import Criatura
from comida import Comida
from gerenciador_estados import GerenciadorDeEstado

import genetica

pygame.init()
FONT = pygame.font.Font(None, 20)
BIG_FONT = pygame.font.Font(None, 48)

estado = GerenciadorDeEstado()
estatisticas = Estatisticas()


class Simulacao:
    def __init__(self):
        self.tela = pygame.display.get_surface()
        if self.tela is None:
            # criar surface caso main não tenha criado
            self.tela = pygame.display.set_mode((globais.LARGURA, globais.ALTURA))
        pygame.display.set_caption("Evolução - Simulação")
        self.clock = pygame.time.Clock()
        self.font = FONT

        self.geracao = 1
        self.passos = 0
        self.maior_geracao_atual = 0
        self.total_filhos_geracao = 0

        # populações
        self.criaturas = [Criatura(random.uniform(0, globais.LARGURA), random.uniform(0, globais.ALTURA))
                          for _ in range(globais.NUM_CRIATURAS_INICIAL)]
        self.comidas = [Comida() for _ in range(globais.NUM_COMIDAS_INICIAL)]

        # CSV
        if not os.path.isfile(globais.CSV_ARQUIVO):
            with open(globais.CSV_ARQUIVO, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Geração',
                                 'Machos',
                                 'Fêmeas',
                                 'População',
                                 'Média de Visão',
                                 'Média de Velocidade',
                                 'Média de Risco',
                                 'Total de filhos da geração',
                                 'Detecção de parceiros',
                                 'Taxa de doações'])

    def salvar_dados(self):
        with open(globais.CSV_ARQUIVO, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                estatisticas.geracao_atual,
                estatisticas.total_machos,
                estatisticas.total_femeas,
                estatisticas.populacao,
                estatisticas.media_visao,
                estatisticas.media_vel,
                estatisticas.media_risco,
                estatisticas.total_filhos_geracao,
                estatisticas.detectaram_parceiros,
                estatisticas.media_altruismo])

    def nova_geracao(self):
        novas = genetica.nova_geracao(self.criaturas, self.geracao)
        self.criaturas = novas
        self.comidas = [Comida() for _ in range(globais.NUM_COMIDAS_INICIAL)]
        self.geracao += 1
        self.passos = 0

    def handle_event(self, evento):
        # captura ESC dentro da simulação
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                print("[Simulação] ESC pressionado — pausando")
                estado.pausar_jogo()
            if evento.key == pygame.K_r and getattr(self, "estado", "") == "fim":
                self.reiniciar_simulacao()
        # 👇 Adicionar comida com clique esquerdo
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:  # 1 = botão esquerdo
            print("mouse clicado")
            pos_x, pos_y = pygame.mouse.get_pos()
            from comida import Comida  # ajuste o import conforme seu projeto
            nova_comida = Comida(pos_x, pos_y)
            self.comidas.append(nova_comida)
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 3:
            if self.comidas:
                pos_x, pos_y = pygame.mouse.get_pos()
                comida_mais_proxima = min(self.comidas, key=lambda c: (c.x - pos_x) ** 2 + (c.y - pos_y) ** 2)
                self.comidas.remove(comida_mais_proxima)
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 2:
            print("botão do meio clicado")
            # pausar simulação
            estado.freeze() if not estado.esta_freezado() else estado.desfreezar()

    def reiniciar_simulacao(self):
        self.criaturas = [Criatura(random.uniform(0, globais.LARGURA), random.uniform(0, globais.ALTURA))
                          for _ in range(globais.NUM_CRIATURAS_INICIAL)]
        self.comidas = [Comida() for _ in range(globais.NUM_COMIDAS_INICIAL)]
        self.geracao = 1
        self.passos = 0
        self.estado = ""
        self.motivo_fim = ""
        print("[Simulação] Reiniciando a simulação")

    def update(self):
        if not estado.esta_freezado():
            for c in self.criaturas[:]:
                alvo = None
                if hasattr(c, 'encontrar_alvo'):
                    alvo = c.encontrar_alvo(self.comidas)
                c.mover(alvo=alvo) if hasattr(c, 'mover') else None
                if hasattr(c, 'comer'):
                    comida_antes = c.comida_comida
                    c.comer(self.comidas)
                    # if globais.LIGA_SOM_COMER:
                    #     if c.comida_comida > comida_antes:
                    #         if hasattr(self, "som_pop"):
                    #             self.som_pop.play()
                c.evitar_colisoes(self.criaturas)
                estava_gravida = c.detectou_parceiro
                doou_comida = c.doou_comida
                c.vizinhos = c.perceber_vizinhos(self.criaturas)
                if globais.LIGA_SOM_VUSH:
                    if c.detectou_parceiro != estava_gravida:
                        if hasattr(self, "som_vush"):
                                self.som_vush.play()
                if globais.LIGA_SOM_COMER:
                    if c.doou_comida > doou_comida:
                        if hasattr(self, "som_pop"):
                                self.som_pop.play()
                if hasattr(c, 'energia') and c.energia <= 0:
                    try:
                        self.criaturas.remove(c)
                    except ValueError:
                        pass

            self.passos += 1
            # fim de geração
            if not self.comidas or not self.criaturas or self.passos >= globais.PASSOS_GERACAO:
                print(f"[Simulação] Fim da geração {self.geracao}")
                self.salvar_dados()
                self.nova_geracao()

    def draw(self, surface):
        surface.fill((0, 0, 0))
        if getattr(self, "estado", "") == "fim":
            self.desenhar_tela_fim(surface)
            return
        for comida in self.comidas:
            if hasattr(comida, 'desenhar'):
                comida.desenhar(surface)
            else:
                pygame.draw.circle(surface, (200,200,0), (int(getattr(comida,'x',0)), int(getattr(comida,'y',0))), getattr(comida,'raio',3))
        for c in self.criaturas:
            if hasattr(c, 'desenhar'):
                c.desenhar(surface)
            else:
                pygame.draw.circle(surface, (100, 100, 255), (int(c.x), int(c.y)), 6)

        # estatísticas
        self.desenhar_estatisticas(surface)

    def desenhar_tela_fim(self, surface):
        surface.fill((10, 10, 10))
        linhas = [
            "💀 FIM DA SIMULAÇÃO 💀",
            "",
            self.motivo_fim,
            "",
            f"Geração alcançada: {self.geracao}",
            f"População final: {len(self.criaturas)}",
        ]
        # Estatísticas adicionais, se quiser
        if self.criaturas:
            media_visao = sum(c.visao for c in self.criaturas) / len(self.criaturas)
            media_vel = sum(c.velocidade for c in self.criaturas) / len(self.criaturas)
            linhas.append(f"Visão média: {media_visao:.2f}")
            linhas.append(f"Velocidade média: {media_vel:.2f}")

        # Renderiza o texto centralizado
        y = surface.get_height() // 3
        for linha in linhas:
            texto = self.font.render(linha, True, (255, 255, 255))
            rect = texto.get_rect(center=(surface.get_width() // 2, y))
            surface.blit(texto, rect)
            y += 40

        # Botão de reinício (opcional)
        texto_reset = self.font.render("Pressione [R] para reiniciar", True, (180, 180, 180))
        rect_reset = texto_reset.get_rect(center=(surface.get_width() // 2, y + 40))
        surface.blit(texto_reset, rect_reset)

    def calcular_estatisticas(self):
        criaturas = self.criaturas
        estatisticas.media_visao = round(sum(c.visao for c in criaturas) / len(criaturas), 2
                                         )
        estatisticas.media_vel = round(sum(c.velocidade for c in criaturas) / len(criaturas), 2
                                       )
        estatisticas.media_autoexploracao = round(
            sum(getattr(c, "autoexploracao", 0) for c in criaturas) / len(criaturas), 2
        )
        estatisticas.total_machos = sum(1 for c in criaturas if c.sexo == 'M')
        estatisticas.total_femeas = sum(1 for c in criaturas if c.sexo == 'F')
        estatisticas.media_risco = round(
            sum(getattr(c, "risco", 0) for c in criaturas if c.sexo == 'M') / estatisticas.total_machos, 2
        )
        estatisticas.media_altruismo = round(
            sum(getattr(c, "altruismo", 0) for c in criaturas) / len(criaturas), 2
        )
        estatisticas.comida_doada = sum(getattr(c, "doou_comida", 0) for c in criaturas)
        estatisticas.maior_geracao = max(c.geracao for c in criaturas)
        estatisticas.total_filhos_geracao = sum(1 for c in criaturas if c.geracao == estatisticas.maior_geracao)
        estatisticas.geracao_atual = self.geracao
        estatisticas.detectaram_parceiros = sum(1 for c in criaturas if c.detectou_parceiro)
        estatisticas.populacao = len(criaturas)

    def desenhar_estatisticas(self, surface):

        self.calcular_estatisticas()
        estatisticas.desenhar_estatisticas(surface)

        # Verifica extinção
        if len(self.criaturas) == 0:
            self.motivo_fim = "Todas as criaturas morreram."
            self.estado = "fim"
            if hasattr(self, "som_fim"):
                self.som_fim.play()
            return
        elif estatisticas.total_machos == 0:
            self.motivo_fim = "Não há mais machos. A reprodução tornou-se impossível."
            self.estado = "fim"
            return
        elif estatisticas.total_femeas == 0:
            self.motivo_fim = "Não há mais fêmeas. A reprodução tornou-se impossível."
            self.estado = "fim"
            return
