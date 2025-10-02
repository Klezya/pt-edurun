from functions.supabase import supabaseClient

def get_evaluaciones():
    response = (
        supabaseClient.table("evaluacion")
        .select("id, titulo, fecha_limite")
        .execute()
    )
    return response.data

def get_evaluacion_by_id(evaluacion_id: int):
    response = (
        supabaseClient.table("evaluacion")
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
        supabaseClient.table("evaluacion")
        .select("tests")
        .eq("id", evaluacion_id)
        .execute()
    )
    if response.data:
        return response.data[0]
    else:
        return None