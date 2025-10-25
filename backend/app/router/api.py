from fastapi import APIRouter

# Funciones para manejar los endpoints
from fastapi import Form
from models.evaluacion import Evaluacion
from models.tarea import Tarea

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

@router.post("/evaluacion/")
async def create_evaluacion(evaluacion: Evaluacion):
    from functions.evaluaciones import create_evaluacion
    response = create_evaluacion(evaluacion)
    return response

# tareas

@router.get("/tareas/{course_id_lms}")
async def read_tareas(course_id_lms: str):
    from functions.tareas import get_tareas_by_course_lms_id
    return get_tareas_by_course_lms_id(course_id_lms)

@router.get("/tarea/{tarea_id}")
async def read_tarea(tarea_id: int):
    from functions.tareas import get_tarea_by_id
    return get_tarea_by_id(tarea_id)

@router.post("/tarea/")
async def create_tarea(tarea: Tarea):
    from functions.tareas import create_tarea
    response = create_tarea(tarea)
    return response

# pendings

@router.post("/send-code/")
async def send_code(code: str = Form(...), evaluacion_id: int = Form(...)):
    # from functions.containers import run_unittest_in_docker
    # return run_unittest_in_docker(code, evaluacion_id)
    return {"message": "Funcionalidad pendiente de implementación"}

@router.post("/run-code/")
async def run_code(code: str = Form(...)):
    from functions.containers import run_code_in_docker
    return run_code_in_docker(code)

@router.post("/run-tarea-test/")
async def run_test(code: str = Form(...), tarea_id: int = Form(...)):
    from functions.containers import run_tarea_unittest_in_docker
    return run_tarea_unittest_in_docker(code, tarea_id)

@router.post("/run-evaluacion-test/")
async def run_evaluacion_test(code: str = Form(...), evaluacion_id: int = Form(...)):
    from functions.containers import run_evaluacion_unittest_in_docker
    return run_evaluacion_unittest_in_docker(code, evaluacion_id)