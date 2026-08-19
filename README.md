<div align="center">

# wmsbox-agent

### Agente de IA que responde perguntas em linguagem natural sobre estoque de eletrônicos

[![Python](https://img.shields.io/badge/Python-3.14-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-Agent-1C3C3C?style=for-the-badge&logo=langchain)](https://www.langchain.com/)
[![Hugging Face](https://img.shields.io/badge/LLM-Qwen2.5--72B%20(HF)-FFD21E?style=for-the-badge&logo=huggingface)](https://huggingface.co/)
[![Streamlit](https://img.shields.io/badge/App-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)](https://wmsbox-agent-irc5h9jspgid78r7y4yjkz.streamlit.app)
[![Desafio](https://img.shields.io/badge/Desafio-Alura%20Agent-orange?style=for-the-badge)](https://www.alura.com.br/)

**[Acessar o app online](https://wmsbox-agent-irc5h9jspgid78r7y4yjkz.streamlit.app)**

</div>

---

## Índice

- [Sobre o Projeto](#sobre)
- [Problema](#problema)
- [Arquitetura do Agente](#arquitetura)
- [Stack Tecnológica](#stack)
- [Estrutura de Pastas](#estrutura)
- [Como Rodar](#instalacao)
- [Deploy](#deploy)
- [Exemplos de Uso](#exemplos)
- [Decisões Técnicas](#decisoes)
- [Limitações Conhecidas](#limitacoes)
- [Próximos Passos](#proximos)
- [Referências](#referencias)

---

<a name="sobre"></a>
## Sobre o Projeto

O **wmsbox-agent** é um agente de IA construído em Python para o desafio final **"Alura Agent"**. Ele lê um CSV com o estoque de um armazém de eletrônicos e responde, em português e em linguagem natural, perguntas sobre esses dados — sem que a pessoa precise abrir a planilha ou escrever uma fórmula.

Tem uma interface web (Streamlit) com chat, visualização do estoque atual e opção de importar outro CSV no mesmo formato — não fica preso a um arquivo fixo.

```
"Quantas unidades do produto WMS-0001 temos?"
"Quais itens estão com estoque físico zerado?"
"Qual o valor total em estoque?"
"Quais produtos têm mais de 10 unidades a caminho do Full?"
```

---

<a name="problema"></a>
## Problema

Consultar estoque hoje normalmente significa abrir uma planilha, aplicar filtros manualmente e, muitas vezes, montar uma fórmula nova para cada pergunta diferente. Isso é lento e exige saber onde cada coluna está e como combiná-las.

A proposta aqui é inverter isso: a pessoa faz a pergunta como faria para um colega de trabalho, e o agente descobre sozinho quais colunas usar, qual operação aplicar (soma, contagem, filtro, comparação) e devolve a resposta.

---

<a name="arquitetura"></a>
## Arquitetura do Agente

Perguntas sobre estoque são numéricas (somas, contagens, filtros, comparações) e exigem operar sobre a tabela inteira. Por isso o agente usa **`create_pandas_dataframe_agent`** (LangChain + `langchain-experimental`): o LLM traduz a pergunta em código pandas real, esse código é executado de verdade sobre o `DataFrame` carregado do CSV, e o resultado devolvido é exato — não uma aproximação de texto.

```
Pergunta → LLM gera código pandas → executa no DataFrame → resposta exata

"qual o valor total em estoque?"  →  df['total_reais'].sum()
"estoque físico zerado?"          →  df[df['fisico_atual'] == 0]
```

---

<a name="stack"></a>
## Stack Tecnológica

| Categoria | Tecnologia | Função |
|:---------:|:----------:|:------:|
| **Linguagem** | Python 3.14 | Base do projeto |
| **Dados** | pandas | Carrega e manipula o CSV de estoque |
| **Orquestração** | LangChain | Conecta o LLM às ferramentas do agente |
| **Agente** | langchain-experimental | `create_pandas_dataframe_agent` |
| **LLM** | Qwen2.5-72B-Instruct via Hugging Face (`langchain-openai` + roteador `router.huggingface.co/v1`) | Interpreta a pergunta e gera o código pandas |
| **Configuração** | python-dotenv | Carrega o token de API a partir de um `.env` local |
| **Interface** | Streamlit | Chat web, visualização do estoque e importação de CSV |
| **Deploy** | Docker + Oracle Cloud Infrastructure (OCI) | Empacota e roda a aplicação em uma instância na nuvem |
| **Hospedagem pública** | Streamlit Community Cloud | App acessível por link, direto do repositório GitHub |

---

<a name="estrutura"></a>
## Estrutura de Pastas

```
wmsbox-agent/
├── README.md
├── requirements.txt          ← Dependências do projeto
├── Dockerfile                 ← Empacota a aplicação em container
├── .dockerignore
├── .gitignore
├── .env.example               ← Modelo do arquivo de variáveis de ambiente
├── data/
│   └── estoque.csv             ← Base de dados do estoque
├── src/
│   ├── config.py               ← Carrega o token e configura o LLM (Hugging Face)
│   ├── agente_estoque.py       ← Carrega o CSV e monta o agente pandas
│   ├── main.py                 ← Ponto de entrada: loop de perguntas no terminal
│   └── app_streamlit.py        ← Ponto de entrada: interface web (chat)
└── assets/                     ← Reservado para imagens/prints do README
```

---

<a name="instalacao"></a>
## Como Rodar

### Pré-requisitos

- Python 3.11+
- Um token da Hugging Face, gratuito, com permissão **"Inference"**, gerado em [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

### 1. Clonar o repositório

```bash
git clone https://github.com/Eduardodanield/wmsbox-agent.git
cd wmsbox-agent
```

### 2. Criar e ativar o ambiente virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar o token de API

```bash
# Copie o modelo e cole seu token real dentro do .env gerado
cp .env.example .env
```

Abra o `.env` e preencha:

```
HUGGINGFACE_API_TOKEN=seu_token_aqui
```

### 5. CSV de estoque

O repositório já vem com `data/estoque.csv`. Pra usar outro, é só substituir o arquivo (mesmas colunas) ou importar um novo pela interface web:

```
sku, produto, tipo, mlb_codigo, fisico_atual, full_magazine_qtd,
a_caminho_magazine, full_pegleve_qtd, a_caminho_pegleve,
custo_unitario, total_reais, estoque_geral
```

### 6. Rodar o agente

Pelo terminal:

```bash
python src/main.py
```

**Saída esperada:**

```
============================================================
Agente de Estoque - wmsbox-agent
Pergunte algo sobre o estoque (ex: 'qual o valor total em estoque?')
Digite 'exit/sair/quit' para encerrar.
============================================================

Você: quantos itens estão com estoque físico zerado?

Agente: [resposta calculada em tempo real a partir do seu CSV]
```

Ou pela interface web:

```bash
streamlit run src/app_streamlit.py
```

Abre automaticamente em `http://localhost:8501`.

---

<a name="deploy"></a>
## Deploy

O app roda em três formas, todas a partir do mesmo código:

**1. Local** — `python src/main.py` ou `streamlit run src/app_streamlit.py`, como descrito acima.

**2. Container Docker** — o `Dockerfile` empacota a aplicação (Python + dependências + código):

```bash
docker build -t wmsbox-agent .
docker run -it --env-file .env wmsbox-agent
```

**3. Nuvem (Oracle Cloud Infrastructure)** — o mesmo container roda numa instância Compute gratuita (Always Free) da OCI, acessada via SSH. Evidência de deploy funcionando: agente respondendo perguntas de dentro da instância remota.

**4. Streamlit Community Cloud** — a interface web fica publicamente acessível, conectada direto neste repositório GitHub, sem precisar manter nenhum servidor próprio ligado: **[wmsbox-agent-irc5h9jspgid78r7y4yjkz.streamlit.app](https://wmsbox-agent-irc5h9jspgid78r7y4yjkz.streamlit.app)**

O token de API não vai para o repositório em nenhum dos casos — no Docker/OCI ele é passado via `--env-file .env`; no Streamlit Cloud, via um recurso próprio de "Secrets" do serviço.

---

<a name="exemplos"></a>
## Exemplos de Uso

### Perguntas testadas e validadas

| Pergunta | Resposta do agente |
|---|---|
| Qual o valor total em estoque? | R$ 7.201.110,22 |
| Quantos produtos estão com estoque físico zerado? | 61 produtos |
| Quais os 5 produtos com maior estoque geral? | 1. Teclado Sem Fio T10 Verde (WMS-0148) — 4399 un.<br>2. Cartão de Memória Neo Azul (WMS-0094) — 3965 un.<br>3. Suporte Veicular Max Azul (WMS-0132) — 2620 un.<br>4. Controle Bluetooth Lite Vermelho (WMS-0131) — 2510 un.<br>5. Adaptador USB S1 Verde (WMS-0247) — 2254 un. |

Essas três respostas foram conferidas manualmente contra o CSV (`df['total_reais'].sum()`, `df[df['fisico_atual'] == 0]` e `df.nlargest(5, 'estoque_geral')`, respectivamente) e batem exatamente.

### Outras perguntas que o agente também responde

O agente segue o mesmo princípio para qualquer combinação de filtro/soma/contagem sobre as colunas do CSV — estas ainda não foram testadas formalmente, mas usam a mesma lógica das já validadas acima:

- "Quantas unidades do produto WMS-0001 temos?"
- "Quais produtos têm mais de 10 unidades a caminho do Full Magazine?"
- "Quantos tipos diferentes de produto existem no estoque?"

---

<a name="decisoes"></a>
## Decisões Técnicas

| Decisão | Motivo |
|---|---|
| `encoding="utf-8-sig"` ao ler o CSV | O arquivo tem um BOM (marca invisível de UTF-8) no início; sem isso, a primeira coluna vinha lida como `"﻿sku"` em vez de `"sku"` |
| `temperature=0` no LLM | Respostas mais consistentes e determinísticas — não queremos variação criativa em números de estoque |
| LLM via Hugging Face (`ChatOpenAI` + roteador `router.huggingface.co/v1`) | Endpoint compatível com a API da OpenAI → tool calling maduro no LangChain, essencial para `agent_type="tool-calling"` funcionar bem |
| `allow_dangerous_code=True` | Necessário para o agente executar o código pandas que ele mesmo escreve. Aceitável aqui porque o CSV é local e o agente não é exposto a usuários externos |
| Caminho do CSV resolvido via `__file__` | Garante que `data/estoque.csv` seja encontrado não importa de qual pasta o script for executado |
| Token lido de `st.secrets` como alternativa ao `.env` | No Streamlit Community Cloud não existe `.env` — o token é injetado pelo painel de "Secrets" do próprio serviço |

---

<a name="limitacoes"></a>
## Limitações Conhecidas

- **Perguntas compostas em uma frase só** (ex: "qual o SKU *e* quantas unidades tem o primeiro produto?") podem fazer o agente retornar uma resposta vazia. Perguntas de uma coisa por vez funcionam de forma confiável.
- `langchain-experimental` (pacote que fornece o `create_pandas_dataframe_agent`) está marcado pelo mantenedor como não mais ativamente desenvolvido. Continua funcional, mas vale acompanhar se o LangChain lançar um substituto oficial.
- O agente executa código Python gerado pelo modelo (`allow_dangerous_code=True`) — adequado para uso local com seus próprios dados, não recomendado para expor publicamente sem sandbox.
- A instância OCI usada (tier gratuito Always Free) tem só 1 GB de RAM — suficiente para rodar o container, mas instalações pesadas (como a do próprio Docker) podem precisar de swap para não travar a máquina.

---

<a name="proximos"></a>
## Próximos Passos

- Autenticação/controle de acesso na interface web, caso vá além de uso pessoal/demonstração
- Suporte a mais de um arquivo de estoque carregado ao mesmo tempo (comparar dois períodos, por exemplo)

---

<a name="referencias"></a>
## Referências

- **Curso "Alura Agent"** — [alura.com.br](https://www.alura.com.br/) — desafio final que originou este projeto
- **Canal Hashtag Programação** — vídeo [*"Agente de IA completo com Python - Projeto RAG com Langchain"*](https://www.youtube.com/watch?v=0M8iO5ykY-E) — base de aprendizado sobre LangChain
- **LangChain** — [documentação oficial](https://python.langchain.com/) do `create_pandas_dataframe_agent`
- **Hugging Face** — [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) — geração do token de API
- **Streamlit** — [documentação oficial](https://docs.streamlit.io/) — construção da interface web e deploy no Community Cloud
- **Oracle Cloud Infrastructure** — [Always Free Compute](https://www.oracle.com/cloud/free/) — instância usada para o deploy em nuvem
