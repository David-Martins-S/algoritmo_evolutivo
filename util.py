import os
import csv
import random
from criatura import Criatura

def salvar_dados_csv(geracao, criaturas):
    arquivo = 'dados.csv'
    existe = os.path.isfile(arquivo)
    media_visao = sum([c.visao for c in criaturas]) / len(criaturas) if criaturas else 0
    with open(arquivo, 'a', newline='') as f:
        writer = csv.writer(f)
        if not existe:
            writer.writerow(['Geração', 'População', 'Média de Visão'])
        writer.writerow([geracao, len(criaturas), round(media_visao, 2)])

def nova_geracao(criaturas):
    novas_criaturas = []
    for c in criaturas:
        if c.comida_comida >= 1:
            # Criatura sobrevive
            novas_criaturas.append(Criatura(c.x, c.y, c.visao))
            # Reprodução se comeu 2 ou mais
            if c.comida_comida >= 2:
                nova_visao = max(20, min(150, c.visao + random.randint(-10, 10)))  # mutação leve
                novas_criaturas.append(Criatura(c.x, c.y, nova_visao))
    return novas_criaturas