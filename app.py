from flask import Flask, render_template, request, redirect
import csv
import os
from datetime import datetime

app = Flask(__name__)


# Função para salvar os dados no CSV
def salvar_dados(nome, nota1, nota2, nota3, media, status):
    arquivo_csv = "notas.csv"

    # Verifica se o arquivo já existe
    existe = os.path.isfile(arquivo_csv)

    with open(arquivo_csv, mode="a", newline="", encoding="utf8") as arquivo:
        escritor = csv.writer(arquivo)

        # Escreve o cabeçalho apenas se o arquivo for criado agora
        if not existe:
            escritor.writerow(["Nome", "Data", "Nota1", "Nota2", "Nota3", "Média", "Status"])

        # Captura a data atual
        data_atual = datetime.today().strftime("%d/%m/%Y")

        # Salva os dados no CSV ✅
        escritor.writerow([nome, data_atual, nota1, nota2, nota3, media, status])


# Rota principal (exibe o formulário e a lista de alunos)
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Pega os dados do formulário
        nome = request.form["nome"]
        nota1 = float(request.form["nota1"])
        nota2 = float(request.form["nota2"])
        nota3 = float(request.form["nota3"])

        # Calcula a média
        media = round((nota1 + nota2 + nota3) / 3, 2)
        status = "Aprovado! Parabéns!!" if media >= 7 else "Reprovado! Estude mais!"

        # Salva os dados no CSV
        salvar_dados(nome, nota1, nota2, nota3, media, status)

        return redirect("/")  # Recarrega a página após o cadastro

    # Carrega os alunos do CSV para exibir na tabela
    alunos = []
    try:
        with open("notas.csv", mode="r", encoding="utf8") as arquivo:
            leitor = csv.reader(arquivo)
            next(leitor)  # Pula o cabeçalho
            for linha in leitor:
                alunos.append(linha)
    except FileNotFoundError:
        pass  # Se o arquivo não existir, apenas ignora

    return render_template("index.html", alunos=alunos)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

