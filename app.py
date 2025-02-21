from flask import Flask, render_template, request, redirect
import psycopg2
from psycopg2 import sql
from datetime import datetime

# Configuração do banco de dados
DATABASE_URL = "postgresql://webnotas_db_user:N7UDcn6sFyO7wtmLyJpqA4hssOYHvzAx@dpg-cus768a1jk6c73f1k000-a/webnotas_db"

# Criar conexão com o banco
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# Criar a tabela se não existir
cur.execute("""
    CREATE TABLE IF NOT EXISTS notas (
        id SERIAL PRIMARY KEY,
        nome TEXT,
        data TEXT,
        nota1 FLOAT,
        nota2 FLOAT,
        nota3 FLOAT,
        media FLOAT,
        status TEXT
    )
""")
conn.commit()

app = Flask(__name__)

# Função para salvar os dados no PostgreSQL
def salvar_dados(nome, nota1, nota2, nota3, media, status):
    data_atual = datetime.today().strftime("%d/%m/%Y")
    cur.execute("INSERT INTO notas (nome, data, nota1, nota2, nota3, media, status) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (nome, data_atual, nota1, nota2, nota3, media, status))
    conn.commit()

# Rota principal
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nome = request.form["nome"]
        nota1 = float(request.form["nota1"])
        nota2 = float(request.form["nota2"])
        nota3 = float(request.form["nota3"])

        media = round((nota1 + nota2 + nota3) / 3, 2)
        status = "Aprovado! Parabéns!!" if media >= 7 else "Reprovado! Estude mais!"

        salvar_dados(nome, nota1, nota2, nota3, media, status)
        return redirect("/")

    # Buscar dados do PostgreSQL para exibir na página
    cur.execute("SELECT nome, data, nota1, nota2, nota3, media, status FROM notas")
    alunos = cur.fetchall()

    return render_template("index.html", alunos=alunos)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

