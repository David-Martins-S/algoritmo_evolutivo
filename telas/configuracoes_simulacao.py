# import pygame
# import globais
# from globais import salvar_config, ALTURA, LARGURA
# from estados_menu import MenuState
# from gerenciador_estados import GerenciadorDeEstado
#
# estado = GerenciadorDeEstado()
#
# posx_botao_salvar = (LARGURA / 11)*9
# posy_botao_salvar = (ALTURA / 7)*4
# posx_botao_voltar = (LARGURA / 11)*9
# posy_botao_voltar = (ALTURA / 7)*5
#
#
# class CampoTexto:
#     def __init__(self, x, y, largura, altura, texto_inicial, chave):
#         self.rect = pygame.Rect(x, y, largura, altura)
#         self.texto = str(texto_inicial)
#         self.chave = chave
#         self.ativo = False
#         self.cor_inativa = pygame.Color('gray30')
#         self.cor_ativa = pygame.Color('dodgerblue2')
#         self.cor = self.cor_inativa
#         self.fonte = pygame.font.SysFont("arial", 24)
#
#     def desenhar(self, tela):
#         pygame.draw.rect(tela, self.cor, self.rect, 2)
#         texto_surface = self.fonte.render(self.texto, True, (255, 255, 255))
#         tela.blit(texto_surface, (self.rect.x + 5, self.rect.y + 5))
#
#     def evento(self, event):
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             # Verifica se clicou dentro do campo
#             self.ativo = self.rect.collidepoint(event.pos)
#             self.cor = self.cor_ativa if self.ativo else self.cor_inativa
#         elif event.type == pygame.KEYDOWN and self.ativo:
#             if event.key == pygame.K_RETURN:
#                 self.ativo = False
#                 self.cor = self.cor_inativa
#             elif event.key == pygame.K_BACKSPACE:
#                 self.texto = self.texto[:-1]
#             else:
#                 self.texto += event.unicode
#
#     def get_valor(self):
#         # Tenta converter para float ou int automaticamente
#         try:
#             if '.' in self.texto:
#                 return float(self.texto)
#             else:
#                 return int(self.texto)
#         except ValueError:
#             return self.texto
#
#
# class TelaConfiguracoesSimulacao:
#
#     def __init__(self):
#         self.font = pygame.font.SysFont("arial", 28)
#         self.campos = []
#         self._criar_campos()
#
#         # Botões simples (sem imagens por enquanto)
#
#         self.botao_salvar = pygame.Rect(posx_botao_salvar, posy_botao_salvar, 200, 50)
#         self.botao_voltar = pygame.Rect(posx_botao_voltar, posy_botao_voltar, 200, 50)
#
#     def _criar_campos(self):
#         y = 100
#         espacamento = 50
#         for chave, valor in vars(globais).items():
#             if chave.isupper() and not chave.startswith("__"):
#                 # Ignora funções e não-numéricos
#                 if isinstance(valor, (int, float, bool, str, tuple, list)):
#                     if isinstance(valor, (tuple, list, bool)):
#                         continue  # evita tipos complexos neste primeiro momento
#                     campo = CampoTexto(400, y, 200, 30, valor, chave)
#                     self.campos.append((chave, campo))
#                     y += espacamento
#
#     def desenhar(self, tela):
#         tela.fill((40, 60, 70))
#         y = 100
#         for chave, campo in self.campos:
#             label = self.font.render(chave, True, (255, 255, 255))
#             tela.blit(label, (50, y))
#             campo.desenhar(tela)
#             y += 50
#
#         pygame.draw.rect(tela, (70, 200, 70), self.botao_salvar)
#         pygame.draw.rect(tela, (200, 70, 70), self.botao_voltar)
#         tela.blit(self.font.render("Salvar", True, (255, 255, 255)), (posx_botao_salvar, posy_botao_salvar))
#         tela.blit(self.font.render("Voltar", True, (255, 255, 255)), (posx_botao_voltar, posy_botao_voltar))
#
#     def eventos(self, event):
#         for _, campo in self.campos:
#             campo.evento(event)
#
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             if self.botao_salvar.collidepoint(event.pos):
#                 self.salvar_alteracoes()
#             elif self.botao_voltar.collidepoint(event.pos):
#                 estado.mudar_menu(MenuState.MAIN)
#
#     def salvar_alteracoes(self):
#         novos_valores = {}
#         for chave, campo in self.campos:
#             novos_valores[chave] = campo.get_valor()
#
#         # Atualiza o módulo globais
#         for chave, valor in novos_valores.items():
#             setattr(globais, chave, valor)
#
#         salvar_config(novos_valores)
#         print("Configurações da simulação salvas com sucesso!")

import pygame
import globais
from globais import salvar_config, ALTURA, LARGURA
from estados_menu import MenuState
from gerenciador_estados import GerenciadorDeEstado

estado = GerenciadorDeEstado()


class CampoTexto:
    def __init__(self, x, y, largura, altura, texto_inicial, chave):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = str(texto_inicial)
        self.chave = chave
        self.ativo = False
        self.cor_inativa = pygame.Color('gray40')
        self.cor_ativa = pygame.Color('dodgerblue2')
        self.cor_fundo = pygame.Color('gray15')
        self.cor = self.cor_inativa
        self.fonte = pygame.font.SysFont("consolas", 22)

    def desenhar(self, tela, offset_y):
        rect = self.rect.move(0, offset_y)
        pygame.draw.rect(tela, self.cor_fundo, rect, border_radius=6)
        pygame.draw.rect(tela, self.cor, rect, 2, border_radius=6)
        texto_surface = self.fonte.render(self.texto, True, (255, 255, 255))
        tela.blit(texto_surface, (rect.x + 8, rect.y + 4))

    def evento(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.ativo = self.rect.collidepoint(event.pos[0], event.pos[1] - TelaConfiguracoesSimulacao.scroll_y)
            self.cor = self.cor_ativa if self.ativo else self.cor_inativa
        elif event.type == pygame.KEYDOWN and self.ativo:
            if event.key == pygame.K_RETURN:
                self.ativo = False
                self.cor = self.cor_inativa
            elif event.key == pygame.K_BACKSPACE:
                self.texto = self.texto[:-1]
            else:
                self.texto += event.unicode

    def get_valor(self):
        try:
            if '.' in self.texto:
                return float(self.texto)
            else:
                return int(self.texto)
        except ValueError:
            return self.texto


class TelaConfiguracoesSimulacao:
    scroll_y = 0  # deslocamento global da rolagem

    def __init__(self):
        self.font = pygame.font.SysFont("arial", 26)
        self.campos = []
        self._criar_campos()

        self.botao_salvar = pygame.Rect(LARGURA - 260, ALTURA - 120, 200, 50)
        self.botao_voltar = pygame.Rect(LARGURA - 260, ALTURA - 60, 200, 50)

    def _criar_campos(self):
        y = 80
        espacamento = 55
        for chave, valor in vars(globais).items():
            if chave.isupper() and not chave.startswith("__"):
                if isinstance(valor, (int, float, str)) and not isinstance(valor, bool):
                    campo = CampoTexto(400, y, 220, 35, valor, chave)
                    self.campos.append((chave, campo))
                    y += espacamento
        self.altura_total = y

    def desenhar(self, tela):
        # fundo suave
        tela.fill((30, 45, 55))
        pygame.draw.rect(tela, (25, 35, 45), (0, 0, LARGURA, ALTURA), 0)

        offset_y = self.scroll_y

        y = 80
        for chave, campo in self.campos:
            label = self.font.render(chave, True, (255, 255, 255))
            tela.blit(label, (60, y + offset_y))
            campo.desenhar(tela, offset_y)
            y += 55

        # Botões
        for botao, cor, texto in [
            (self.botao_salvar, (50, 180, 80), "Salvar"),
            (self.botao_voltar, (180, 80, 80), "Voltar")
        ]:
            pygame.draw.rect(tela, cor, botao, border_radius=8)
            texto_surface = self.font.render(texto, True, (255, 255, 255))
            tela.blit(
                texto_surface,
                (botao.centerx - texto_surface.get_width() / 2, botao.centery - texto_surface.get_height() / 2)
            )

    def eventos(self, event):
        if event.type == pygame.MOUSEWHEEL:
            TelaConfiguracoesSimulacao.scroll_y += event.y * 25
            TelaConfiguracoesSimulacao.scroll_y = min(0, TelaConfiguracoesSimulacao.scroll_y)
            TelaConfiguracoesSimulacao.scroll_y = max(
                ALTURA - self.altura_total - 100, TelaConfiguracoesSimulacao.scroll_y
            )

        for _, campo in self.campos:
            campo.evento(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.botao_salvar.collidepoint(event.pos):
                self.salvar_alteracoes()
            elif self.botao_voltar.collidepoint(event.pos):
                estado.mudar_menu(MenuState.MAIN)

    def salvar_alteracoes(self):
        novos_valores = {}
        for chave, campo in self.campos:
            novos_valores[chave] = campo.get_valor()

        for chave, valor in novos_valores.items():
            setattr(globais, chave, valor)

        salvar_config(novos_valores)
        print("Configurações salvas e aplicadas com sucesso!")
