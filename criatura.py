import pygame
import random
import math
import globais


BARREIRA_X = globais.LARGURA / 2

class Criatura:


    def __init__(self, x, y, visao=None, velocidade=None, cor=None, geracao=None,
                 idade=None, sexo=None, risco=None, family_id=None, altruismo=None, doou_comida=None,
                 autoexploracao=None):
        self.x = float(x)
        self.y = float(y)
        self.sexo = sexo if sexo is not None else random.choice(['M', 'F'])
        self.raio = 5
        self.cor = cor if cor is not None else (0, 100, 255) if self.sexo == 'M' else (255, 192, 203)
        self.visao = visao if visao is not None else random.randint(globais.MINIMO_VISAO, globais.MAXIMO_VISAO)
        self.risco = risco if risco is not None else random.uniform(globais.MINIMO_RISCO, globais.MAXIMO_RISCO)
        self.velocidade = velocidade if velocidade is not None else random.uniform(
            globais.MINIMO_VELOCIDADE, globais.MAXIMO_VELOCIDADE)
        self.energia = 100.0
        self.comida_comida = 0
        self.geracao = geracao if geracao is not None else 1
        self.idade = idade if idade is not None else 15
        self.autoexploracao = (
            autoexploracao) if autoexploracao is not None else random.uniform(0.0, 1.0)
        self.detectou_parceiro = False
        self.doou_comida = 0
        self.direcao = random.uniform(0, 2 * math.pi)
        self.passo_atual = 0
        self.passos_antes_de_mudar = random.randint(20, 80)
        self.parceiras_recentes = set()
        self.encontros_recentes = set()
        self.doou_comida = doou_comida if doou_comida is not None else 0
        self.colonia = None

        # self.family_id = family_id if family_id is not None else random.randint(1, 1000000)
        self.family_id = family_id if family_id is not None else random.choice(globais.ANT_FAMILY_NAMES)
        self.altruismo = altruismo if altruismo is not None else random.uniform(0.0, 0.1)  # tendência a doar

    def encontrar_alvo(self, comidas):
        """Retorna a comida mais próxima dentro do raio de visão (ou None)."""
        alvo = None
        menor_dist = float('inf')
        for comida in comidas:
            dist = math.dist((self.x, self.y), (comida.x, comida.y))
            if globais.BARREIRA_ATIVADA:
                if self.colonia.lado_colonia == "esquerda" and comida.x < BARREIRA_X:
                    if dist <= self.visao and dist < menor_dist:
                        menor_dist = dist
                        alvo = comida
                if self.colonia.lado_colonia == "direita" and comida.x > BARREIRA_X:
                    if dist <= self.visao and dist < menor_dist:
                        menor_dist = dist
                        alvo = comida
            else:
                if dist <= self.visao and dist < menor_dist:
                    menor_dist = dist
                    alvo = comida
        return alvo

    def mover(self, alvo=None):
        """Move a criatura em direção ao alvo (se houver) ou aleatoriamente."""
        if alvo is not None:
            dx = alvo.x - self.x
            dy = alvo.y - self.y
            dist = math.hypot(dx, dy)
            if dist > 0.001:
                passo_x = (dx / dist) * self.velocidade
                passo_y = (dy / dist) * self.velocidade
                self.x += passo_x
                self.y += passo_y
        else:

            if self.passo_atual >= self.passos_antes_de_mudar:
                # quanto maior a autoexploração, maior a variação de direção
                variacao = self.autoexploracao * random.uniform(-0.7, 0.7)
                self.direcao += variacao
                self.passos_antes_de_mudar = random.randint(20, 80)
                self.passo_atual = 0
            self.passo_atual += 1

            self.x += math.cos(self.direcao) * self.velocidade
            self.y += math.sin(self.direcao) * self.velocidade

            # limites da tela
            if self.x <= 0 or self.x >= globais.LARGURA:
                self.direcao = math.pi - self.direcao
            if self.y <= 0 or self.y >= globais.ALTURA:
                self.direcao = -self.direcao

            if globais.BARREIRA_ATIVADA:
                if self.x < BARREIRA_X and self.colonia.lado_colonia == "esquerda":
                    # Está do lado esquerdo tentando atravessar
                    self.direcao = math.pi - self.direcao
                if self.x < BARREIRA_X and self.colonia.lado_colonia == "direita":
                    # Está do lado esquerdo tentando atravessar
                    self.direcao = math.pi - self.direcao

    def comer(self, comidas):
        """Verifica colisão com comida e consome apenas uma por frame."""
        for comida in comidas:
            if math.dist((self.x, self.y), (comida.x, comida.y)) < (self.raio + comida.raio):
                comidas.remove(comida)
                self.comida_comida += 1
                self.energia = min(self.energia + 30.0, 100.0)
                break

    def evitar_colisoes(self, criaturas):
        """Evita que as criaturas se sobreponham fisicamente."""
        for outra in criaturas:
            if outra is self:
                continue
            dist = math.dist((self.x, self.y), (outra.x, outra.y))
            soma_raios = self.raio + outra.raio
            if 0 < dist < soma_raios:  # colisão detectada
                # Calcula direção de separação
                dx = (self.x - outra.x) / dist
                dy = (self.y - outra.y) / dist
                overlap = soma_raios - dist

                # Move cada uma metade da distância de sobreposição
                self.x += dx * overlap / 2
                self.y += dy * overlap / 2
                outra.x -= dx * overlap / 2
                outra.y -= dy * overlap / 2

    # toda a interação entre criaturas está acontecendo aqui
    def perceber_vizinhos(self, criaturas):
        """Retorna lista de criaturas próximas e define se detectou parceiro reprodutivo."""
        vizinhos = []

        # inicializa o controle de parceiras, se ainda não existir
        if not hasattr(self, "parceiras_recentes"):
            self.parceiras_recentes = set()

        for outra in criaturas:
            if outra is self:
                continue

            dist = math.dist((self.x, self.y), (outra.x, outra.y))
            # se está 'vendo' outra criatura
            if dist <= self.visao:
                vizinhos.append(outra)

                # condição mínima de percepção reprodutiva
                if (self.sexo == 'M' and outra.sexo == 'F') and self.comida_comida >= 1 and outra.comida_comida >= 1:
                    # verifica se já interagiu com essa fêmea
                    if id(outra) not in self.parceiras_recentes and not outra.detectou_parceiro:
                        # decide se vai gastar energia ou não
                        if self.comida_comida > 1 or random.random() < self.risco:
                            self.comida_comida -= 1
                            self.detectou_parceiro = True
                            outra.detectou_parceiro = True
                            # passa para a mãe o gene de risco do pai
                            outra.risco = self.risco
                            self.parceiras_recentes.add(id(outra))
                        # caso contrário, ele decide não gastar energia agora
                        else:
                            self.parceiras_recentes.add(id(outra))
                elif self.sexo == 'F' and outra.sexo == 'M':
                    # Fêmeas apenas aguardam machos decidirem
                    pass

                # verifica se a outra é da família e pode doar comida
                self.tentar_doar(outra)

        return vizinhos

    def tentar_doar(self, outra):

        if not hasattr(self, "encontros_recentes"):
            self.encontros_recentes = set()

        if id(outra) not in self.encontros_recentes:
            mesma_familia = True if self.family_id == outra.family_id else False
            sentindo_se_altruista = random.random() < self.altruismo
            esta_gravida = self.detectou_parceiro

            # apenas doa comida se não estiver grávida e se a outra for da mesma família
            if not esta_gravida and mesma_familia:

                # se encontra alguém da mesma família sem comida e está com comida "sobrando"
                if sentindo_se_altruista:
                    if self.comida_comida > 1 and outra.comida_comida == 0:
                        print("doando comida para alguém com fome")
                        self.comida_comida -= 1
                        outra.comida_comida += 1
                        self.doou_comida += 1

                    # se encontra uma fêmea grávida da mesma família com menos de 2 comidas
                    elif outra.detectou_parceiro and outra.comida_comida < 2:
                        if self.comida_comida > 1 or random.random() < self.risco:
                            print("doando comida para uma grávida")
                            self.comida_comida -= 1
                            outra.comida_comida += 1
                            self.doou_comida += 1

        self.encontros_recentes.add(id(outra))

    def desenhar(self, tela):
        pygame.draw.circle(tela, self.cor, (int(self.x), int(self.y)), self.raio)
        # Desenha o círculo de visão sutil
        if globais.MOSTRA_CIRCULO_VISAO:
            pygame.draw.circle(tela, (125, 125, 255), (int(self.x), int(self.y)), int(self.visao), 1)

        # Barra de energia pequena acima
        if globais.MOSTRA_BARRA_ENERGIA:
            barra_larg = 16
            barra_alt = 3
            x0 = int(self.x - barra_larg // 2)
            y0 = int(self.y - self.raio - 8)
            pygame.draw.rect(tela, (40, 40, 40), (x0, y0, barra_larg, barra_alt))
            pct = max(0.0, self.energia / 100.0)
            pygame.draw.rect(tela, (50, 200, 50), (x0, y0, int(barra_larg * pct), barra_alt))

        # === Exibir número da geração ===
        if globais.MOSTRA_TEXTO_CABECA_CRIATURA:
            cor_texto = (255, 255, 0)
            # if hasattr(self, "colonia"):
            #     cor_texto = (255, 255, 0) if self.colonia.lado_colonia == "esquerda" else (0, 255, 255)
            font = pygame.font.SysFont('Arial', 12)
            texto = font.render(f"{self.family_id}", True, cor_texto)
            texto_rect = texto.get_rect(center=(int(self.x), int(self.y - self.raio - 16)))
            tela.blit(texto, texto_rect)

        # --- desenhar pontos de comida abaixo ---
        if globais.MOSTRA_COMIDA_COMIDA:
            n = getattr(self, "comida_comida", 0)
            if n > 0:
                espacamento = 5
                base_y = int(self.y + self.raio + 5)
                total_pontos = min(n, 3)
                total_largura = (total_pontos - 1) * espacamento

                # desenha 1 a 4 pontos
                for i in range(total_pontos):
                    x_ponto = int(self.x - total_largura // 2 + i * espacamento)
                    pygame.draw.circle(tela, (0, 255, 0), (x_ponto, base_y), 2)

                # adiciona um "+" se tiver mais que 4 comidas
                if n > 3:
                    font = pygame.font.SysFont(None, 14)
                    texto = font.render("+", True, (0, 255, 0))
                    tela.blit(texto, (self.x + total_largura // 2 + 4, base_y - texto.get_height() // 2))

        # linha de ligação
        if globais.MOSTRA_LINHA_LIGACAO:
            if hasattr(self, 'vizinhos'):
                for v in self.vizinhos:
                    pygame.draw.line(tela, (100, 100, 255), (int(self.x), int(self.y)), (int(v.x), int(v.y)), 1)

        # indicador de parceiro detectado
        if globais.MOSTRA_GRAVIDEZ:
            if getattr(self, "detectou_parceiro", False) and getattr(self, "sexo") == 'F':
                pygame.draw.circle(tela, (255, 255, 0), (int(self.x), int(self.y)), self.raio + 3, 1)
