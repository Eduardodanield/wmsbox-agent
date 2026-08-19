import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Carrega o token do .env para o ambiente do processo.
load_dotenv()

HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

# Falha cedo com mensagem clara em vez de um erro confuso lá na frente.
if not HUGGINGFACE_API_TOKEN:
    raise RuntimeError(
        "HUGGINGFACE_API_TOKEN não encontrada. Copie .env.example para .env "
        "e cole ali seu token da Hugging Face, com permissão 'Inference' "
        "(huggingface.co/settings/tokens)."
    )

# ChatOpenAI apontado pro roteador da Hugging Face (API compatível com a
# da OpenAI) — dá o tool calling maduro que o create_pandas_dataframe_agent
# precisa pra usar agent_type="tool-calling" de forma confiável.
# temperature=0 deixa a geração de código pandas mais previsível.
llm = ChatOpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HUGGINGFACE_API_TOKEN,
    model="Qwen/Qwen2.5-72B-Instruct",
    temperature=0,
)
