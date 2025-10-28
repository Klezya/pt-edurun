from functions.supabase import supabaseClient


def get_evaluaciones_by_course_lms_id(course_id_lms: str):
    from functions.lti import get_course_id_by_lms_id
    course_id = get_course_id_by_lms_id(course_id_lms).get("id")
    response = (
        supabaseClient.table("evaluacion")
        .select("id, titulo, fecha_limite")
        .eq("id_curso", course_id)
        .execute()
    )
    return response.data

def get_evaluacion_by_id(evaluacion_id: int):
    response = (
        supabaseClient.table("evaluacion")
        .select("id, titulo, fecha_limite, contenido, test")
        .eq("id", evaluacion_id)
        .execute()
    )
    return response.data[0]

def get_evaluacion_test(evaluacion_id: int):
    response = (
        supabaseClient.table("evaluacion")
        .select("test")
        .eq("id", evaluacion_id)
        .execute()
    )
    if response.data:
        return response.data[0]
    else:
        return None
    
# Metodos Post
from models.evaluacion import Evaluacion, EvaluacionUpdate

def create_evaluacion(evaluacion: Evaluacion):
    response = (
        supabaseClient.table("evaluacion")
        .insert({"id_curso": evaluacion.id_curso,
                 "titulo": evaluacion.titulo,
                 "contenido": evaluacion.contenido,
                 "fecha_limite": evaluacion.fecha_limite,
                 "test": evaluacion.test})
        .execute()
    )
    return response.data

def update_evaluacion(evaluacion_id: int, evaluacion: EvaluacionUpdate):
    response = (
        supabaseClient.table("evaluacion")
        .update({"titulo": evaluacion.titulo,
                 "contenido": evaluacion.contenido,
                 "test": evaluacion.test})
        .eq("id", evaluacion_id)
        .execute()
    )
    return response.data