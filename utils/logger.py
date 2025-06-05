# utils/logger.py

import os
import logging
from datetime import datetime

# Garante que o diretório de logs existe
os.makedirs("logs", exist_ok=True)

# Configura o logger principal
logging.basicConfig(
    filename="logs/app.log",
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def registrar_erro(mensagem):
    """
    Registra uma mensagem de erro no arquivo de log.
    """
    logging.error(mensagem)

def registrar_alerta(mensagem):
    """
    Registra um alerta leve (não erro crítico).
    """
    logging.warning(mensagem)

def registrar_info(mensagem):
    """
    Registra uma informação útil (como login bem-sucedido, etc).
    """
    logging.info(mensagem)
