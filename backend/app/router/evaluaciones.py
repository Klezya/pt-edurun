from fastapi import APIRouter

# Funciones para manejar los endpoints
from fastapi import Form

router = APIRouter()

@router.get("/health/")
async def health_check():
    return {"status": "ok"}

# evaluaciones

@router.get("/evaluaciones/{course_id_lms}")
async def read_evaluaciones(course_id_lms: str):
    from functions.evaluaciones import get_evaluaciones_by_course_lms_id
    return get_evaluaciones_by_course_lms_id(course_id_lms)

@router.get("/evaluacion/{evaluacion_id}")
async def read_evaluacion(evaluacion_id: int):
    from functions.evaluaciones import get_evaluacion_by_id
    return get_evaluacion_by_id(evaluacion_id)

# tareas

@router.get("/tareas/{course_id_lms}")
async def read_tareas(course_id_lms: str):
    from functions.tareas import get_tareas_by_course_lms_id
    return get_tareas_by_course_lms_id(course_id_lms)

@router.get("/tarea/{tarea_id}")
async def read_tarea(tarea_id: int):
    from functions.tareas import get_tarea_by_id
    return get_tarea_by_id(tarea_id)

# pendings

@router.post("/send-code/")
async def send_code(code: str = Form(...), evaluacion_id: int = Form(...)):
    from functions.containers import run_unittest_in_docker
    return run_unittest_in_docker(code, evaluacion_id)

@router.post("/run-code/")
async def run_code(code: str = Form(...)):
    from functions.containers import run_code_in_docker
    return run_code_in_docker(code)