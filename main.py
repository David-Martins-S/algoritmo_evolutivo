import pygame
# import numpy as np
import sys
from estados_menu import MenuState
from gerenciador_estados import GerenciadorDeEstado
from button import Button
from telas.simulacao import Simulacao
from telas.configuracoes_video import TelaConfiguracoesVideo

import globais

# from globals import LARGURA, ALTURA, FPS
from telas.configuracoes import TelaConfiguracoes
from telas.configuracoes_simulacao import TelaConfiguracoesSimulacao

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(16)
som_pop = pygame.mixer.Sound("assets/sounds/pop2.mp3")
som_vush = pygame.mixer.Sound("assets/sounds/vush.mp3")
som_pop.set_volume(0.3)  # volume de 0.0 a 1.0
som_vush.set_volume(0.5)  # volume de 0.0 a 1.0
FONT = pygame.font.SysFont("Segoe UI Emoji", 20)
BIG_FONT = pygame.font.SysFont("Segoe UI Emoji", 48)

# instância global
estado = GerenciadorDeEstado()
# por padrão, começamos em simulação (se preferir menu, set True)
estado.pausar_jogo()
tela_config_sim = TelaConfiguracoesSimulacao()


def main():
    screen = pygame.display.set_mode((globais.LARGURA, globais.ALTURA))
    pygame.display.set_caption("Simulação Evolutiva - Arquivão")
    clock = pygame.time.Clock()

    def load_img(path):
        try:
            return pygame.image.load(path).convert_alpha()
        except Exception as e:
            print(f"[AVISO] Falha ao carregar {path}: {e}")
            return None

    def make_btn(x, y, txt):
       return Button(x, y, text=txt, w=220, h=60)

    resume_button = make_btn(globais.LARGURA/2-110, globais.ALTURA/3, "INICIAR")
    options_button = make_btn(globais.LARGURA/2-110, globais.ALTURA/2, "OPÇÕES")
    quit_button = make_btn(globais.LARGURA/2-110, ((globais.ALTURA/3)*2), "SAIR")
    video_button = make_btn(globais.LARGURA/2-110, ((globais.ALTURA/6)*2), "VIDEO")
    param_button = make_btn(globais.LARGURA/2-110, ((globais.ALTURA/6)*3), "PARÂM. DA SIMULAÇÃO")
    keys_button = make_btn(globais.LARGURA/2-110, ((globais.ALTURA/6)*4), "TECLAS")
    back_button = make_btn(globais.LARGURA/2-110, ((globais.ALTURA/6)*5), "VOLTAR")

    simulacao = Simulacao()
    simulacao.som_pop = som_pop
    simulacao.som_vush = som_vush

    tela_video = TelaConfiguracoesVideo()

    run = True
    while run:
        # processa eventos uma vez por frame
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                run = False
            if not estado.esta_pausado():
                simulacao.handle_event(evento)
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    estado.retomar_jogo() if estado.esta_pausado() else estado.pausar_jogo()
                if evento.key == pygame.K_ESCAPE:
                    estado.pausar_jogo()
            if estado.menu_state == MenuState.VIDEO_SETTINGS:
                tela_video.handle_event(evento)
            if estado.menu_state == MenuState.SIMULATION_SETTINGS:
                tela_config_sim.eventos(evento)

        if not estado.esta_pausado():
            simulacao.update()
            simulacao.draw(screen)
        else:
            # menu
            screen.fill((52, 78, 91))
            if estado.menu_state == MenuState.MAIN:
                title = BIG_FONT.render("MENU PRINCIPAL", True, (255, 255, 255))
                screen.blit(title, (globais.LARGURA//2 - title.get_width()//2, 60))
                if resume_button.draw(screen):
                    estado.retomar_jogo()
                if options_button.draw(screen):
                    estado.mudar_menu(MenuState.OPTIONS)
                if quit_button.draw(screen):
                    run = False
            elif estado.menu_state == MenuState.OPTIONS:
                # title = BIG_FONT.render("MENU PRINCIPAL", True, (255, 255, 255))
                sub = BIG_FONT.render("OPÇÕES", True, (255, 255, 255))
                screen.blit(sub, (globais.LARGURA/2-80, 80))
                if video_button.draw(screen):
                    estado.mudar_menu(MenuState.VIDEO_SETTINGS)
                if param_button.draw(screen):
                    estado.mudar_menu(MenuState.SIMULATION_SETTINGS)
                if keys_button.draw(screen):
                    estado.mudar_menu(MenuState.KEYS_SETTINGS)
                if back_button.draw(screen):
                    estado.mudar_menu(MenuState.MAIN)
            elif estado.menu_state == MenuState.VIDEO_SETTINGS:
                tela_video.desenhar(screen)
                if back_button.draw(screen):
                    estado.mudar_menu(MenuState.OPTIONS)
            elif estado.menu_state == MenuState.SIMULATION_SETTINGS:
                tela_config_sim.desenhar(screen)

        pygame.display.flip()
        clock.tick(globais.FPS)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
