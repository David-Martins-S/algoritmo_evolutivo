import pygame
import sys
from estados_menu import MenuState
from gerenciador_estados import GerenciadorDeEstado
from button import Button
from telas.simulacao import Simulacao
from telas.configuracoes_video import TelaConfiguracoesVideo

from globais import LARGURA, ALTURA, FPS
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

    # cria botões
    def make_btn(x, y, txt):

       return Button(x, y, text=txt, w=220, h=60)

    resume_button = make_btn(LARGURA/2-110, ALTURA/3, "PLAY")
    options_button = make_btn(LARGURA/2-110, ALTURA/2, "OPÇÕES")
    quit_button = make_btn(LARGURA/2-110, ((ALTURA/3)*2), "SAIR")
    video_button = make_btn(LARGURA/2-110, ((ALTURA/6)*2), "VIDEO")
    audio_button = make_btn(LARGURA/2-110, ((ALTURA/6)*3), "AUDIO")
    keys_button = make_btn(LARGURA/2-110, ((ALTURA/6)*4), "TECLAS")
    back_button = make_btn(LARGURA/2-110, ((ALTURA/6)*5), "VOLTAR")

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
                # title = BIG_FONT.render("MENU PRINCIPAL", True, (255, 255, 255))
                sub = BIG_FONT.render("OPÇÕES", True, (255, 255, 255))
                screen.blit(sub, (LARGURA/2-80, 80))

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
