<div align="center">

# 📦 wmsbox-agent

### Agente de IA que responde perguntas em linguagem natural sobre estoque de eletrônicos

[![Python](https://img.shields.io/badge/Python-3.14-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-Agent-1C3C3C?style=for-the-badge&logo=langchain)](https://www.langchain.com/)
[![Gemini](https://img.shields.io/badge/LLM-Gemini%202.5%20Flash-8E75B2?style=for-the-badge&logo=googlegemini)](https://ai.google.dev/)
[![Desafio](https://img.shields.io/badge/Desafio-Alura%20Agent-orange?style=for-the-badge)](https://www.alura.com.br/)

</div>

---

## 📖 Índice

- [Sobre o Projeto](#sobre)
- [Problema](#problema)
- [Por que agente pandas, e não RAG?](#arquitetura)
- [Stack Tecnológica](#stack)
- [Estrutura de Pastas](#estrutura)
- [Como Rodar](#instalacao)
- [Exemplos de Uso](#exemplos)
- [Decisões Técnicas](#decisoes)
- [Limitações Conhecidas](#limitacoes)
- [Próximos Passos](#proximos)
- [Referências](#referencias)

---

<a name="sobre"></a>
## 🎯 Sobre o Projeto

O **wmsbox-agent** é um agente de IA construído em Python para o desafio final **"Alura Agent"**. Ele lê um CSV com o estoque de um armazém de eletrônicos e responde, em português e em linguagem natural, perguntas sobre esses dados — sem que a pessoa precise abrir a planilha ou escrever uma fórmula.

```
"Quantas unidades do produto WMS-0001 temos?"
"Quais itens estão com estoque físico zerado?"
"Qual o valor total em estoque?"
"Quais produtos têm mais de 10 unidades a caminho do Full?"
```

---

<a name="problema"></a>
## ❓ Problema

Consultar estoque hoje normalmente significa abrir uma planilha, aplicar filtros manualmente e, muitas vezes, montar uma fórmula nova para cada pergunta diferente. Isso é lento e exige saber onde cada coluna está e como combiná-las.

A proposta aqui é inverter isso: a pessoa faz a pergunta como faria para um colega de trabalho, e o agente descobre sozinho quais colunas usar, qual operação aplicar (soma, contagem, filtro, comparação) e devolve a resposta.

---

<a name="arquitetura"></a>
## 🧠 Por que agente pandas, e não RAG?

O caminho mais comum ensinado em tutoriais de "agente de IA com LangChain" é **RAG** (Retrieval-Augmented Generation): o documento é quebrado em pedaços de texto, cada pedaço vira um vetor (embedding), tudo é guardado num banco vetorial (ex: ChromaDB) e, a cada pergunta, o sistema busca os pedaços de texto **mais parecidos semanticamente** com a pergunta para o modelo ler antes de responder.

Isso funciona bem para perguntas sobre **conteúdo** de documentos (“o que diz o contrato sobre X?”). Mas falha para perguntas **numéricas sobre uma tabela inteira**, que é o caso deste projeto:

- Não existe uma linha do CSV "parecida semanticamente" com *"qual o valor total em estoque?"* — essa resposta exige somar a coluna `total_reais` de **todas** as 279 linhas, não recuperar algumas linhas parecidas.
- Mesmo que o RAG trouxesse as linhas certas, quem faria a conta seria o próprio modelo "de cabeça", lendo texto — impreciso e nada confiável para números.

Por isso este projeto usa **`create_pandas_dataframe_agent`** (pacote `langchain-experimental`), um padrão diferente de RAG: o LLM recebe uma ferramenta que executa código Python/pandas de verdade sobre o `DataFrame` carregado do CSV. A pergunta é traduzida em código (`df['total_reais'].sum()`, `df[df.fisico_atual == 0]`, etc.), o código roda de fato, e o resultado é exato — não uma aproximação de texto.

| | RAG (embeddings) | Agente pandas |
|---|---|---|
| Recupera | Pedaços de texto parecidos | — |
| Calcula | ❌ Não soma/filtra dados reais | ✅ Executa pandas de verdade |
| Ideal para | Perguntas sobre conteúdo de texto/documentos | Perguntas numéricas sobre tabelas |
| Usado neste projeto | Não | **Sim** |

---

<a name="stack"></a>
## 🛠️ Stack Tecnológica

| Categoria | Tecnologia | Função |
|:---------:|:----------:|:------:|
| **Linguagem** | Python 3.14 | Base do projeto |
| **Dados** | pandas | Carrega e manipula o CSV de estoque |
| **Orquestração** | LangChain | Conecta o LLM às ferramentas do agente |
| **Agente** | langchain-experimental | `create_pandas_dataframe_agent` |
| **LLM** | Gemini 2.5 Flash (`langchain-google-genai`) | Interpreta a pergunta e gera o código pandas |
| **Configuração** | python-dotenv | Carrega a chave de API a partir de um `.env` local |

**Por que Gemini, e não OpenAI?** O vídeo de referência usa `ChatOpenAI`, que exige um plano pago. `ChatGoogleGenerativeAI` (Gemini) tem um nível gratuito generoso, suficiente para este projeto — a troca é só o import e a classe usada em [src/config.py](src/config.py), o resto do agente não muda.

---

<a name="estrutura"></a>
## 📁 Estrutura de Pastas

```
wmsbox-agent/
├── README.md
├── requirements.txt          ← Dependências do projeto
├── .gitignore
├── .env.example               ← Modelo do arquivo de variáveis de ambiente
├── data/
│   └── estoque.csv            ← Base de dados do estoque (não versionado publicamente)
├── src/
│   ├── config.py               ← Carrega o .env e configura o LLM Gemini
│   ├── agente_estoque.py       ← Carrega o CSV e monta o agente pandas
│   └── main.py                 ← Ponto de entrada: loop de perguntas no terminal
└── assets/                     ← Reservado para imagens/prints do README
```

---

<a name="instalacao"></a>
## ⚙️ Como Rodar

### Pré-requisitos

- Python 3.11+
- Uma chave de API do Gemini, gratuita, gerada em [aistudio.google.com/apikey](https://aistudio.google.com/apikey)

### 1️⃣ Clonar o repositório

```bash
git clone https://github.com/Eduardodanield/wmsbox-agent.git
cd wmsbox-agent
```

### 2️⃣ Criar e ativar o ambiente virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3️⃣ Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4️⃣ Configurar a chave de API

```bash
# Copie o modelo e cole sua chave real dentro do .env gerado
cp .env.example .env
```

Abra o `.env` e preencha:

```
GOOGLE_API_KEY=sua_chave_aqui
```

### 5️⃣ Colocar o CSV de estoque

Coloque seu arquivo em `data/estoque.csv`, com as colunas:

```
sku, produto, tipo, mlb_codigo, fisico_atual, full_magazine_qtd,
a_caminho_magazine, full_pegleve_qtd, a_caminho_pegleve,
custo_unitario, total_reais, estoque_geral
```

### 6️⃣ Rodar o agente

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

---

<a name="exemplos"></a>
## 💬 Exemplos de Uso

*(Respostas reais omitidas de propósito — são calculadas a partir dos seus dados comerciais. O que segue descreve o que o agente faz por trás de cada pergunta.)*

| Pergunta | O que o agente faz |
|---|---|
| "Quantas unidades do produto X temos?" | Filtra a linha pelo `sku`/`produto` e lê `estoque_geral` |
| "Quais itens estão com estoque físico zerado?" | `df[df['fisico_atual'] == 0]` |
| "Qual o valor total em estoque?" | `df['total_reais'].sum()` |
| "Quais produtos têm mais de X unidades a caminho do Full?" | `df[df['a_caminho_magazine'] > X]` |

---

<a name="decisoes"></a>
## 💡 Decisões Técnicas

| Decisão | Motivo |
|---|---|
| `encoding="utf-8-sig"` ao ler o CSV | O arquivo tem um BOM (marca invisível de UTF-8) no início; sem isso, a primeira coluna vinha lida como `"﻿sku"` em vez de `"sku"` |
| `temperature=0` no LLM | Respostas mais consistentes e determinísticas — não queremos variação criativa em números de estoque |
| `agent_type="tool-calling"` | Usa o function calling nativo do Gemini para acionar a execução de código, em vez do parsing de texto livre do modo antigo (mais frágil) |
| `allow_dangerous_code=True` | Necessário para o agente executar o código pandas que ele mesmo escreve. Aceitável aqui porque o CSV é local e o agente não é exposto a usuários externos |
| Caminho do CSV resolvido via `__file__` | Garante que `data/estoque.csv` seja encontrado não importa de qual pasta o script for executado |

---

<a name="limitacoes"></a>
## ⚠️ Limitações Conhecidas

- **Perguntas compostas em uma frase só** (ex: "qual o SKU *e* quantas unidades tem o primeiro produto?") podem fazer o agente retornar uma resposta vazia. Perguntas de uma coisa por vez funcionam de forma confiável.
- `langchain-experimental` (pacote que fornece o `create_pandas_dataframe_agent`) está marcado pelo mantenedor como não mais ativamente desenvolvido. Continua funcional, mas vale acompanhar se o LangChain lançar um substituto oficial.
- O agente executa código Python gerado pelo modelo (`allow_dangerous_code=True`) — adequado para uso local com seus próprios dados, não recomendado para expor publicamente sem sandbox.

---

<a name="proximos"></a>
## 🚀 Próximos Passos

- Empacotar a aplicação em um Dockerfile (etapa futura, fora do escopo desta versão)
- Interface web simples (ex: Streamlit) no lugar do terminal

---

<a name="referencias"></a>
## 📚 Referências

- **Curso "Alura Agent"** — [alura.com.br](https://www.alura.com.br/) — desafio final que originou este projeto
- **Canal Hashtag Programação** — vídeo [*"Agente de IA completo com Python - Projeto RAG com Langchain"*](https://www.youtube.com/watch?v=0M8iO5ykY-E) — base de aprendizado sobre LangChain; a arquitetura final deste projeto diverge do vídeo (agente pandas em vez de RAG sobre PDF) pelos motivos explicados na seção [Por que agente pandas, e não RAG?](#arquitetura)
- **LangChain** — [documentação oficial](https://python.langchain.com/) do `create_pandas_dataframe_agent`
- **Google AI Studio** — [aistudio.google.com](https://aistudio.google.com/) — geração da chave de API do Gemini
