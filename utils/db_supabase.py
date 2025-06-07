from supabase import create_client, Client
import os
from datetime import datetime

SUPABASE_URL = "https://jdzbdgejsnkmzcvfpxym.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpkemJkZ2Vqc25rbXpjdmZweHltIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDkzMDEzOTYsImV4cCI6MjA2NDg3NzM5Nn0.ftE3LXY_LeEeP6WnDSLPjc8oTM7s-9B-q683sZTe54w"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def salvar_perfil(usuario_id: str, perfil: dict):
    perfil["id"] = usuario_id
    perfil["data_criacao"] = perfil.get("data_criacao", datetime.utcnow().isoformat())

    existing = supabase.table("usuarios").select("id").eq("id", usuario_id).execute()
    if existing.data:
        supabase.table("usuarios").update(perfil).eq("id", usuario_id).execute()
    else:
        supabase.table("usuarios").insert(perfil).execute()

def carregar_perfil(usuario_id: str):
    result = supabase.table("usuarios").select("*").eq("id", usuario_id).single().execute()
    return result.data if result.data else None

def perfil_existe(usuario_id: str):
    result = supabase.table("usuarios").select("id").eq("id", usuario_id).execute()
    return bool(result.data)
