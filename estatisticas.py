import pygame

FONT = pygame.font.Font(None, 20)


class Estatisticas:
    def __init__(self, media_visao=None, media_vel=None, media_autoexploracao=None,
                 media_risco=None, media_altruismo=None, comida_doada=None, maior_geracao=None,
                 total_filhos_geracao=None, total_machos=None, total_femeas=None,
                 geracao_atual=None, populacao=None, detectaram_parceiros=None):
        self.media_visao = media_visao if media_visao is not None else 0
        self.media_vel = media_vel if media_vel is not None else 0
        self.media_autoexploracao = media_autoexploracao if media_autoexploracao is not None else 0
        self.media_risco = media_risco if media_risco is not None else 0
        self.media_altruismo = media_altruismo if media_altruismo is not None else 0
        self.comida_doada = comida_doada if comida_doada is not None else 0
        self.maior_geracao = maior_geracao if maior_geracao is not None else 0
        self.total_filhos_geracao = total_filhos_geracao if total_filhos_geracao is not None else 0
        self.total_machos = total_machos if total_machos is not None else 0
        self.total_femeas = total_femeas if total_femeas is not None else 0
        self.geracao_atual = geracao_atual if geracao_atual is not None else 0
        self.populacao = populacao if populacao is not None else 0
        self.detectaram_parceiros = detectaram_parceiros if detectaram_parceiros is not None else 0

    def desenhar_estatisticas(self, surface):
        texto = (
            f"Geração: {self.geracao_atual} | "
            f"População: {self.populacao} "
            f"(M: {self.total_machos} / F: {self.total_femeas}) | "
            f"Visão: {self.media_visao:.1f} | "
            f"Vel: {self.media_vel:.2f} | "
            f"Filhos: {self.total_filhos_geracao} | "
            f"Risco médio: {self.media_risco:.2f} | "
            f"Média altruismo: {self.media_altruismo:.2f} | "
            f"Comida doada: {self.comida_doada}"
        )

        surf = FONT.render(texto, True, (255, 255, 255))
        surface.blit(surf, (10, 10))
