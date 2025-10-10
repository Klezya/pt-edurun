from fastapi import APIRouter
from models.lti import Usuario, Curso, Plataforma

router = APIRouter()

@router.get("/health/")
async def get_canvas_data():
    return {"status": "ok"}

@router.get("/course/{course_id_lms}")
async def get_course_by_lms_id(course_id_lms: str):
    from functions.lti import get_course_id_by_lms_id
    result = get_course_id_by_lms_id(course_id_lms)
    if result:
        return result
    return {"error": "Curso no encontrado"}

@router.post("/register_instance/")
async def register_lti_launch(usuario: Usuario, curso: Curso, plataforma: Plataforma):
    from functions.lti import register_lti_launch
    result = register_lti_launch(usuario, curso, plataforma)
    return result
