import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client("https://znduweqofbxljoivufcr.supabase.co", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpuZHV3ZXFvZmJ4bGpvaXZ1ZmNyIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NjM5NDg0MCwiZXhwIjoyMDcxOTcwODQwfQ.0nI7uj-ToMF1wI_eF44R0aQisE8CnS7cGsrBHKFh4aM")

def get_evaluaciones():
    response = (
        supabase.table("evaluacion")
        .select("id, titulo, fecha_limite")
        .execute()
    )
    return response.data

def get_evaluacion_by_id(evaluacion_id: int):
    response = (
        supabase.table("evaluacion")
        .select("id, titulo, fecha_limite, contenido")
        .eq("id", evaluacion_id)
        .execute()
    )
    if response.data:
        return response.data[0]
    else:
        return None

def get_evaluacion_test(evaluacion_id: int):
    response = (
        supabase.table("evaluacion")
        .select("tests")
        .eq("id", evaluacion_id)
        .execute()
    )
    if response.data:
        return response.data[0]
    else:
        return None