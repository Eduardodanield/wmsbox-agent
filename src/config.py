import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# load_dotenv() lê o arquivo .env da raiz do projeto e injeta cada linha
# dele (ex: HUGGINGFACE_API_TOKEN=xxxx) como variável de ambiente do
# processo. É por isso que conseguimos ler o token com os.getenv logo
# abaixo sem nunca escrever o token real dentro do código.
load_dotenv()

HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

# Falha rápido e com mensagem clara se alguém esquecer de criar o .env,
# em vez de deixar o erro estourar mais tarde, dentro do LangChain, com
# uma mensagem confusa sobre autenticação.
if not HUGGINGFACE_API_TOKEN:
    raise RuntimeError(
        "HUGGINGFACE_API_TOKEN não encontrada. Copie .env.example para .env "
        "e cole ali seu token da Hugging Face, com permissão 'Inference' "
        "(huggingface.co/settings/tokens)."
    )

# O roteador da Hugging Face (router.huggingface.co) expõe vários modelos
# open-source através de uma API compatível com a da OpenAI. Por isso
# usamos ChatOpenAI (pacote langchain-openai) só apontando base_url/api_key
# para lá, em vez de ChatHuggingFace/HuggingFaceEndpoint — essas duas são
# integrações pensadas para a API "clássica" de Inference da Hugging Face,
# com suporte a tool calling menos maduro no LangChain. O ChatOpenAI é o
# cliente de tool calling mais usado e testado do LangChain, e é esse tool
# calling maduro que faz o create_pandas_dataframe_agent continuar
# confiável usando agent_type="tool-calling" (em vez de cair de volta no
# modo antigo, baseado em parsing de texto livre, mais frágil).
#
# Qwen2.5-72B-Instruct: modelo aberto com bom equilíbrio entre seguir tool
# calling de forma confiável e gerar código correto — o que interessa aqui,
# já que o agente passa a maior parte do tempo escrevendo pandas. Se esse
# modelo não estiver disponível no seu tier gratuito, troque só esta
# string por, por exemplo, "meta-llama/Llama-3.3-70B-Instruct".
#
# temperature=0 mantém a mesma lógica de antes: menos variação criativa,
# mais previsibilidade ao gerar código pandas.
llm = ChatOpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HUGGINGFACE_API_TOKEN,
    model="Qwen/Qwen2.5-72B-Instruct",
    temperature=0,
)
