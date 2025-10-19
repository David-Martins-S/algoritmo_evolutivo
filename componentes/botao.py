import pygame

class Botao:
    def __init__(self, texto, x, y, largura, altura, cor_normal, cor_hover, acao=None):
        self.texto = texto
        self.rect = pygame.Rect(x, y, largura, altura)
        self.cor_normal = cor_normal
        self.cor_hover = cor_hover
        self.acao = acao
        self.fonte = pygame.font.SysFont(None, 40)

    def desenhar(self, tela):
        mouse = pygame.mouse.get_pos()
        clique = pygame.mouse.get_pressed()
        cor = self.cor_hover if self.rect.collidepoint(mouse) else self.cor_normal

        pygame.draw.rect(tela, cor, self.rect, border_radius=10)
        texto_render = self.fonte.render(self.texto, True, (255, 255, 255))
        tela.blit(texto_render, texto_render.get_rect(center=self.rect.center))

        if self.rect.collidepoint(mouse) and clique[0]:
            if self.acao:
                self.acao()

