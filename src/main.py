from agente_estoque import agente

# Digitar qualquer uma dessas palavras encerra o loop de conversa.
COMANDOS_SAIDA = {"sair", "exit", "quit"}


def main():
    print("=" * 60)
    print("Agente de Estoque - wmsbox-agent")
    print("Pergunte algo sobre o estoque (ex: 'qual o valor total em estoque?')")
    print(f"Digite '{'/'.join(COMANDOS_SAIDA)}' para encerrar.")
    print("=" * 60)

    while True:
        try:
            pergunta = input("\nVocê: ").strip()
        except (KeyboardInterrupt, EOFError):
            # Sai limpo em Ctrl+C/Ctrl+D, sem traceback.
            print("\nAté mais!")
            break

        if not pergunta:
            continue

        if pergunta.lower() in COMANDOS_SAIDA:
            print("Até mais!")
            break

        try:
            resposta = agente.invoke({"input": pergunta})
            print(f"\nAgente: {resposta['output']}")
        except Exception as erro:
            # Erro de API não deve derrubar o programa inteiro.
            print(f"\nOcorreu um erro ao consultar o agente: {erro}")


if __name__ == "__main__":
    main()
