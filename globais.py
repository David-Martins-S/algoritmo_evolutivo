import json
import os

CAMINHO_CONFIG = "config_simulacao.json"


# Carrega os parâmetros de simulação do arquivo JSON
def carregar_config():
    if os.path.exists(CAMINHO_CONFIG):
        with open(CAMINHO_CONFIG, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        print("Arquivo de configuração não encontrado. Usando valores padrão.")
        return {}


# Salva parâmetros atuais no arquivo JSON
def salvar_config(dados):
    with open(CAMINHO_CONFIG, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4)


# Carrega e aplica os valores nas globais
dados = carregar_config()

LARGURA = dados.get("LARGURA", 800)
ALTURA = dados.get("ALTURA", 600)
NUM_COMIDAS_INICIAL = dados.get("NUM_COMIDAS_INICIAL", 60)
NUM_CRIATURAS_INICIAL = dados.get("NUM_CRIATURAS_INICIAL", 30)
PASSOS_GERACAO = dados.get("PASSOS_GERACAO", 500)
FPS = dados.get("FPS", 60)
MINIMO_VISAO = dados.get("MINIMO_VISAO", 20)
MAXIMO_VISAO = dados.get("MAXIMO_VISAO", 60)
MINIMO_VELOCIDADE = dados.get("MINIMO_VELOCIDADE", 0.1)
MAXIMO_VELOCIDADE = dados.get("MAXIMO_VELOCIDADE", 1)
VARIACAO_VELOCIDADE = dados.get("VARIACAO_VELOCIDADE", 0.2)
VARIACAO_VISAO = dados.get("VARIACAO_VISAO", 8)
VARIACAO_COR = dados.get("VARIACAO_COR", 30)
COR_INICIAL = tuple(dados.get("COR_INICIAL", [0, 100, 255]))
CSV_ARQUIVO = dados.get("CSV_ARQUIVO", "dados.csv")
MOSTRA_BARRA_ENERGIA = False
MOSTRA_COMIDA_COMIDA = True
MOSTRA_CIRCULO_VISAO = dados.get("CIRCULO_VISAO", False)
MOSTRA_LINHA_LIGACAO = True
MOSTRA_TEXTO_CABECA_CRIATURA = False

