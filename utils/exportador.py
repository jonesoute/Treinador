# utils/exportador.py

import os
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
import xml.dom.minidom

def exportar_treino_para_zwo(usuario_id, treino, nome_arquivo=None):
    """
    Exporta um treino para o formato .ZWO (Zwift Workout XML)
    treino = {
        "modalidade": "Ciclismo",
        "tipo": "Intervalado",
        "descricao": "Aquecimento 10min + 5x4min Z4 com 3min Z2 entre + cooldown",
        "zona": "Z2-Z4",
        "tempo": 60
    }
    """
    if not nome_arquivo:
        nome_arquivo = f"{treino['tipo'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.zwo"

    treino_xml = Element('workout_file')
    name = SubElement(treino_xml, 'name')
    name.text = treino["tipo"]

    author = SubElement(treino_xml, 'author')
    author.text = "Treinador Virtual IA"

    description = SubElement(treino_xml, 'description')
    description.text = treino["descricao"]

    workout = SubElement(treino_xml, 'workout')

    # Exemplo simples: aquecimento + blocos + cooldown
    # Em versões futuras podemos transformar texto em blocos automáticos

    # Aquecimento
    SubElement(workout, 'SteadyState', attrib={
        'Duration': '600',
        'PowerLow': '0.5',
        'PowerHigh': '0.6'
    })

    # Blocos (5x4min)
    for _ in range(5):
        SubElement(workout, 'SteadyState', attrib={
            'Duration': '240',
            'PowerLow': '0.9',
            'PowerHigh': '1.0'
        })
        SubElement(workout, 'SteadyState', attrib={
            'Duration': '180',
            'PowerLow': '0.6',
            'PowerHigh': '0.7'
        })

    # Cooldown
    SubElement(workout, 'SteadyState', attrib={
        'Duration': '600',
        'PowerLow': '0.5',
        'PowerHigh': '0.6'
    })

    xml_str = xml.dom.minidom.parseString(tostring(treino_xml)).toprettyxml(indent="  ")

    pasta_saida = os.path.join("data", "usuarios", usuario_id, "exportados")
    os.makedirs(pasta_saida, exist_ok=True)

    caminho_completo = os.path.join(pasta_saida, nome_arquivo)
    with open(caminho_completo, "w", encoding="utf-8") as f:
        f.write(xml_str)

    return caminho_completo

