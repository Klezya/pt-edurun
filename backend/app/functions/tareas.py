from functions.supabase import supabaseClient

def get_tareas_by_course_lms_id(course_id_lms: str):
    from functions.lti import get_course_id_by_lms_id
    course_id = get_course_id_by_lms_id(course_id_lms).get("id")
    response = (
        supabaseClient.table("tarea")
        .select("id, titulo")
        .eq("id_curso", course_id)
        .execute()
    )
    return response.data

def get_tarea_by_id(tarea_id: int):
    response = (
        supabaseClient.table("tarea")
        .select("id, titulo, contenido, test")
        .eq("id", tarea_id)
        .execute()
    )
    return response.data[0]

def get_tarea_test(tarea_id: int):
    response = (
        supabaseClient.table("tarea")
        .select("test")
        .eq("id", tarea_id)
        .execute()
    )
    if response.data:
        return response.data[0]
    else:
        return None

# Metodos Post
from models.tarea import Tarea, TareaUpdate

def create_tarea(tarea: Tarea):
    response = (
        supabaseClient.table("tarea")
        .insert({"id_curso": tarea.id_curso,
                 "titulo": tarea.titulo,
                 "contenido": tarea.contenido,
                 "fecha_limite": tarea.fecha_limite,
                 "test": tarea.test})
        .execute()
    )
    return response.data

def update_tarea(tarea_id: int, tarea: TareaUpdate):
    response = (
        supabaseClient.table("tarea")
        .update({"titulo": tarea.titulo,
                 "contenido": tarea.contenido,
                 "test": tarea.test})
        .eq("id", tarea_id)
        .execute()
    )
    return response.data