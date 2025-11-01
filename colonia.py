import random
import statistics

import globais


class Colonia:
    def __init__(self, family_id):
        self.family_id = family_id
        self.criaturas = []
        self.idade = 0
        self.comida_total = 0
        self.altruismo_medio = 0
        self.visao_media = 0
        self.velocidade_media = 0
        self.risco_medio = 0
        self.populacao_viva = 0
        self.populacao_inicial = 0
        self.geracao = 1
        self.cor = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        self.tipo = "neutra"  # pode virar "rainha", "coletora", etc. no futuro
        self.lado_colonia = random.choice(["esquerda", "direita"])

    def adicionar_criatura(self, criatura):
        """Adiciona uma criatura à colônia."""
        if not criatura in self.criaturas:
            self.criaturas.append(criatura)
            if globais.BARREIRA_ATIVADA:
                if self.lado_colonia == "esquerda":
                    criatura.x = random.uniform(0, globais.LARGURA//2 - 20)
                else:
                    criatura.x = random.uniform(globais.LARGURA//2 + 20, globais.LARGURA)
            self.populacao_inicial += 1


    def atualizar(self):
        """Atualiza estatísticas internas da colônia."""

        #Remove da colônia criaturas que morreram
        self.criaturas = [c for c in self.criaturas if c.comida_comida > 0]
        self.comida_total = sum(c.comida_comida for c in self.criaturas)
        if self.criaturas:
            self.altruismo_medio = statistics.mean(c.altruismo for c in self.criaturas)
            self.visao_media = statistics.mean(c.visao for c in self.criaturas)
            self.velocidade_media = statistics.mean(c.velocidade for c in self.criaturas)
            self.risco_medio = statistics.mean(c.risco for c in self.criaturas)
        self.idade += 1
        self.atualiza_populacao_viva()

    def esta_extinta(self):
        """Retorna True se a colônia perdeu todas as criaturas."""
        return len(self.criaturas) == 0

    def estatisticas(self):
        """Retorna um dicionário com dados úteis para salvar em CSV."""
        return {
            "family_id": self.family_id,
            "idade": self.idade,
            "geracao": self.geracao,
            "populacao_viva": self.populacao_viva,
            "comida_total": self.comida_total,
            "altruismo_medio": round(self.altruismo_medio, 3),
            "visao_media": round(self.visao_media, 2),
            "velocidade_media": round(self.velocidade_media, 2),
            "risco_medio": round(self.risco_medio, 3),
        }

    def atualiza_populacao_viva(self):
        self.populacao_viva = len(self.criaturas)

    def doar_para_familia(self, prioridade_gravidas=True, max_por_doador=None):
        """
        Redistribui comida dentro da colônia **somente** entre criaturas que se encontraram.
        - prioridade_gravidas: se True, tenta ajudar primeiro fêmeas detectaram parceiro (gravidas).
        - max_por_doador: limite opcional de unidades que um doador pode ceder por rodada (None = sem limite exceto deixar 1).
        """
        # lista de possíveis beneficiários (famintos) - fêmeas grávidas primeiro se flag True
        famintos = []
        for c in self.criaturas:
            # se está grávida e precisa de comida para garantir filhos: considerar como faminta (prioritária)
            if prioridade_gravidas and getattr(c, "detectou_parceiro", False) and c.comida_comida < 2:
                famintos.append((c, 2 - c.comida_comida))  # precisa de 1 ou 2 para completar
            # pessoas sem comida
            elif c.comida_comida == 0:
                famintos.append((c, 1))
        # separa gravidas primeiro se pedido
        if prioridade_gravidas:
            famintos.sort(key=lambda tup: 0 if tup[0].detectou_parceiro else 1)

        # para cada faminto, procure doadores que SE ENCONTRARAM com ele nesta rodada
        for needy, need_amount in famintos:
            if need_amount <= 0:
                continue

            # candidatos doadores: membros da mesma colônia que tiveram encontro com 'needy'
            candidatos = []
            for d in self.criaturas:
                if d is needy:
                    continue
                # só considerar doadores na mesma colônia (já garantido) e que possuam >1 comida
                if d.comida_comida > 1:
                    # verificar se houve encontro recíproco (qualquer direção)
                    encontros_d = getattr(d, "encontros_recentes", set())
                    encontros_needy = getattr(needy, "encontros_recentes", set())
                    if id(needy) in encontros_d or id(d) in encontros_needy:
                        candidatos.append(d)

            # ordenar por altruismo decrescente (doadores mais altruístas primeiro)
            candidatos.sort(key=lambda x: getattr(x, "altruismo", 0), reverse=True)

            for d in candidatos:
                if need_amount <= 0:
                    break
                # chance de doar baseado no altruismo (opcional, já testado em tentar_doar)
                prob = getattr(d, "altruismo", 0.0)
                if random.random() > prob:
                    # doador não se sente altruísta neste encontro
                    continue

                # quanto pode doar sem deixar-se em risco (deixa ao menos 1 para sobreviver)
                disponivel = d.comida_comida - 1
                if disponivel <= 0:
                    continue

                # limitar quanto cede
                if max_por_doador is not None:
                    disponivel = min(disponivel, max_por_doador)

                transferencia = min(disponivel, need_amount)

                # efetua a transferência
                d.comida_comida -= transferencia
                needy.comida_comida += transferencia
                d.doou_comida = getattr(d, "doou_comida", 0) + transferencia

                need_amount -= transferencia

            # fim de tentativa para este needy

        # fim do método

