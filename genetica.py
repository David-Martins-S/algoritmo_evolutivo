import random
from globais import (LARGURA, ALTURA,
                     MINIMO_VISAO, MAXIMO_VISAO,
                     MINIMO_VELOCIDADE, MAXIMO_VELOCIDADE,
                     VARIACAO_VISAO, VARIACAO_VELOCIDADE
                     )
from criatura import Criatura


def nova_geracao(geracao_finalizada, geracao_atual):
    novas = []

    def cria_herdeiro(parent):
        """Cria um filho a partir de um objeto 'parent' aplicando mutações suaves."""
        nova_visao = int(parent.visao + random.randint(-VARIACAO_VISAO, VARIACAO_VISAO))
        nova_vel = parent.velocidade + random.uniform(-VARIACAO_VELOCIDADE, VARIACAO_VELOCIDADE)
        parent_generation = getattr(parent, "geracao", 1)
        filho_geracao = geracao_atual + 1

        # Cria o objeto
        filho = Criatura(random.uniform(0, LARGURA),
                         random.uniform(0, ALTURA),
                         nova_visao, nova_vel, None, filho_geracao)

        filho.autoexploracao = max(0, min(1, parent.autoexploracao + random.uniform(-0.1, 0.1)))

        # # Herança e mutação dos pesos comportamentais
        # if hasattr(parent, "pesos"):
        #     filho.pesos = {
        #         k: max(0.0, v + random.uniform(-0.05, 0.05))
        #         for k, v in parent.pesos.items()
        #     }
        # else:
        #     # fallback (caso alguma criatura antiga não tenha pesos)
        #     filho.pesos = {"ir_para_comida": 1.0, "aleatoriedade": 0.2}

        return filho

    def cria_pai_sem_mutacao(parent):
        """Cria uma nova instância representando o pai que sobrevive sem mutação."""
        parent_generation = getattr(parent, "geracao", 1)
        new_generation = parent_generation
        parent_idade = getattr(parent, "idade")
        nova_idade = parent_idade + 15
        sexo = getattr(parent, "sexo")

        p = Criatura(random.uniform(0, LARGURA),
                     random.uniform(0, ALTURA),
                     int(parent.visao),
                     float(parent.velocidade),
                     getattr(parent, "cor", (0, 100, 255)),
                     new_generation, nova_idade, sexo)
        # Preserva energia? normalmente resetamos energia para 100 na nova geração
        p.energia = getattr(parent, "energia", 100)
        comida_anterior = getattr(parent, "comida_comida", 1)
        p.comida_comida = 1 if comida_anterior > 1 else 0
        return p

    for parent in geracao_finalizada:
        eaten = getattr(parent, "comida_comida", 0)
        detectou = getattr(parent, "detectou_parceiro", False)

        # Apenas fêmeas podem gerar filhos, e só se detectaram um parceiro
        if parent.sexo == 'F':
            if eaten == 0:
                # morre
                continue

            elif eaten == 1:
                # sobrevive, mas não gera filhos
                novas.append(cria_pai_sem_mutacao(parent))

            elif eaten >= 2 and detectou:
                # sobrevive e gera até 3 filhos (dependendo da comida)

                num_filhos = min(eaten - 1, 3)  # 1 comida = 0 filhos, 2 = 1, 3 = 2, 4+ = 3
                for _ in range(num_filhos):
                    f = cria_herdeiro(parent)
                    f.comida_comida = 1  # cada filho nasce "alimentado"
                    novas.append(f)

                parent.comida_comida = parent.comida_comida - num_filhos
                novas.append(cria_pai_sem_mutacao(parent))

            else:
                # não detectou parceiro, apenas sobrevive
                novas.append(cria_pai_sem_mutacao(parent))

        else:
            # Machos apenas sobrevivem se comeram ao menos 1 comida
            if eaten >= 1:
                novas.append(cria_pai_sem_mutacao(parent))

    # fallback: se nada sobreviveu, repovoar com alguns indivíduos padrão
    if not novas:
        for _ in range(max(1, len(geracao_finalizada)//2)):
            novas.append(Criatura(random.uniform(0, LARGURA),
                                  random.uniform(0, ALTURA),
                                  random.randint(MINIMO_VISAO, MAXIMO_VISAO),
                                  random.uniform(MINIMO_VELOCIDADE, MAXIMO_VELOCIDADE),
                                  (0, 100, 255),
                                  1))

    media_ir = sum(c.pesos["ir_para_comida"] for c in novas if hasattr(c, "pesos")) / len(novas)
    media_rand = sum(c.pesos["aleatoriedade"] for c in novas if hasattr(c, "pesos")) / len(novas)
    print(f"Médias dos pesos → comida: {media_ir:.2f}, aleatoriedade: {media_rand:.2f}")

    return novas

