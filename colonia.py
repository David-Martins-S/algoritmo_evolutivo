import random
import statistics

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

    def adicionar_criatura(self, criatura):
        """Adiciona uma criatura à colônia."""
        self.criaturas.append(criatura)
        self.populacao_inicial += 1

    def atualizar(self):
        """Atualiza estatísticas internas da colônia."""
        self.criaturas = [c for c in self.criaturas if c.energia > 0]  # remove mortos
        self.populacao_viva = len(self.criaturas)
        self.comida_total = sum(c.comida_comida for c in self.criaturas)

        if self.criaturas:
            self.altruismo_medio = statistics.mean(c.altruismo for c in self.criaturas)
            self.visao_media = statistics.mean(c.visao for c in self.criaturas)
            self.velocidade_media = statistics.mean(c.velocidade for c in self.criaturas)
            self.risco_medio = statistics.mean(c.risco for c in self.criaturas)

        self.idade += 1

    def doar_para_familia(self):
        """Redistribui comida dentro da colônia (cooperação interna)."""
        famintos = [c for c in self.criaturas if c.comida_comida == 0]
        doadores = [c for c in self.criaturas if c.comida_comida > 1]
        random.shuffle(doadores)

        for d in doadores:
            if not famintos:
                break
            alvo = random.choice(famintos)
            d.comida_comida -= 1
            alvo.comida_comida += 1
            famintos.remove(alvo)

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
