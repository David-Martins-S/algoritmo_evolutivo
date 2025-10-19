# import random
# from comida import Comida
#
# class Ambiente:
#     def __init__(self, largura, altura, num_comidas):
#         self.largura = largura
#         self.altura = altura
#         self.num_comidas = num_comidas
#         self.comidas = self.gerar_comidas()
#
#     def gerar_comidas(self):
#         return [
#             Comida(random.uniform(0, self.largura), random.uniform(0, self.altura))
#             for _ in range(self.num_comidas)
#         ]
#
#     def resetar(self):
#         self.comidas = self.gerar_comidas()
