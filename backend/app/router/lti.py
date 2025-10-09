from fastapi import APIRouter
from models.lti import Usuario, Curso, Plataforma

router = APIRouter()

@router.get("/health/")
async def get_canvas_data():
    return {"status": "ok"}

@router.post("/register_instance/")
async def register_lti_launch(usuario: Usuario, curso: Curso, plataforma: Plataforma):
    from functions.lti import register_lti_launch
    result = register_lti_launch(usuario, curso, plataforma)
    return result
