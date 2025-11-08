from functions.supabase import supabaseClient

# Funciones get

def get_platform_id_by_guid(platform_guid: str):
    response = ( supabaseClient.table("plataforma")
    .select("id")
    .eq("guid", platform_guid)
    .execute()
    )
    return response.data[0] if response.data else None

def get_user_id_by_lms_id(user_id_lms: str):
    response = ( supabaseClient.table("usuario")
    .select("id")
    .eq("id_lms", user_id_lms)
    .execute()
    )
    return response.data[0] if response.data else None

def get_course_id_by_lms_id(course_id_lms: str):
    response = ( supabaseClient.table("curso")
    .select("id")
    .eq("id_curso_lms", course_id_lms)
    .execute()
    )
    return response.data[0] if response.data else None

def get_user_in_course(user_id: int, course_id: int):
    response = ( supabaseClient.table("curso_usuario")
    .select("*")
    .eq("id_usuario", user_id)
    .eq("id_curso", course_id)
    .execute()
    )
    return response.data[0] if response.data else None

# Funciones post

from models.lti import Plataforma, Usuario, Curso

def register_platform(plataforma: Plataforma):
    response = ( supabaseClient.table("plataforma")
    .insert({"guid": plataforma.guid,
             "nombre": plataforma.nombre,
             "version": plataforma.version,
             "family_code": plataforma.family_code})
    .execute()
    )
    return response.data

def register_user(usuario: Usuario):
    response = ( supabaseClient.table("usuario")
    .insert({"id_lms": usuario.id_lms,
             "nombre": usuario.nombre})
    .execute()
    )
    return response.data

def register_course(curso: Curso):
    response = ( supabaseClient.table("curso")
    .insert({"nombre": curso.nombre,
             "etiqueta": curso.etiqueta,
             "id_curso_lms": curso.id_curso_lms,
             "id_plataforma": curso.id_plataforma})
    .execute()
    )
    return response.data

def enroll_user_in_course(user_id: int, course_id: int):
    response = ( supabaseClient.table("curso_usuario")
    .insert({"id_usuario": user_id,
             "id_curso": course_id})
    .execute()
    )
    return response.data

# Launch completo

def register_lti_launch(
        usuario: Usuario,
        curso: Curso,
        plataforma: Plataforma,
):
    platform_state = None
    course_state = None
    user_state = None
    enrollment_state = None

    try:
        # Verificar/Registrar Plataforma
        platform = get_platform_id_by_guid(plataforma.guid)
        if not platform:
            platform_data = register_platform(plataforma)
            platform = platform_data[0] if platform_data else None
            platform_state = "registered"
        else:
            platform_state = "existing"
        
        platform_id = platform.get('id')
        curso.id_plataforma = platform_id 
        
        # Verificar/Registrar Curso
        course = get_course_id_by_lms_id(curso.id_curso_lms)
        if not course:
            print(f"Curso no encontrado. Registrando curso: {curso.nombre}")
            course_data = register_course(curso)
            course = course_data[0] if course_data else None
            course_state = "registered"
        else:
            course_state = "existing"
        
        course_id = course.get('id')
        
        # Verificar/Registrar Usuario
        user = get_user_id_by_lms_id(usuario.id_lms)
        if not user:
            print(f"Usuario no encontrado. Registrando usuario: {usuario.nombre}")
            user_data = register_user(usuario)
            user = user_data[0] if user_data else None
            user_state = "registered"
        else:
            user_state = "existing"
        
        user_id = user.get('id')
        
        is_enrolled = get_user_in_course(user_id, course_id)
        if not is_enrolled:
            enrollment = enroll_user_in_course(user_id, course_id)
            enrollment_state = "registered"
        else:
            enrollment_state = "existing"
        
        return {
            "success": True,
            "data": {
                "plataforma": platform_state,
                "curso": course_state,
                "usuario": user_state,
                "enrolacion": enrollment_state
            },
            "message": "Registro LTI completado exitosamente"
        }
        
    except Exception as e:
        print(f"Error en register_lti_launch: {str(e)}")
        return {
            "success": False,
            "message": f"Error al procesar el registro LTI: {str(e)}",
            "data": None
        }