# utils/treino_generator.py

import os
import json
from datetime import date, timedelta, datetime
from utils.analysis import preparar_dataframe_atividades, calcular_cargas
from components.calendar import carregar_provas
from utils.perfil import carregar_perfil
from utils.logger import registrar_erro

def salvar_treinos_semana(usuario_id, treinos):
    try:
        caminho = os.path.join("data", "usuarios", usuario_id, "treinos_semana.json")
        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(treinos, f, ensure_ascii=False, indent=4)
    except Exception as e:
        registrar_erro(f"Erro ao salvar treinos da semana para '{usuario_id}': {e}")

def carregar_feedbacks(usuario_id):
    try:
        caminho = os.path.join("data", "usuarios", usuario_id, "feedbacks.json")
        if os.path.exists(caminho):
            with open(caminho, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    except Exception as e:
        registrar_erro(f"Erro ao carregar feedbacks do usuário '{usuario_id}': {e}")
        return {}

def ajustar_carga_por_feedback(usuario_id):
    feedbacks = carregar_feedbacks(usuario_id)
    hoje = date.today()
    ultima_semana = [hoje - timedelta(days=i) for i in range(1, 8)]

    valores_rpe = {
        "Muito fácil": 1,
        "Fácil": 2,
        "Moderado": 3,
        "Difícil": 4,
        "Exaustivo": 5
    }

    rpes = []
    for fb in feedbacks.values():
        data_fb = datetime.fromisoformat(fb["data"]).date()
        if data_fb in ultima_semana:
            rpes.append(valores_rpe.get(fb["sentimento"], 3))

    if not rpes:
        return 0, True

    media = sum(rpes) / len(rpes)
    if media <= 2.0:
        return +1, False
    elif media >= 4.0:
        return -1, False
    else:
        return 0, False

def obter_fase_treinamento(usuario_id):
    try:
        perfil = carregar_perfil(usuario_id)
        data_inicio = perfil.get("data_criacao", date.today().isoformat())
        data_inicio = datetime.fromisoformat(data_inicio).date()
        hoje = date.today()
        semanas = (hoje - data_inicio).days // 7

        provas = carregar_provas(usuario_id)
        provas_ordenadas = sorted(provas, key=lambda p: p["data_inicio"])
        if provas_ordenadas:
            data_prova = datetime.fromisoformat(provas_ordenadas[0]["data_inicio"]).date()
            semanas_ate_prova = (data_prova - hoje).days // 7

            if semanas_ate_prova <= 1:
                return "taper"
            elif semanas_ate_prova <= 3:
                return "pre-prova"

        if semanas < 4:
            return "base"
        elif semanas < 8:
            return "especifica"
        elif semanas < 10:
            return "pre-prova"
        else:
            return "transicao"

    except Exception as e:
        registrar_erro(f"Erro ao determinar fase de treinamento de '{usuario_id}': {e}")
        return "base"

def ajustar_para_competicoes(plano, usuario_id):
    try:
        provas = carregar_provas(usuario_id)
        hoje = date.today()

        for prova in provas:
            data_inicio = datetime.fromisoformat(prova["data_inicio"]).date()
            data_fim = datetime.fromisoformat(prova["data_fim"]).date()
            dias_competicao = (data_fim - data_inicio).days + 1

            for i in range(dias_competicao):
                dia = data_inicio + timedelta(days=i)
                key = dia.isoformat()
                plano[key] = [{
                    "modalidade": prova["tipo"],
                    "tipo": "🏁 Dia de Competição",
                    "descricao": f"{prova['nome']} - {prova['distancia_km']} km / {prova.get('altimetria_m', 0)} m de altimetria.",
                    "zona": "Competição",
                    "tempo": 0,
                    "fase": "competicao"
                }]

            for dias_antes in range(1, 4):
                dia_taper = data_inicio - timedelta(days=dias_antes)
                key = dia_taper.isoformat()
                if key in plano:
                    for treino in plano[key]:
                        treino["tipo"] = "Taper pré-prova"
                        treino["descricao"] = f"Redução de volume antes da prova ({treino['descricao']})"
                        treino["zona"] = "Z1-Z2"
                        treino["fase"] = "taper"

            dia_pos = data_fim + timedelta(days=1)
            key = dia_pos.isoformat()
            if key in plano:
                plano[key] = [{
                    "modalidade": prova["tipo"],
                    "tipo": "Regenerativo pós-prova",
                    "descricao": "Atividade leve para acelerar recuperação",
                    "zona": "Z1",
                    "tempo": 30,
                    "fase": "transicao"
                }]

        return plano

    except Exception as e:
        registrar_erro(f"Erro ao ajustar treinos para competições de '{usuario_id}': {e}")
        return plano

def adicionar_dicas_nutricao(treino, perfil):
    try:
        peso = perfil.get("peso", 70)
        tempo = treino.get("tempo", 60)
        intensidade = treino.get("zona", "Z2")

        carbo_min = 30
        carbo_max = 90 if "Z4" in intensidade or "Z5" in intensidade else 60
        liquido_ml = 500 if tempo < 90 else 750
        sodio_mg = 500 if tempo >= 90 else 300

        treino["nutricao"] = {
            "carbo": f"{carbo_min}-{carbo_max}g/h",
            "agua": f"{liquido_ml}ml/h",
            "sodio": f"~{sodio_mg}mg/l"
        }
        return treino
    except Exception as e:
        registrar_erro(f"Erro ao adicionar dicas de nutrição para treino: {e}")
        return treino

def gerar_semana_treinos(usuario_id):
    try:
        perfil = carregar_perfil(usuario_id)
        modalidades = perfil.get("modalidades", ["Ciclismo"])
        dias_disponiveis = perfil.get("dias_disponiveis", [])
        horas_disponiveis = perfil.get("horas_disponiveis", {})
        ftp = perfil.get("ftp", 200)

        df = preparar_dataframe_atividades(usuario_id, ftp)
        sem_atividades = df.empty

        if sem_atividades:
            cargas = {"ATL": 0, "CTL": 0, "TSB": 10}  # assume bem descansado
        else:
            cargas = calcular_cargas(df)

        fase = obter_fase_treinamento(usuario_id)
        ajuste_feedback, sem_feedback = ajustar_carga_por_feedback(usuario_id)

        hoje = date.today()
        plano = {}

        if sem_feedback:
            plano["_mensagem"] = (
                "⚠️ Você não registrou nenhum feedback nos últimos 7 dias. "
                "A intensidade dos treinos será mantida sem ajustes automáticos. "
                "Responder aos feedbacks permite que o plano se adapte melhor ao seu corpo e evolução."
            )

        if sem_atividades:
            plano["_mensagem"] = (
                "ℹ️ Você ainda não possui treinos registrados no sistema. "
                "Foi gerado um plano de transição leve com base no seu perfil."
            )

        for i in range(7):
            dia = hoje + timedelta(days=i)
            nome_dia = dia.strftime("%A")
            if nome_dia not in dias_disponiveis:
                continue

            tempo_max = horas_disponiveis.get(nome_dia, 1.0)
            tipo_treino = "leve" if cargas["TSB"] < -10 else "moderado" if cargas["TSB"] < 10 else "intenso"

            if fase == "base" and tipo_treino == "intenso":
                tipo_treino = "moderado"
            elif fase in ["taper", "transicao"]:
                tipo_treino = "leve"

            if ajuste_feedback == +1 and tipo_treino == "moderado":
                tipo_treino = "intenso"
            elif ajuste_feedback == -1 and tipo_treino == "intenso":
                tipo_treino = "moderado"
            elif ajuste_feedback == -1 and tipo_treino == "moderado":
                tipo_treino = "leve"

            if sem_atividades:
                tipo_treino = "leve"

            plano[dia.isoformat()] = []
            for modalidade in modalidades:
                if modalidade == "Ciclismo":
                    treino = gerar_treino_ciclismo(tipo_treino, tempo_max, fase)
                elif modalidade == "Corrida":
                    treino = gerar_treino_corrida(tipo_treino, tempo_max, fase)
                treino = adicionar_dicas_nutricao(treino, perfil)
                plano[dia.isoformat()].append(treino)

        plano = ajustar_para_competicoes(plano, usuario_id)
        salvar_treinos_semana(usuario_id, plano)
        return plano

    except Exception as e:
        registrar_erro(f"Erro ao gerar plano semanal para '{usuario_id}': {e}")
        return {}
