# utils/exportador.py

import os
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
import xml.dom.minidom
from utils.logger import registrar_erro

def exportar_treino_para_zwo(usuario_id, treino, nome_arquivo=None):
    try:
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

        # Aquecimento
        SubElement(workout, 'SteadyState', attrib={
            'Duration': '600',
            'PowerLow': '0.5',
            'PowerHigh': '0.6'
        })

        # Blocos (5x4min Z4 + 3min Z2)
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
    except Exception as e:
        registrar_erro(f"Erro ao exportar treino ZWO para '{usuario_id}': {e}")
        return None

def exportar_treino_para_tcx(usuario_id, treino, nome_arquivo=None):
    try:
        import xml.etree.ElementTree as ET
        from xml.dom import minidom

        if not nome_arquivo:
            nome_arquivo = f"{treino['tipo'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.tcx"

        sport = "Running" if treino["modalidade"] == "Corrida" else "Biking"

        tcx = ET.Element("TrainingCenterDatabase", {
            "xmlns": "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2",
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "xsi:schemaLocation": "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2 http://www.garmin.com/xmlschemas/TrainingCenterDatabasev2.xsd"
        })

        workouts = ET.SubElement(tcx, "Workouts")
        workout = ET.SubElement(workouts, "Workout", Sport=sport)
        ET.SubElement(workout, "Name").text = treino["tipo"]

        # Aquecimento
        step1 = ET.SubElement(workout, "Step")
        ET.SubElement(step1, "Name").text = "Aquecimento"
        dur1 = ET.SubElement(step1, "Duration", {"xsi:type": "Time_t"})
        dur1.text = "600"
        ET.SubElement(step1, "Intensity").text = "Warmup"
        hr1 = ET.SubElement(step1, "Target")
        ET.SubElement(hr1, "HeartRateZone").text = "1"

        # Intervalos + Recuperações
        for i in range(5):
            step = ET.SubElement(workout, "Step")
            ET.SubElement(step, "Name").text = f"Intervalo {i+1}"
            dur = ET.SubElement(step, "Duration", {"xsi:type": "Time_t"})
            dur.text = "240"
            ET.SubElement(step, "Intensity").text = "Active"
            fc_target = ET.SubElement(step, "Target")
            ET.SubElement(fc_target, "HeartRateZone").text = "4"
            ET.SubElement(step, "Notes").text = "Simular 90-100% FTP (Z4)"

            rest = ET.SubElement(workout, "Step")
            ET.SubElement(rest, "Name").text = f"Recuperação {i+1}"
            dur2 = ET.SubElement(rest, "Duration", {"xsi:type": "Time_t"})
            dur2.text = "180"
            ET.SubElement(rest, "Intensity").text = "Resting"
            hr2 = ET.SubElement(rest, "Target")
            ET.SubElement(hr2, "HeartRateZone").text = "2"

        # Cooldown
        stepf = ET.SubElement(workout, "Step")
        ET.SubElement(stepf, "Name").text = "Cooldown"
        durf = ET.SubElement(stepf, "Duration", {"xsi:type": "Time_t"})
        durf.text = "600"
        ET.SubElement(stepf, "Intensity").text = "Cooldown"
        hrf = ET.SubElement(ET.SubElement(stepf, "Target"), "HeartRateZone")
        hrf.text = "1"

        xml_str = minidom.parseString(ET.tostring(tcx)).toprettyxml(indent="  ")

        pasta_saida = os.path.join("data", "usuarios", usuario_id, "exportados")
        os.makedirs(pasta_saida, exist_ok=True)

        caminho = os.path.join(pasta_saida, nome_arquivo)
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(xml_str)

        return caminho
    except Exception as e:
        registrar_erro(f"Erro ao exportar treino TCX para '{usuario_id}': {e}")
        return None
