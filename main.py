import pygame
import sys
from estados_menu import MenuState
from gerenciador_estados import GerenciadorDeEstado
from button import Button
from telas.simulacao import Simulacao
from telas.configuracoes_video import TelaConfiguracoesVideo

from globais import *
from telas.configuracoes import TelaConfiguracoes

pygame.init()
FONT = pygame.font.SysFont("Arial", 20)
BIG_FONT = pygame.font.SysFont("Arial", 48)

# instância global
estado = GerenciadorDeEstado()
# por padrão, começamos em simulação (se preferir menu, set True)
estado.pausar_jogo()


def main():
    screen = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Simulação Evolutiva - Arquivão")
    clock = pygame.time.Clock()

    # tenta carregar imagens de botão; se falhar, usa botões textuais
    def load_img(path):
        try:
            return pygame.image.load(path).convert_alpha()
        except Exception as e:
            print(f"[AVISO] Falha ao carregar {path}: {e}")
            return None

    resume_img = load_img("images/button_resume.png")
    options_img = load_img("images/button_options.png")
    quit_img = load_img("images/button_quit.png")
    video_img = load_img("images/button_video.png")
    audio_img = load_img("images/button_audio.png")
    keys_img = load_img("images/button_keys.png")
    back_img = load_img("images/button_back.png")

    # cria botões (se a imagem não existir, cria botão textual)
    def make_btn(x, y, img, txt):
        if img:
            return Button(x, y, img, 1)
        else:
            return Button(x, y, text=txt, w=220, h=60)

    resume_button = make_btn(LARGURA/2-191/2, ALTURA/3, resume_img, "RESUMIR")
    options_button = make_btn(LARGURA/2-205/2, ALTURA/2, options_img, "OPÇÕES")
    quit_button = make_btn(LARGURA/2-128/2, ((ALTURA/3)*2), quit_img, "SAIR")
    video_button = make_btn(LARGURA/2-347/2, ((ALTURA/6)*2), video_img, "VIDEO")
    audio_button = make_btn(LARGURA/2-349/2, ((ALTURA/6)*3), audio_img, "AUDIO")
    keys_button = make_btn(LARGURA/2-308/2, ((ALTURA/6)*4), keys_img, "TECLAS")
    back_button = make_btn(LARGURA/2-135/2, ((ALTURA/6)*5), back_img, "VOLTAR")

    simulacao = Simulacao()

    # Tela de configurações simplificada (apenas desenho)
    tela_configuracoes = TelaConfiguracoes()
    tela_video = TelaConfiguracoesVideo()

    run = True
    while run:
        # processa eventos uma vez por frame
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                run = False
            # envia evento para simulação quando não estiver pausado
            if not estado.esta_pausado():
                simulacao.handle_event(evento)
            # caso esteja pausado, deixamos menus reagirem via botões (click detectado no draw)
            # também podemos tratar atalhos globais aqui
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    print("[Main] espaço pressionado -> pausar/reiniciar")
                    estado.retomar_jogo() if estado.esta_pausado() else estado.pausar_jogo()
                if evento.key == pygame.K_ESCAPE:
                    print("[Main] ESC pressionado -> pausar")
                    estado.pausar_jogo()

        # DRAW & UPDATE
        if not estado.esta_pausado():
            # simulação atualiza & desenha
            simulacao.update()
            simulacao.draw(screen)
        else:
            # menu
            screen.fill((52, 78, 91))
            if estado.menu_state == MenuState.MAIN:
                title = BIG_FONT.render("MENU PRINCIPAL", True, (255, 255, 255))
                screen.blit(title, (LARGURA//2 - title.get_width()//2, 60))

                if resume_button.draw(screen):
                    print("[Main] Resume pressionado")
                    estado.retomar_jogo()

                if options_button.draw(screen):
                    estado.mudar_menu(MenuState.OPTIONS)

                if quit_button.draw(screen):
                    run = False

            elif estado.menu_state == MenuState.OPTIONS:
                sub = FONT.render("OPÇÕES", True, (255, 255, 255))
                screen.blit(sub, (100, 80))

                if video_button.draw(screen):
                    estado.mudar_menu(MenuState.VIDEO_SETTINGS)
                if audio_button.draw(screen):
                    estado.mudar_menu(MenuState.AUDIO_SETTINGS)
                if keys_button.draw(screen):
                    estado.mudar_menu(MenuState.KEYS_SETTINGS)
                if back_button.draw(screen):
                    estado.mudar_menu(MenuState.MAIN)

            elif estado.menu_state == MenuState.VIDEO_SETTINGS:
                # tela_configuracoes.desenhar(screen)
                for evento in pygame.event.get(pygame.KEYDOWN):
                    tela_video.handle_event(evento)
                tela_video.desenhar(screen)
                if back_button.draw(screen):
                    estado.mudar_menu(MenuState.OPTIONS)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
