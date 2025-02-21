from flask import Flask, render_template, request, redirect
import psycopg2
import os
from datetime import datetime

app = Flask(__name__)

# Configurações do banco de dados a partir das variáveis de ambiente
db_config = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

# Função para conectar ao banco de dados
def get_db_connection():
    return psycopg2.connect(**db_config)

# Criar a tabela caso não exista
def criar_tabela():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS notas (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            data DATE NOT NULL,
            nota1 NUMERIC(4,2) NOT NULL,
            nota2 NUMERIC(4,2) NOT NULL,
            nota3 NUMERIC(4,2) NOT NULL,
            media NUMERIC(4,2) NOT NULL,
            status VARCHAR(50) NOT NULL
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

# Rota principal (exibe o formulário e a lista de alunos)
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nome = request.form["nome"]
        nota1 = float(request.form["nota1"])
        nota2 = float(request.form["nota2"])
        nota3 = float(request.form["nota3"])
        media = round((nota1 + nota2 + nota3) / 3, 2)
        status = "Aprovado! Parabéns!!" if media >= 7 else "Reprovado! Estude mais!"
        data_atual = datetime.today().strftime("%Y-%m-%d")

        # Salvar no banco de dados
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO notas (nome, data, nota1, nota2, nota3, media, status) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (nome, data_atual, nota1, nota2, nota3, media, status)
        )
        conn.commit()
        cur.close()
        conn.close()

        return redirect("/")

    # Recuperar os alunos do banco de dados
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT nome, data, nota1, nota2, nota3, media, status FROM notas")
    alunos = cur.fetchall()
    cur.close()
    conn.close()

    return render_template("index.html", alunos=alunos)

if __name__ == "__main__":
    criar_tabela()  # Garante que a tabela existe antes de rodar o app
    app.run(host="0.0.0.0", port=5000)
