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

import os
import sys
import pygame
import subprocess
import time

def reiniciar_programa():
    """Tenta reiniciar o script atual.
    Primeiro tenta execv (substitui o processo). Se falhar, abre um novo processo e sai.
    """
    try:
        pygame.quit()
    except Exception:
        pass

    python = sys.executable  # caminho completo para o interpretador usado
    args = [python] + sys.argv

    # Tenta substituir o processo atual (mais "limpo")
    try:
        os.execv(python, args)
    except Exception:
        # fallback: spawn em segundo plano e encerrar o processo atual
        # Use stdout/stderr encaminhados para ver logs se quiser
        try:
            subprocess.Popen(args)
        except Exception as e:
            # nada que possamos fazer — registra o erro e sai
            print("Falha ao spawnar novo processo:", e)
        # dá um pequeno delay pra garantir que o novo processo comece
        time.sleep(0.1)
        sys.exit(0)
