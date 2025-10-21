from simulacao import Simulacao
from globais import LARGURA, ALTURA
from telas.configuracoes import TelaConfiguracoes
from estados_menu import MenuState
from gerenciador_estados import GerenciadorDeEstado

import pygame
import button

pygame.init()

# create game window
screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Menu Principal")

# game variables
game_paused = True
menu_state = MenuState.MAIN

# define fonts
font = pygame.font.SysFont("arialblack", 40)

# define colours
TEXT_COL = (255, 255, 255)

# load button images
resume_img = pygame.image.load("images/button_resume.png").convert_alpha()
options_img = pygame.image.load("images/button_options.png").convert_alpha()
quit_img = pygame.image.load("images/button_quit.png").convert_alpha()
video_img = pygame.image.load('images/button_video.png').convert_alpha()
audio_img = pygame.image.load('images/button_audio.png').convert_alpha()
keys_img = pygame.image.load('images/button_keys.png').convert_alpha()
back_img = pygame.image.load('images/button_back.png').convert_alpha()

# create button instances
resume_button = button.Button(LARGURA/2-191/2, ALTURA/3, resume_img, 1)
options_button = button.Button(LARGURA/2-205/2, ALTURA/2, options_img, 1)
quit_button = button.Button(LARGURA/2-128/2, ((ALTURA/3)*2), quit_img, 1)
video_button = button.Button(LARGURA/2-347/2, ((ALTURA/6)*2), video_img, 1)
audio_button = button.Button(LARGURA/2-349/2, ((ALTURA/6)*3), audio_img, 1)
keys_button = button.Button(LARGURA/2-308/2, ((ALTURA/6)*4), keys_img, 1)
back_button = button.Button(LARGURA/2-135/2, ((ALTURA/6)*5), back_img, 1)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


estado = GerenciadorDeEstado()
simulacao = Simulacao()
tela_configuracoes = TelaConfiguracoes()

# game loop
run = True
while run:

    screen.fill((52, 78, 91))

    # Gerenciador de eventos
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_paused = True
        if event.type == pygame.QUIT:
            run = False

    if estado.esta_pausado():
        if estado.menu_state == MenuState.MAIN:
            if resume_button.draw(screen):
                estado.retomar_jogo()
            if options_button.draw(screen):
                estado.mudar_menu(MenuState.OPTIONS)
            if quit_button.draw(screen):
                run = False
        elif estado.menu_state == MenuState.OPTIONS:
            if video_button.draw(screen):
                estado.mudar_menu(MenuState.VIDEO_SETTINGS)
            if audio_button.draw(screen):
                estado.mudar_menu(MenuState.AUDIO_SETTINGS)
            if keys_button.draw(screen):
                estado.mudar_menu(MenuState.KEYS_SETTINGS)
            if back_button.draw(screen):
                estado.mudar_menu(MenuState.MAIN)
        elif estado.menu_state == MenuState.VIDEO_SETTINGS:
            tela_configuracoes.desenhar(screen)
    else:
        simulacao.rodar()

    pygame.display.update()

pygame.quit()
