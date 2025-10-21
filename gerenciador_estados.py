# import pygame
#
# from estados_menu import MenuState
#
#
#
#
# class GerenciadorDeEstado:
#     def __init__(self):
#         # Estado inicial do menu
#         self.menu_state = MenuState.MAIN
#         # Você pode adicionar outros estados no futuro (ex: jogo pausado, fase atual etc)
#         self.game_paused = True
#
#     def mudar_menu(self, novo_estado: MenuState):
#         """Atualiza o estado atual do menu."""
#         print(f"[GERENCIADOR] Mudando menu de {self.menu_state.value} para {novo_estado.value}")
#         self.menu_state = novo_estado
#         pygame.event.clear()  # limpa eventos pendentes
#         pygame.time.wait(100)  # pausa curta para evitar clique remanescente
#
#     def pausar_jogo(self):
#         """Define o estado de pausa."""
#         self.game_paused = True
#
#     def retomar_jogo(self):
#         """Retoma o jogo."""
#         self.game_paused = False
#
#     def esta_pausado(self):
#         """Retorna se o jogo está pausado."""
#         return self.game_paused
import pygame

from estados_menu import MenuState

class GerenciadorDeEstado:
    def __init__(self):
        self.menu_state = MenuState.MAIN
        self.game_paused = True

    def mudar_menu(self, novo_estado: MenuState):
        print(f"[GERENCIADOR] {self.menu_state.name} → {novo_estado.name}")
        self.menu_state = novo_estado

        pygame.event.clear()
        pygame.time.wait(100)

    def pausar_jogo(self):
        """Define o estado de pausa."""
        self.game_paused = True

    def retomar_jogo(self):
        """Retoma o jogo."""
        self.game_paused = False

    def esta_pausado(self):
        """Retorna se o jogo está pausado."""
        return self.game_paused


# cria a instância única aqui mesmo
estado_global = GerenciadorDeEstado()



