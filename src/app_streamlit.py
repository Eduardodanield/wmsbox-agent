import pandas as pd
import streamlit as st

import agente_estoque

# Letra no lugar de emoji no favicon/título.
st.set_page_config(page_title="wmsbox-agent", page_icon="A")

st.title("Agente de Estoque")
st.caption(
    "Faça perguntas em linguagem natural sobre o estoque de eletrônicos. "
    "O agente traduz a pergunta em código pandas e calcula a resposta em cima do CSV real."
)

# Guarda o df/agente ativos e o histórico do chat entre reexecuções do script.
if "df_ativo" not in st.session_state:
    st.session_state.df_ativo = agente_estoque.df
    st.session_state.agente_ativo = agente_estoque.agente
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

with st.sidebar:
    st.subheader("Estoque")

    if st.checkbox("Ver estoque atual"):
        if st.session_state.df_ativo is not None:
            st.dataframe(st.session_state.df_ativo, use_container_width=True)
        else:
            st.info("Nenhum estoque carregado ainda.")

    st.divider()

    st.subheader("Importar outro estoque")
    st.caption(
        "O arquivo precisa ter exatamente as mesmas colunas do modelo "
        "atual (sku, produto, tipo, fisico_atual, etc.)."
    )
    arquivo_novo = st.file_uploader("Escolher CSV", type="csv", label_visibility="collapsed")

    if arquivo_novo is not None:
        novo_df = pd.read_csv(arquivo_novo, encoding="utf-8-sig")

        if list(novo_df.columns) != agente_estoque.COLUNAS_ESPERADAS:
            st.error(
                "Esse CSV não está no formato esperado. As colunas precisam ser, "
                "nesta ordem: " + ", ".join(agente_estoque.COLUNAS_ESPERADAS)
            )
        else:
            # Só recria o agente se o CSV mudou de verdade.
            if not novo_df.equals(st.session_state.df_ativo):
                st.session_state.df_ativo = novo_df
                st.session_state.agente_ativo = agente_estoque.criar_agente(novo_df)
                st.session_state.mensagens = []
            st.success(f"Estoque atualizado: {len(novo_df)} produtos carregados.")

    st.divider()

    st.subheader("Exemplos de pergunta")
    exemplos = [
        "Qual o valor total em estoque?",
        "Quantos produtos estão com estoque físico zerado?",
        "Quais os 5 produtos com maior estoque geral?",
        "Quantas unidades do produto WMS-0001 temos?",
    ]
    for exemplo in exemplos:
        if st.button(exemplo, use_container_width=True):
            st.session_state["pergunta_pendente"] = exemplo

if st.session_state.agente_ativo is None:
    st.info("Nenhum estoque carregado ainda. Importe um CSV na barra lateral para começar.")
else:
    # Reexibe o histórico do chat.
    for autor, texto in st.session_state.mensagens:
        with st.chat_message(autor):
            st.markdown(texto)

    # Botão de exemplo clicado também vira pergunta.
    pergunta = st.chat_input("Digite sua pergunta sobre o estoque...")
    if "pergunta_pendente" in st.session_state:
        pergunta = st.session_state.pop("pergunta_pendente")

    if pergunta:
        st.session_state.mensagens.append(("user", pergunta))
        with st.chat_message("user"):
            st.markdown(pergunta)

        with st.chat_message("assistant"):
            with st.spinner("Consultando o estoque..."):
                resposta = st.session_state.agente_ativo.invoke({"input": pergunta})
                st.markdown(resposta["output"])
        st.session_state.mensagens.append(("assistant", resposta["output"]))
