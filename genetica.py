import random
from criatura import Criatura
from globais import *

def nova_geracao(geracao_finalizada):
    novas = []
    for c in geracao_finalizada:
        eaten = c.comida_comida
        if eaten == 0:
            continue  # morre

        # cria individuo herdado (com mutação leve)
        def cria_herdeiro(herda_visao, herda_vel, herda_cor):
            nova_visao = herda_visao + random.randint(-VARIACAO_VISAO, VARIACAO_VISAO)
            nova_vel = herda_vel + random.uniform(-VARIACAO_VELOCIDADE, VARIACAO_VELOCIDADE)
            nova_cor = tuple(
                max(0, min(255, c + random.randint(-VARIACAO_COR, VARIACAO_COR)))
                for c in herda_cor
                )
            return Criatura(random.uniform(0, LARGURA), random.uniform(0, ALTURA), nova_visao, nova_vel, nova_cor)

        def pai_sobrevive(visao, velocidade, cor):
            p = Criatura(random.uniform(0, LARGURA), random.uniform(0, ALTURA), visao, velocidade, cor)
            return p

        if eaten == 1:
            # sobrevive (pai)
            novas.append(pai_sobrevive(c.visao, c.velocidade, c.cor))
        elif eaten == 2:
            # sobrevive + 1 filho
            novas.append(pai_sobrevive(c.visao, c.velocidade, c.cor))
            novas.append(cria_herdeiro(c.visao, c.velocidade, c.cor))
        elif eaten == 3:
            # 50/50: pai começa com 1 comida (simulate by setting comida_comida) OR filho começa com 1 comida
            if random.random() < 0.5:
                # pai com comida, filho sem
                p = pai_sobrevive(c.visao, c.velocidade, c.cor)
                p.comida_comida = 1
                novas.append(p)
                novas.append(cria_herdeiro(c.visao, c.velocidade, c.cor))
            else:
                # filho com comida, pai sem
                novas.append(pai_sobrevive(c.visao, c.velocidade, c.cor))
                f = cria_herdeiro(c.visao, c.velocidade, c.cor)
                f.comida_comida = 1
                novas.append(f)
        else:  # eaten >= 4
            # pai e filho começam com comida
            p = pai_sobrevive(c.visao, c.velocidade, c.cor)
            f = cria_herdeiro(c.visao, c.velocidade, c.cor)
            p.comida_comida = 1
            f.comida_comida = 1
            novas.append(p)
            novas.append(f)



    # se não sobrou ninguém, repovoa com população inicial
    if not novas:
        novas = [Criatura(random.uniform(0, LARGURA), random.uniform(0, ALTURA))
                 for _ in range(NUM_CRIATURAS_INICIAL)]

    # resetar contadores e aplicar nova população
    for ind in novas:
        ind.comida_comida = getattr(ind, 'comida_comida', 0)
        ind.energia = 100.0

    return novas
