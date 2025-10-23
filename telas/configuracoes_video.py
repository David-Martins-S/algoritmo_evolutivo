import globais
import pygame


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
        tela.fill((52, 78, 91))

        BIG_FONT = pygame.font.SysFont("Arial", 48)

        titulo = BIG_FONT.render("CONFIGURAÇÕES DE VÍDEO", True, (255, 255, 255))

        # titulo = self.fonte.render("Configurações de Vídeo", True, (255, 255, 0))
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

    def handle_event(self, evento):

        if evento.type == pygame.MOUSEBUTTONDOWN:
            # Detecta qual campo foi clicado
            if self.campo_largura.collidepoint(evento.pos):
                self.ativo_largura = True
                self.ativo_altura = False
                print("Largura clicada")
            elif self.campo_altura.collidepoint(evento.pos):
                self.ativo_altura = True
                self.ativo_largura = False
                print("Altura clicada")
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
