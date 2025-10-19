from simulacao import Simulacao
from globais import LARGURA, ALTURA
#
# # --- Execução principal ---
# if __name__ == "__main__":
#     simulacao = Simulacao()
#     simulacao.rodar()

import pygame
import button

def Menu_Inicial():
    def __init__(self):
        pygame.init()

        # create game window
        screen = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("Main Menu")

        # game variables
        game_paused = True
        menu_state = "main"

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
        resume_button = button.Button(304, 125, resume_img, 1)
        options_button = button.Button(297, 250, options_img, 1)
        quit_button = button.Button(336, 375, quit_img, 1)
        video_button = button.Button(226, 75, video_img, 1)
        audio_button = button.Button(225, 200, audio_img, 1)
        keys_button = button.Button(246, 325, keys_img, 1)
        back_button = button.Button(332, 450, back_img, 1)

        def draw_text(text, font, text_col, x, y):
            img = font.render(text, True, text_col)
            screen.blit(img, (x, y))

    def rodar(self):

        # game loop
        run = True
        while run:

            self.screen.fill((52, 78, 91))

            # check if game is paused
            if game_paused == True:
                # check menu state
                if menu_state == "main":
                    # draw pause screen buttons
                    if self.resume_button.draw(self.screen):
                        game_paused = False
                    if self.options_button.draw(self.screen):
                        menu_state = "options"
                    if self.quit_button.draw(self.screen):
                        run = False
                # check if the options menu is open
                if menu_state == "options":
                    # draw the different options buttons
                    if self.video_button.draw(self.screen):
                        print("Video Settings")
                    if self.audio_button.draw(self.screen):
                        print("Audio Settings")
                    if self.keys_button.draw(self.screen):
                        print("Change Key Bindings")
                    if self.back_button.draw(self.screen):
                        menu_state = "main"
            else:
                # RODA O JOGO
                simulacao = Simulacao()
                simulacao.rodar()

            # event handler
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_paused = True
                if event.type == pygame.QUIT:
                    run = False

            pygame.display.update()

        pygame.quit()