#!/usr/bin/env python

import cgi
import cgitb
import pyodbc

cgitb.enable()  # Per il debug

# Funzione per connettersi al database
def connect_to_db():
    conn_str = (
        "DRIVER={MySQL ODBC 8.0 Driver};"
        "SERVER=localhost;"
        "DATABASE=nome_tuo_database;"
        "UID=tuo_username;"
        "PWD=tua_password;"
    )
    return pyodbc.connect(conn_str)

# Funzione per inserire un nuovo utente
def insert_user(nome, cognome, email):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "INSERT INTO UTENTI (nome, cognome, email) VALUES (?, ?, ?)"
    cursor.execute(query, (nome, cognome, email))
    conn.commit()
    cursor.close()
    conn.close()

# Genera il form HTML
def generate_form():
    print("Content-Type: text/html\n")
    print("""
    <html>
    <head>
        <title>Inserisci Utente</title>
    </head>
    <body>
        <h1>Inserisci un nuovo utente</h1>
        <form method="post" action="/cgi-bin/insert_user.py">
            Nome: <input type="text" name="nome"><br>
            Cognome: <input type="text" name="cognome"><br>
            Email: <input type="text" name="email"><br>
            <input type="submit" value="Inserisci">
        </form>
    </body>
    </html>
    """)

# Processa i dati del form
def process_form():
    form = cgi.FieldStorage()
    nome = form.getvalue("nome")
    cognome = form.getvalue("cognome")
    email = form.getvalue("email")

    if nome and cognome and email:
        insert_user(nome, cognome, email)
        print("Content-Type: text/html\n")
        print("<html><body><h1>Utente inserito con successo!</h1></body></html>")
    else:
        generate_form()

# Main
if __name__ == "__main__":
    if cgi.FieldStorage():
        process_form()
    else:
        generate_form()
