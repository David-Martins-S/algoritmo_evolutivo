# import pygame
#
# from estados_menu import MenuState
#
# class GerenciadorDeEstado:
#     def __init__(self):
#         self.menu_state = MenuState.MAIN
#         self.game_paused = True
#
#     def mudar_menu(self, novo_estado: MenuState):
#         print(f"[GERENCIADOR] {self.menu_state.name} → {novo_estado.name}")
#         self.menu_state = novo_estado
#
#         pygame.event.clear()
#         pygame.time.wait(100)
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
#
#
# # cria a instância única aqui mesmo
# estado_global = GerenciadorDeEstado()

import pygame

from estados_menu import MenuState

class GerenciadorDeEstado:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia.menu_state = MenuState.MAIN
            cls._instancia._pausado = True
        return cls._instancia

    def mudar_menu(self, novo_estado: MenuState):
        # limpa eventos residuais (evita cliques fantasmas)
        pygame.event.clear()
        print(f"[GERENCIADOR] {self.menu_state.name} -> {novo_estado.name}")
        self.menu_state = novo_estado

    def pausar_jogo(self):
        self._pausado = True
        self.menu_state = MenuState.MAIN

    def retomar_jogo(self):
        self._pausado = False
        self.menu_state = MenuState.SIMULACAO

    def esta_pausado(self):
        return self._pausado



