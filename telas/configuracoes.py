# import pygame
# import globais
# from componentes.botao import Botao
# from gerenciador_estados import estado_global
# from estados_menu import MenuState
#
# class TelaConfiguracoes:
#     def __init__(self):
#         self.fonte = pygame.font.SysFont(None, 36)
#         self.configs = {
#             "NUM_CRIATURAS_INICIAL": str(globais.NUM_CRIATURAS_INICIAL),
#             "NUM_COMIDAS_INICIAL": str(globais.NUM_COMIDAS_INICIAL),
#             "PASSOS_GERACAO": str(globais.PASSOS_GERACAO),
#             "FPS": str(globais.FPS)
#         }
#         self.campos = {}
#         self.criar_campos()
#
#         self.botoes = [
#             Botao("SALVAR", 700, 900, 200, 60, (0,150,0), (0,200,0), self.salvar),
#             Botao("CANCELAR", 1000, 900, 200, 60, (150,0,0), (200,0,0), self.cancelar)
#         ]
#
#     def criar_campos(self):
#         y = 300
#         for chave, valor in self.configs.items():
#             rect = pygame.Rect(900, y, 200, 40)
#             self.campos[chave] = {"rect": rect, "texto": valor, "ativo": False}
#             y += 60
#
#     def salvar(self):
#         for chave, campo in self.campos.items():
#             try:
#                 valor = float(campo["texto"])
#                 setattr(globais, chave, valor)
#             except ValueError:
#                 pass  # ignora valores inválidos
#         self.gerenciador.mudar_tela("menu")
#
#     def cancelar(self):
#         estado_global.mudar_menu(MenuState.OPTIONS)
#
#
#     def desenhar(self, tela):
#         tela.fill((20, 20, 20))
#         y = 300
#         for chave, campo in self.campos.items():
#             label = self.fonte.render(chave, True, (255,255,255))
#             tela.blit(label, (600, y))
#             pygame.draw.rect(tela, (50,50,50), campo["rect"])
#             texto = self.fonte.render(campo["texto"], True, (255,255,255))
#             tela.blit(texto, (campo["rect"].x + 10, campo["rect"].y + 5))
#             y += 60
#
#         for botao in self.botoes:
#             botao.desenhar(tela)
#
#     def eventos(self, event):
#         for campo in self.campos.values():
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 campo["ativo"] = campo["rect"].collidepoint(event.pos)
#             if event.type == pygame.KEYDOWN and campo["ativo"]:
#                 if event.key == pygame.K_BACKSPACE:
#                     campo["texto"] = campo["texto"][:-1]
#                 elif event.key == pygame.K_RETURN:
#                     campo["ativo"] = False
#                 else:
#                     campo["texto"] += event.unicode

import pygame
from globais import LARGURA


pygame.init()
FONT = pygame.font.SysFont("Arial", 20)
BIG_FONT = pygame.font.SysFont("Arial", 48)

class TelaConfiguracoes:
    def desenhar(self, surface):
        surface.fill((35, 35, 50))
        title = BIG_FONT.render("Configurações", True, (255, 255, 255))
        surface.blit(title, (LARGURA // 2 - title.get_width() // 2, 80))
        info = FONT.render("Aqui colocarias campos editáveis...", True, (200, 200, 200))
        surface.blit(info, (100, 200))
