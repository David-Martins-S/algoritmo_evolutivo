import json
import os

CAMINHO_CONFIG = "config_simulacao.json"
LARGURA = 1360
ALTURA = 768
NUM_COMIDAS_INICIAL = 60
NUM_CRIATURAS_INICIAL = 31
PASSOS_GERACAO = 1200
FPS = 60
MINIMO_VISAO = 20
MAXIMO_VISAO = 60
MINIMO_RISCO = 0.25
MAXIMO_RISCO = 0.5
VARIACAO_RISCO = 0.01
MINIMO_VELOCIDADE = 0.5
MAXIMO_VELOCIDADE = 1
VARIACAO_VELOCIDADE = 0.2
VARIACAO_VISAO = 8
VARIACAO_COR = 30
CSV_ARQUIVO = "dados.csv"
MOSTRA_BARRA_ENERGIA = "False"
MOSTRA_COMIDA_COMIDA = "True"
MOSTRA_CIRCULO_VISAO = "False"
MOSTRA_LINHA_LIGACAO = "True"
MOSTRA_TEXTO_CABECA_CRIATURA = "False"
MOSTRA_GRAVIDEZ = "True"
LIGA_SOM_COMER = "False"
LIGA_SOM_VUSH = "True"
VARIACAO_ALTRUISMO = 0.1
BARREIRA_ATIVADA = False

ANT_FAMILY_NAMES = [
    "Formicidae Prime",
    "Mandíbula Vermelha",
    "Rainha Solar",
    "Terranautas",
    "Ninho do Amanhecer",
    "As Diligentes",
    "Linha Alfa",
    "Os Recolectores",
    "Dinastia da Areia",
    "Semente Viva",
    "As Perseverantes",
    "Colônia Âmbar",
    "Clã do Tronco",
    "Os Mineradores",
    "Filhas do Sol",
    "Linha Obsidiana",
    "Os Vigilantes",
    "Casa Rubra",
    "As Operárias de Ferro",
    "Os Doceiros",
    "Família Hexápode",
    "Colônia Esmeralda",
    "Os Traçadores",
    "Dinastia Eclipse",
    "Ninho do Vento",
    "Os Escavadores",
    "Casa Aurora",
    "Os Enfileirados",
    "Clã das Folhas",
    "Família Granular"
]


def carregar_config():
    """Carrega o arquivo de configuração JSON, se existir."""
    if os.path.exists(CAMINHO_CONFIG):
        with open(CAMINHO_CONFIG, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        print("Arquivo de configuração não encontrado. Usando valores padrão.")
        return {}


def salvar_config(dados):
    """Salva as configurações no arquivo JSON."""
    with open(CAMINHO_CONFIG, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


# Carrega o dicionário de configurações
dados = carregar_config()

# Torna todas as chaves disponíveis como variáveis globais
for chave, valor in dados.items():
    globals()[chave] = valor


