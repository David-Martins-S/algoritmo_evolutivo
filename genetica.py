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
        """Cria uma nova instância representando o pai que sobrevive sem mutação."""
        parent_generation = getattr(parent, "geracao", 1)
        new_generation = parent_generation
        parent_idade = getattr(parent, "idade")
        nova_idade = parent_idade + 15
        sexo = getattr(parent, "sexo")
        risco = getattr(parent, "risco")
        family_id = getattr(parent, "family_id")
        altruismo = getattr(parent, "altruismo")
        doou_comida = getattr(parent, "doou_comida", 0)

        p = Criatura(random.uniform(0, globais.LARGURA),
                     random.uniform(0, globais.ALTURA),
                     visao=int(parent.visao),
                     velocidade=float(parent.velocidade),
                     cor=getattr(parent, "cor", (0, 100, 255)),
                     geracao=new_generation,
                     idade=nova_idade,
                     sexo=sexo,
                     risco=risco,
                     family_id=family_id,
                     altruismo=altruismo,
                     doou_comida=doou_comida)
        # Preserva energia? normalmente resetamos energia para 100 na nova geração
        p.energia = getattr(parent, "energia", 100)
        comida_anterior = getattr(parent, "comida_comida", 1)
        p.comida_comida = 1 if comida_anterior > 1 else 0
        p.cor = (0, 100, 255) if p.sexo == 'M' else (255, 192, 203)
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

    media_ir = sum(c.pesos["ir_para_comida"] for c in novas if hasattr(c, "pesos")) / len(novas)
    media_rand = sum(c.pesos["aleatoriedade"] for c in novas if hasattr(c, "pesos")) / len(novas)
    print(f"Médias dos pesos → comida: {media_ir:.2f}, aleatoriedade: {media_rand:.2f}")

    return novas

