from fastapi import APIRouter

# Funciones para manejar los endpoints
from fastapi import Form
from models.evaluacion import EntregaEvaluacion, Evaluacion, EvaluacionUpdate
from models.tarea import Tarea, TareaUpdate

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

@router.put("/evaluacion/{evaluacion_id}")
async def update_evaluacion(evaluacion_id: int, evaluacion: EvaluacionUpdate):
    from functions.evaluaciones import update_evaluacion
    response = update_evaluacion(evaluacion_id, evaluacion)
    return response

@router.post("/evaluacion/entrega/")
async def submit_evaluacion(entrega: EntregaEvaluacion):
    from functions.evaluaciones import create_or_update_entrega_evaluacion
    response = create_or_update_entrega_evaluacion(entrega)
    return response

@router.get("/evaluacion/entrega/")
async def get_entregas_evaluacion(user_id_lms: str,evaluacion_id: int):
    from functions.evaluaciones import get_entrega_evaluacion
    response = get_entrega_evaluacion(user_id_lms,evaluacion_id)
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

@router.put("/tarea/{tarea_id}")
async def update_tarea(tarea_id: int, tarea: TareaUpdate):
    from functions.tareas import update_tarea
    response = update_tarea(tarea_id, tarea)
    return response

# Delete endpoints
@router.delete("/evaluacion/{evaluacion_id}")
async def delete_evaluacion(evaluacion_id: int):
    from functions.evaluaciones import delete_evaluacion
    response = delete_evaluacion(evaluacion_id)
    return response

@router.delete("/tarea/{tarea_id}")
async def delete_tarea(tarea_id: int):
    from functions.tareas import delete_tarea
    response = delete_tarea(tarea_id)
    return response

# Containers endpoints

'''
@router.post("/send-code/")
async def send_code(code: str = Form(...), evaluacion_id: int = Form(...)):
    from functions.containers import evaluate_activity
    return evaluate_activity(code, evaluacion_id)

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
'''

# AWS Lambda endpoints
@router.post("/run-code/")
async def run_code_lambda(code: str = Form(...)):
    from functions.aws_lambda import execute_python_code
    return await execute_python_code(code)

@router.post("/run-tarea-test/")
async def run_tarea_test_lambda(code: str = Form(...), tarea_id: int = Form(...)):
    from functions.aws_lambda import execute_code_test
    return await execute_code_test(code, tarea_id)

@router.post("/run-evaluacion-test/")
async def run_evaluacion_test_lambda(code: str = Form(...), evaluacion_id: int = Form(...)):
    from functions.aws_lambda import execute_code_test_evaluacion
    return await execute_code_test_evaluacion(code, evaluacion_id)

@router.post("/evaluate-activity/")
async def evaluate_activity_lambda(code: str = Form(...), evaluacion_id: int = Form(...)):
    from functions.aws_lambda import evaluate_activity
    return await evaluate_activity(code, evaluacion_id)