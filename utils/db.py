# utils/db.py

import sqlite3
import os

DB_PATH = os.path.join("data", "treinador.db")

def conectar():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    return conn

def inicializar_banco():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id TEXT PRIMARY KEY,
            dados TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedbacks (
            usuario_id TEXT,
            data TEXT,
            tipo TEXT,
            sentimento TEXT,
            PRIMARY KEY (usuario_id, data, tipo)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS treinos_semana (
            usuario_id TEXT,
            data TEXT,
            treinos TEXT,
            PRIMARY KEY (usuario_id, data)
        )
    """)

    conn.commit()
    conn.close()
