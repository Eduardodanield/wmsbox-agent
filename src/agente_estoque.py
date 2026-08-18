import os

import pandas as pd
from langchain_experimental.agents import create_pandas_dataframe_agent

from config import llm

# __file__ é o caminho deste arquivo (src/agente_estoque.py). Subimos um
# nível (dirname duas vezes) para chegar na raiz do projeto e então
# entramos em data/. Montar o caminho assim, em vez de usar a string
# "data/estoque.csv" direto, garante que o CSV seja encontrado não
# importa de qual pasta o comando "python ..." for executado.
PASTA_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAMINHO_CSV = os.path.join(PASTA_PROJETO, "data", "estoque.csv")

# encoding="utf-8-sig" remove o BOM (marca invisível no início do arquivo)
# que costuma aparecer em CSVs exportados como "UTF-8" pelo Excel. Sem
# isso, o nome da primeira coluna viria como "﻿sku" em vez de "sku"
# e quebraria qualquer filtro que dependesse desse nome de coluna.
df = pd.read_csv(CAMINHO_CSV, encoding="utf-8-sig")

# create_pandas_dataframe_agent monta um agente que recebe uma pergunta
# em linguagem natural, escreve código pandas para respondê-la e EXECUTA
# esse código de verdade sobre o DataFrame acima — diferente de um RAG,
# que só recuperaria trechos de texto parecidos com a pergunta.
#
# agent_type="tool-calling": usa o mecanismo de "function calling" nativo
# do Gemini para acionar a ferramenta de execução de código, em vez do
# formato antigo baseado em interpretar texto livre (mais frágil).
#
# allow_dangerous_code=True: obrigatório para o agente poder executar o
# código pandas que ele mesmo escreve. Só é aceitável aqui porque o CSV
# é nosso, o agente roda local e não está exposto a usuários externos.
#
# verbose=True: imprime no terminal o raciocínio e o código pandas que o
# agente gerou antes de cada resposta — útil para entender o que está
# acontecendo por trás da resposta final.
agente = create_pandas_dataframe_agent(
    llm,
    df,
    agent_type="tool-calling",
    allow_dangerous_code=True,
    verbose=True,
)
