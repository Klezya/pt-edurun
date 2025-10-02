from fastapi import APIRouter

# Funciones para manejar los endpoints
from fastapi import Form

router = APIRouter()

@router.get("/health/")
async def health_check():
    return {"status": "ok"}

@router.get("/evaluaciones/")
async def read_evaluaciones():
    from functions.evaluaciones import get_evaluaciones
    return get_evaluaciones()

@router.get("/evaluaciones/{evaluacion_id}")
async def read_evaluacion(evaluacion_id: int):
    from functions.evaluaciones import get_evaluacion_by_id
    return get_evaluacion_by_id(evaluacion_id)

@router.post("/send-code/")
async def send_code(code: str = Form(...), evaluacion_id: int = Form(...)):
    from functions.containers import run_unittest_in_docker
    return run_unittest_in_docker(code, evaluacion_id)

@router.post("/run-code/")
async def run_code(code: str = Form(...)):
    from functions.containers import run_code_in_docker
    return run_code_in_docker(code)