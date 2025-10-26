import random
from globais import (LARGURA, ALTURA,
                     MINIMO_VISAO, MAXIMO_VISAO,
                     MINIMO_VELOCIDADE, MAXIMO_VELOCIDADE,
                     VARIACAO_VISAO, VARIACAO_VELOCIDADE,
                     VARIACAO_COR)
from criatura import Criatura


def nova_geracao(geracao_finalizada):
    novas = []

    def cria_herdeiro(parent):
        """Cria um filho a partir de um objeto 'parent' aplicando mutações suaves."""
        # Visão mutada (int)
        nova_visao = int(parent.visao + random.randint(-VARIACAO_VISAO, VARIACAO_VISAO))
        # nova_visao = max(MINIMO_VISAO, min(MAXIMO_VISAO, nova_visao))

        # Velocidade mutada (float)
        nova_vel = parent.velocidade + random.uniform(-VARIACAO_VELOCIDADE, VARIACAO_VELOCIDADE)
        # nova_vel = max(MINIMO_VELOCIDADE, min(MAXIMO_VELOCIDADE, nova_vel))

        # Cor mutada (RGB tuple)
        parent_cor = getattr(parent, "cor", (0, 100, 255))
        nova_cor = tuple(
            max(0, min(255, int(channel + random.randint(-VARIACAO_COR, VARIACAO_COR))))
            for channel in parent_cor
        )

        # Geração do filho = geração do pai + 1 (assume que parent.geracao existe)
        parent_generation = getattr(parent, "geracao", 1)
        filho_geracao = parent_generation + 1

        # Cria o objeto - ajuste a assinatura se o seu __init__ for diferente
        filho = Criatura(random.uniform(0, LARGURA),
                         random.uniform(0, ALTURA),
                         nova_visao, nova_vel, nova_cor, filho_geracao)
        # Opcional: iniciar com 0 comida (ou 1 se regra pedir)
        filho.comida_comida = 0
        return filho

    def cria_pai_sem_mutacao(parent, inherit_generation_increment=False):
        """Cria uma nova instância representando o pai que sobrevive sem mutação.
           Se inherit_generation_increment=True, pode aumentar a geração do pai (opcional)."""
        parent_generation = getattr(parent, "geracao", 1)
        new_generation = parent_generation + 1 if inherit_generation_increment else parent_generation
        parent_idade = getattr(parent, "idade")
        nova_idade = parent_idade + 15

        p = Criatura(random.uniform(0, LARGURA),
                     random.uniform(0, ALTURA),
                     int(parent.visao),
                     float(parent.velocidade),
                     getattr(parent, "cor", (0, 100, 255)),
                     new_generation, nova_idade)
        # Preserva energia? normalmente resetamos energia para 100 na nova geração
        p.energia = getattr(parent, "energia", 100)
        p.comida_comida = 0
        return p

    for parent in geracao_finalizada:
        eaten = getattr(parent, "comida_comida", 0)

        if eaten == 0:
            # morre
            continue

        elif eaten == 1:
            # sobrevive — pai entra na próxima geração com os mesmos atributos (sem mutação)
            novas.append(cria_pai_sem_mutacao(parent))

        elif eaten == 2:
            # pai sobrevive (sem mutação) + um filho mutado
            novas.append(cria_pai_sem_mutacao(parent))
            novas.append(cria_herdeiro(parent))

        elif eaten == 3:
            # 50/50: pai começa com 1 comida OR filho começa com 1 comida
            if random.random() < 0.5:
                # pai com comida (inicia com 1), filho sem
                p = cria_pai_sem_mutacao(parent)
                p.comida_comida = 1
                novas.append(p)
                novas.append(cria_herdeiro(parent))
            else:
                # pai sem comida, filho com 1
                novas.append(cria_pai_sem_mutacao(parent))
                f = cria_herdeiro(parent)
                f.comida_comida = 1
                novas.append(f)

        else:  # eaten >= 4
            # pai e filho começam a próxima rodada com 1 comida cada
            p = cria_pai_sem_mutacao(parent)
            f = cria_herdeiro(parent)
            p.comida_comida = 1
            f.comida_comida = 1
            novas.append(p)
            novas.append(f)

    # fallback: se nada sobreviveu, repovoar com alguns indivíduos padrão
    if not novas:
        for _ in range(max(1, len(geracao_finalizada)//2)):
            novas.append(Criatura(random.uniform(0, LARGURA),
                                  random.uniform(0, ALTURA),
                                  random.randint(MINIMO_VISAO, MAXIMO_VISAO),
                                  random.uniform(MINIMO_VELOCIDADE, MAXIMO_VELOCIDADE),
                                  (0, 100, 255),
                                  1))
    return novas

