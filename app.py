import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")

meses_ano = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # TODO: Add the user's entry into the database

        # Solicita e recebe do HTML os campos preenchidos
        # E os armazena em variáveis Python
        novo_nome = request.form.get("name")
        novo_dia = request.form.get("day")
        novo_mes = request.form.get("month")

        # converte mês número em mês texto
        i = 0
        for i in range (0, len(meses_ano)):
            if novo_mes == meses_ano[i]:
                break


        # insere o novo registo no banco de dados (com cuidado de "?" para evitar SQL injection)
        db.execute("INSERT INTO birthdays (name, month, day, month_text) VALUES (?, ?, ?, ?)",
        novo_nome, i, novo_dia, novo_mes)

        # recarrega a página (que irá atualizar a exibição dos aniversarios do banco)
        return redirect("/")

    else:

        # TODO: Exibir os registros do banco na página index.html

        # ler registros do banco de dados e gravar numa lista de dicionários
        registros_aniversarios = db.execute("SELECT * FROM birthdays ORDER BY month, day")
        # passar a lista de dicionários para o HTML e renderiza a página HTML

        return render_template("index.html", registros_aniversarios=registros_aniversarios)


@app.route("/deletar", methods=["POST"])
def deletar():

    # Solicita e recebe do HTML o id a ser apagado.
    # e armazena em variável Python
    id_apagar = request.form.get("id")

    # Apaga o registro enviado
    db.execute("DELETE FROM birthdays WHERE id = ?", id_apagar)

    # recarrega a página (que irá atualizar a exibição dos aniversarios do banco)
    return redirect("/")
