import pygame
import globais
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

        self.botao_salvar = pygame.Rect(globais.LARGURA - 260, globais.ALTURA - 120, 200, 50)
        self.botao_voltar = pygame.Rect(globais.LARGURA - 260, globais.ALTURA - 60, 200, 50)

    def _criar_campos(self):
        y = 80
        espacamento = 55
        for chave, valor in vars(globais).items():
            if chave.isupper() and not chave.startswith("__"):
                # Campo numérico / texto
                if isinstance(valor, (int, float, str)):
                    campo = CampoTexto(400, y, 220, 35, valor, chave)
                    self.campos.append((chave, campo))
                    y += espacamento
                # Campo booleano → checkbox
                elif isinstance(valor, bool):
                    checkbox = {
                        "chave": chave,
                        "rect": pygame.Rect(400, y, 25, 25),
                        "valor": valor
                    }
                    self.campos.append(("checkbox", checkbox))
                    y += espacamento
        self.altura_total = y

    def desenhar(self, tela):
        # fundo suave
        tela.fill((30, 45, 55))
        pygame.draw.rect(tela, (25, 35, 45), (0, 0, globais.LARGURA, globais.ALTURA), 0)

        offset_y = self.scroll_y

        y = 80
        for chave, campo in self.campos:
            label = self.font.render(chave, True, (255, 255, 255))
            tela.blit(label, (60, y + offset_y))
            campo.desenhar(tela, offset_y)
            y += 55

        y = 80
        for chave, campo in self.campos:
            if chave == "checkbox":
                label = self.font.render(campo["chave"], True, (255, 255, 255))
                tela.blit(label, (60, y + offset_y))
                rect = campo["rect"].move(0, offset_y)
                pygame.draw.rect(tela, (200, 200, 200), rect, 2, border_radius=4)
                if campo["valor"]:
                    pygame.draw.line(tela, (0, 255, 0), rect.topleft, rect.bottomright, 3)
                    pygame.draw.line(tela, (0, 255, 0), rect.topright, rect.bottomleft, 3)
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
                globais.ALTURA - self.altura_total - 100, TelaConfiguracoesSimulacao.scroll_y
            )

        for _, campo in self.campos:
            campo.evento(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.botao_salvar.collidepoint(event.pos):
                self.salvar_alteracoes()
            elif self.botao_voltar.collidepoint(event.pos):
                estado.mudar_menu(MenuState.MAIN)
            for tipo, campo in self.campos:
                if tipo == "checkbox":
                    rect = campo["rect"].move(0, self.scroll_y)
                    if rect.collidepoint(event.pos):
                        campo["valor"] = not campo["valor"]

    def salvar_alteracoes(self):
        novos_valores = {}
        for tipo, campo in self.campos:
            if tipo == "checkbox":
                novos_valores[campo["chave"]] = campo["valor"]
            else:
                novos_valores[campo.chave] = campo.get_valor()

        for chave, valor in novos_valores.items():
            setattr(globais, chave, valor)

        globais.salvar_config(novos_valores)
        print("Configurações salvas e aplicadas com sucesso!")

