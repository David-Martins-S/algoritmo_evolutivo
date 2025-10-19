from telas.simulacao import Simulacao
from telas.menu_inicial import TelaInicial
from telas.configuracoes import TelaConfiguracoes

class GerenciadorTelas:
    def __init__(self):
        self.telas = {
            "menu": TelaInicial(self),
            "simulacao": Simulacao(self),
            "configuracoes": TelaConfiguracoes(self)
        }
        self.tela_atual = self.telas["simulacao"]

    def adicionar_tela(self, nome, tela):
        self.telas[nome] = tela

    def mudar_tela(self, nome):
        self.tela_atual = self.telas[nome]


    def desenhar(self, tela):
        if self.tela_atual:
            if hasattr(self.tela_atual, "atualizar"):
                self.tela_atual.atualizar()
            else:
                self.tela_atual.desenhar(tela)

    def eventos(self, event):
        if hasattr(self.tela_atual, "eventos"):
            self.tela_atual.eventos(event)