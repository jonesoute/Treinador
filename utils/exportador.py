# utils/exportador.py

import os
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
import xml.dom.minidom
import xml.etree.ElementTree as ET

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

def exportar_treino_para_tcx(usuario_id, treino, nome_arquivo=None):
    import xml.etree.ElementTree as ET
    from xml.dom import minidom

    if not nome_arquivo:
        nome_arquivo = f"{treino['tipo'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.tcx"

    sport = "Running" if treino["modalidade"] == "Corrida" else "Biking"

    tcx = ET.Element("TrainingCenterDatabase", {
        "xmlns": "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2",
        "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "xsi:schemaLocation": "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2 "
                              "http://www.garmin.com/xmlschemas/TrainingCenterDatabasev2.xsd"
    })

    workouts = ET.SubElement(tcx, "Workouts")
    workout = ET.SubElement(workouts, "Workout", Sport=sport)
    ET.SubElement(workout, "Name").text = treino["tipo"]

    # ETAPA 1 – Aquecimento
    step1 = ET.SubElement(workout, "Step")
    ET.SubElement(step1, "Name").text = "Aquecimento"
    ET.SubElement(step1, "Duration").set("xsi:type", "Time_t")
    ET.SubElement(step1, "Duration").text = "600"
    ET.SubElement(step1, "Intensity").text = "Warmup"
    hr1 = ET.SubElement(step1, "HeartRate")
    ET.SubElement(hr1, "HeartRateZone").text = "1"

    # ETAPA 2 – Intervalos com alvo
    for i in range(5):
        step = ET.SubElement(workout, "Step")
        ET.SubElement(step, "Name").text = f"Intervalo {i+1}"
        ET.SubElement(step, "Duration").set("xsi:type", "Time_t")
        ET.SubElement(step, "Duration").text = "240"
        ET.SubElement(step, "Intensity").text = "Active"

        # FC alvo
        fc_target = ET.SubElement(step, "Target")
        ET.SubElement(fc_target, "HeartRateZone").text = "4"

        # Simulação de potência em Notas
        ET.SubElement(step, "Notes").text = "Simular 90-100% FTP (Z4)"

        # Recuperação
        rest = ET.SubElement(workout, "Step")
        ET.SubElement(rest, "Name").text = f"Recuperação {i+1}"
        ET.SubElement(rest, "Duration").set("xsi:type", "Time_t")
        ET.SubElement(rest, "Duration").text = "180"
        ET.SubElement(rest, "Intensity").text = "Resting"
        hr2 = ET.SubElement(rest, "Target")
        ET.SubElement(hr2, "HeartRateZone").text = "2"

    # ETAPA 3 – Cooldown
    stepf = ET.SubElement(workout, "Step")
    ET.SubElement(stepf, "Name").text = "Cooldown"
    ET.SubElement(stepf, "Duration").set("xsi:type", "Time_t")
    ET.SubElement(stepf, "Duration").text = "600"
    ET.SubElement(stepf, "Intensity").text = "Cooldown"
    ET.SubElement(ET.SubElement(stepf, "Target"), "HeartRateZone").text = "1"

    # Salvar arquivo
    xml_str = minidom.parseString(ET.tostring(tcx)).toprettyxml(indent="  ")
    pasta_saida = os.path.join("data", "usuarios", usuario_id, "exportados")
    os.makedirs(pasta_saida, exist_ok=True)

    caminho = os.path.join(pasta_saida, nome_arquivo)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(xml_str)

    return caminho
