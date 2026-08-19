import os

import pandas as pd
from langchain_experimental.agents import create_pandas_dataframe_agent

from config import llm

# Caminho absoluto do CSV, pra funcionar não importa de onde o script rodar.
PASTA_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAMINHO_CSV = os.path.join(PASTA_PROJETO, "data", "estoque.csv")

# Colunas exigidas de qualquer CSV de estoque, padrão ou importado.
COLUNAS_ESPERADAS = [
    "sku", "produto", "tipo", "mlb_codigo", "fisico_atual",
    "full_magazine_qtd", "a_caminho_magazine", "full_pegleve_qtd",
    "a_caminho_pegleve", "custo_unitario", "total_reais", "estoque_geral",
]


def criar_agente(df):
    """Cria um agente pandas para o DataFrame informado."""
    # tool-calling usa o function calling nativo do modelo; allow_dangerous_code
    # é necessário pra ele poder executar o código pandas que ele mesmo escreve.
    return create_pandas_dataframe_agent(
        llm,
        df,
        agent_type="tool-calling",
        allow_dangerous_code=True,
        verbose=True,
    )


# utf-8-sig remove o BOM do CSV (senão a coluna "sku" vem com caractere invisível junto).
# Se o arquivo não existir por algum motivo, df/agente ficam None e a tela
# pede pra importar um CSV em vez de travar.
if os.path.exists(CAMINHO_CSV):
    df = pd.read_csv(CAMINHO_CSV, encoding="utf-8-sig")
    agente = criar_agente(df)
else:
    df = None
    agente = None
