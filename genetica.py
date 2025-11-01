import random
import globais
from criatura import Criatura


def nova_geracao(geracao_finalizada, geracao_atual):
    novas = []

    def cria_herdeiro(parent):
        """Cria um filho a partir de um objeto 'parent' aplicando mutações suaves."""
        nova_visao = int(parent.visao + random.randint(-globais.VARIACAO_VISAO, globais.VARIACAO_VISAO))
        nova_vel = parent.velocidade + random.uniform(-globais.VARIACAO_VELOCIDADE, globais.VARIACAO_VELOCIDADE)
        altruismo = max(0, parent.altruismo + random.uniform(-globais.VARIACAO_ALTRUISMO, globais.VARIACAO_ALTRUISMO))
        parent_generation = getattr(parent, "geracao", 1)
        filho_geracao = geracao_atual + 1
        novo_risco = parent.risco + random.uniform(-globais.VARIACAO_RISCO, globais.VARIACAO_RISCO)
        if novo_risco < 0:
            novo_risco = 0
        elif novo_risco > 1:
            novo_risco = 1
        autoexploracao = max(0, min(1, parent.autoexploracao + random.uniform(-0.1, 0.1)))
        family_id = parent.family_id

        # Cria o objeto
        filho = Criatura(random.uniform(0, globais.LARGURA),
                         random.uniform(0, globais.ALTURA),
                         visao=nova_visao,
                         velocidade=nova_vel,
                         cor=None,
                         geracao=filho_geracao,
                         risco=novo_risco,
                         family_id=family_id,
                         autoexploracao=autoexploracao,
                         altruismo=altruismo)

        filho.cor = (0, 100, 255) if filho.sexo == 'M' else (255, 192, 203)

        return filho

    def cria_pai_sem_mutacao(parent):
        """Apenas retorna o pai atualizando atributos."""
        parent.idade = getattr(parent, "idade") + 15
        # parent.x = random.uniform(0, globais.LARGURA)
        # parent.y = random.uniform(0, globais.ALTURA)
        parent.energia = 100
        comida_anterior = getattr(parent, "comida_comida", 1)
        parent.comida_comida = 1 if comida_anterior > 1 else 0 # rever isto
        parent.detectou_parceiro = False

        return parent


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

                num_filhos = min(eaten - 1, 10)  # 1 comida = 0 filhos, 2 = 1, 3 = 2, 4+ = 3
                for _ in range(num_filhos):
                    f = cria_herdeiro(parent)
                    f.comida_comida = 1  # cada filho nasce "alimentado"
                    novas.append(f)

                parent.comida_comida = 1
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
            novas.append(Criatura(random.uniform(0, globais.LARGURA),
                                  random.uniform(0, globais.ALTURA),
                                  random.randint(globais.MINIMO_VISAO, globais.MAXIMO_VISAO),
                                  random.uniform(globais.MINIMO_VELOCIDADE, globais.MAXIMO_VELOCIDADE),
                                  (0, 100, 255),
                                  1))


    return novas

