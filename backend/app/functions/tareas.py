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
        .select("id, titulo, contenido")
        .eq("id", tarea_id)
        .execute()
    )
    return response.data[0]

def get_tarea_test(tarea_id: int):
    response = (
        supabaseClient.table("tarea")
        .select("tests")
        .eq("id", tarea_id)
        .execute()
    )
    if response.data:
        return response.data[0]
    else:
        return None