import json
import os

CAMINHO_CONFIG = "config_simulacao.json"


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
