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


def delete_evaluacion(evaluacion_id: int):
    response = (
        supabaseClient.table("evaluacion")
        .delete()
        .eq("id", evaluacion_id)
        .execute()
    )
    return response.data

from models.evaluacion import EntregaEvaluacion

def create_entrega_evaluacion(entrega_data: EntregaEvaluacion):
    from functions.lti import get_user_id_by_lms_id
    user = get_user_id_by_lms_id(entrega_data.id_alumno)
    user_id = user.get("id")
    response = (
        supabaseClient.table("entrega_evaluacion")
        .insert({"id_evaluacion": entrega_data.id_evaluacion,
                 "id_alumno": user_id,
                 "nota": entrega_data.nota,
                 "codigo": entrega_data.codigo,
                 "detalles": entrega_data.detalles})
        .execute()
    )
    return response.data

def update_entrega_evaluacion(entrega_data: EntregaEvaluacion):
    from functions.lti import get_user_id_by_lms_id
    user = get_user_id_by_lms_id(entrega_data.id_alumno)
    user_id = user.get("id")
    response = (
        supabaseClient.table("entrega_evaluacion")
        .update({"nota": entrega_data.nota,
                 "codigo": entrega_data.codigo,
                 "detalles": entrega_data.detalles})
        .eq("id_alumno", user_id)
        .eq("id_evaluacion", entrega_data.id_evaluacion)
        .execute()
    )
    return response.data

def get_entrega_evaluacion(user_id_lms: str, evaluacion_id: int):
    from functions.lti import get_user_id_by_lms_id
    user = get_user_id_by_lms_id(user_id_lms)
    user_id = user.get("id")
    response = (
        supabaseClient.table("entrega_evaluacion")
        .select("*")
        .eq("id_alumno", user_id)
        .eq("id_evaluacion", evaluacion_id)
        .execute()
    )
    if response.data:
        return response.data[0]
    else:
        return None

def create_or_update_entrega_evaluacion(entrega_data: EntregaEvaluacion):
    existing_entrega = get_entrega_evaluacion(entrega_data.id_alumno, entrega_data.id_evaluacion)
    if existing_entrega:
        return update_entrega_evaluacion(entrega_data)
    else:
        return create_entrega_evaluacion(entrega_data)