# Imagem oficial do Python, variante "slim": só o essencial pra rodar
# Python, sem as ferramentas de build que a imagem completa carrega.
# Deixa a imagem final bem menor.
FROM python:3.14-slim

# Todo comando daqui pra baixo roda dentro dessa pasta, dentro do container.
WORKDIR /app

# Copia só o requirements.txt primeiro e instala as dependências antes de
# copiar o resto do código. Isso é cache de camada do Docker: se só o
# código em src/ mudar depois, o Docker reaproveita essa camada de
# instalação em vez de baixar tudo de novo a cada build.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código-fonte e os dados para dentro da imagem.
COPY src/ src/
COPY data/ data/

# Comando executado quando o container sobe.
CMD ["python", "src/main.py"]
