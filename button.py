import pygame

pygame.init()
FONT = pygame.font.SysFont("Arial", 20)


class Button:
    def __init__(self, x, y, image=None, scale=1, text=None, w=None, h=None):
        """
        image: Surface ou None.
        text: string para renderizar botão simples.
        w,h: largura/altura se usar botão de texto.
        """
        self.clicked = False
        self.image = None
        if image is not None:
            width = image.get_width()
            height = image.get_height()
            self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
            self.rect = self.image.get_rect(topleft=(int(x), int(y)))
        else:
            # botão textual
            self.rect = pygame.Rect(int(x), int(y), int(w or 150), int(h or 50))
            self.text = text
            self.bg = (70, 70, 70)
            self.hover = (100, 100, 100)
            self.txt_surf = FONT.render(self.text or "", True, (255,255,255))

    def draw(self, surface):
        """
        Retorna True somente quando o botão foi clicado (mouse down + release dentro do botão).
        Lógica baseada em mouse button up para evitar cliques fantasmas.
        """
        action = False
        pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        # se tem imagem, desenha imagem; senão desenha rect/texto
        if self.image:
            surface.blit(self.image, (self.rect.x, self.rect.y))
        else:
            cor = self.hover if self.rect.collidepoint(pos) else self.bg
            pygame.draw.rect(surface, cor, self.rect, border_radius=6)
            txt_rect = self.txt_surf.get_rect(center=self.rect.center)
            surface.blit(self.txt_surf, txt_rect)

        # clique: detecta press -> marcar clicked; quando soltar dentro -> action True
        if self.rect.collidepoint(pos):
            if mouse_pressed and not self.clicked:
                # mouse down dentro do botão
                self.clicked = True
            elif not mouse_pressed and self.clicked:
                # mouse foi solto; se estava marcado, considera como clique
                action = True
                self.clicked = False
        else:
            # se sair da área e soltar, reseta
            if not mouse_pressed:
                self.clicked = False

        return action
