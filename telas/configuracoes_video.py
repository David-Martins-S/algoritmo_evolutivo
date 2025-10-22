import pygame

import globais
from globais import LARGURA, ALTURA
from gerenciador_estados import GerenciadorDeEstado
from estados_menu import MenuState

# estado = GerenciadorDeEstado()
#
# pygame.init()
# FONT = pygame.font.SysFont("Arial", 24)
#
# class CampoTexto:
#     def __init__(self, x, y, largura, altura, texto_inicial=""):
#         self.rect = pygame.Rect(x, y, largura, altura)
#         self.texto = str(texto_inicial)
#         self.ativo = False
#
#     def handle_event(self, evento):
#         if evento.type == pygame.MOUSEBUTTONDOWN:
#             # Ativa ou desativa o campo
#             self.ativo = self.rect.collidepoint(evento.pos)
#         elif evento.type == pygame.KEYDOWN and self.ativo:
#             if evento.key == pygame.K_RETURN:
#                 self.ativo = False
#             elif evento.key == pygame.K_BACKSPACE:
#                 self.texto = self.texto[:-1]
#             elif evento.unicode.isdigit():
#                 self.texto += evento.unicode
#
#     def draw(self, tela):
#         cor = (255, 255, 255) if self.ativo else (200, 200, 200)
#         pygame.draw.rect(tela, (50, 50, 50), self.rect)
#         pygame.draw.rect(tela, cor, self.rect, 2)
#         txt_surf = FONT.render(self.texto, True, cor)
#         tela.blit(txt_surf, (self.rect.x + 8, self.rect.y + 8))
#
#     def get_valor(self):
#         try:
#             return int(self.texto)
#         except ValueError:
#             return None
#
#
# class Botao:
#     def __init__(self, x, y, w, h, texto):
#         self.rect = pygame.Rect(x, y, w, h)
#         self.texto = texto
#         self.clicked = False
#
#     def draw(self, tela):
#         cor = (100, 100, 100)
#         pos = pygame.mouse.get_pos()
#         if self.rect.collidepoint(pos):
#             cor = (150, 150, 150)
#         pygame.draw.rect(tela, cor, self.rect, border_radius=6)
#         txt_surf = FONT.render(self.texto, True, (0, 0, 0))
#         tela.blit(txt_surf, (self.rect.centerx - txt_surf.get_width()//2, self.rect.centery - txt_surf.get_height()//2))
#         mouse_pressed = pygame.mouse.get_pressed()[0]
#         if mouse_pressed and not self.clicked and self.rect.collidepoint(pos):
#             self.clicked = True
#         elif not mouse_pressed and self.clicked:
#             self.clicked = False
#             if self.rect.collidepoint(pos):
#                 return True
#         return False
#
#
# class TelaConfiguracoesVideo:
#     def __init__(self):
#         self.campo_largura = CampoTexto(500, 250, 150, 40, str(LARGURA))
#         self.campo_altura = CampoTexto(500, 320, 150, 40, str(ALTURA))
#         self.botao_aplicar = Botao(400, 400, 120, 50, "Aplicar")
#         self.botao_voltar = Botao(560, 400, 120, 50, "Voltar")
#
#     def handle_event(self, evento):
#         self.campo_largura.handle_event(evento)
#         self.campo_altura.handle_event(evento)
#
#     def draw(self, tela):
#         tela.fill((40, 60, 70))
#         titulo = FONT.render("Configurações de Vídeo", True, (255,255,255))
#         tela.blit(titulo, (400, 180))
#
#         # Rótulos
#         lbl_largura = FONT.render("Largura:", True, (255,255,255))
#         lbl_altura = FONT.render("Altura:", True, (255,255,255))
#         tela.blit(lbl_largura, (380, 255))
#         tela.blit(lbl_altura, (395, 325))
#
#         # Campos
#         self.campo_largura.draw(tela)
#         self.campo_altura.draw(tela)
#
#         # Botões
#         if self.botao_aplicar.draw(tela):
#             self.aplicar_configuracoes()
#         if self.botao_voltar.draw(tela):
#             estado.mudar_menu(MenuState.OPTIONS)
#
#     def aplicar_configuracoes(self):
#         global LARGURA, ALTURA
#         nova_largura = self.campo_largura.get_valor()
#         nova_altura = self.campo_altura.get_valor()
#         if nova_largura and nova_altura:
#             print(f"[CONFIG VÍDEO] Alterando resolução para {nova_largura}x{nova_altura}")
#             globais.LARGURA = nova_largura
#             globais.ALTURA = nova_altura
#             pygame.display.set_mode((nova_largura, nova_altura))

import pygame
# from config import LARGURA_TELA, ALTURA_TELA

class TelaConfiguracoesVideo:
    def __init__(self):
        self.fonte = pygame.font.Font(None, 40)

        self.largura_texto = str(globais.LARGURA)
        self.altura_texto = str(globais.ALTURA)

        # Define áreas clicáveis para os campos de texto
        self.campo_largura = pygame.Rect(300, 200, 200, 50)
        self.campo_altura = pygame.Rect(300, 300, 200, 50)

        self.ativo_largura = False
        self.ativo_altura = False

        self.cor_inativa = pygame.Color("gray70")
        self.cor_ativa = pygame.Color("white")

        self.botao_salvar = pygame.Rect(300, 400, 200, 60)

    def desenhar(self, tela):
        tela.fill((30, 30, 30))

        titulo = self.fonte.render("Configurações de Vídeo", True, (255, 255, 0))
        tela.blit(titulo, (220, 100))

        # Desenha campos de largura e altura
        cor_largura = self.cor_ativa if self.ativo_largura else self.cor_inativa
        cor_altura = self.cor_ativa if self.ativo_altura else self.cor_inativa

        pygame.draw.rect(tela, cor_largura, self.campo_largura)
        pygame.draw.rect(tela, cor_altura, self.campo_altura)

        txt_largura = self.fonte.render(self.largura_texto, True, (0, 0, 0))
        txt_altura = self.fonte.render(self.altura_texto, True, (0, 0, 0))
        tela.blit(txt_largura, (self.campo_largura.x + 10, self.campo_largura.y + 10))
        tela.blit(txt_altura, (self.campo_altura.x + 10, self.campo_altura.y + 10))

        # Labels
        tela.blit(self.fonte.render("Largura:", True, (255, 255, 255)), (150, 210))
        tela.blit(self.fonte.render("Altura:", True, (255, 255, 255)), (150, 310))

        # Botão salvar
        pygame.draw.rect(tela, (50, 200, 50), self.botao_salvar)
        tela.blit(self.fonte.render("Salvar", True, (255, 255, 255)), (355, 415))

    def handle_event(self, eventos):

        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                # Detecta qual campo foi clicado
                if self.campo_largura.collidepoint(evento.pos):
                    self.ativo_largura = True
                    self.ativo_altura = False
                elif self.campo_altura.collidepoint(evento.pos):
                    self.ativo_altura = True
                    self.ativo_largura = False
                elif self.botao_salvar.collidepoint(evento.pos):
                    try:
                        nova_largura = int(self.largura_texto)
                        nova_altura = int(self.altura_texto)
                        globais.LARGURA = nova_largura
                        globais.ALTURA = nova_altura
                        print(f"Resolução alterada para: {globais.LARGURA}x{globais.ALTURA}")
                    except ValueError:
                        print("Valores inválidos! Digite apenas números.")
                else:
                    # Clicou fora, desativa os campos
                    self.ativo_largura = False
                    self.ativo_altura = False

            elif evento.type == pygame.KEYDOWN:
                if self.ativo_largura:
                    if evento.key == pygame.K_BACKSPACE:
                        self.largura_texto = self.largura_texto[:-1]
                    elif evento.unicode.isdigit():
                        self.largura_texto += evento.unicode
                elif self.ativo_altura:
                    if evento.key == pygame.K_BACKSPACE:
                        self.altura_texto = self.altura_texto[:-1]
                    elif evento.unicode.isdigit():
                        self.altura_texto += evento.unicode

