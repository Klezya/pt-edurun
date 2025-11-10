import httpx
import json
from typing import Dict, Any

from settings import LAMBDA_API_URL

async def execute_python_code(code: str) -> Dict[str, Any]:

    url = f"{LAMBDA_API_URL}/CodeRun"

    payload = {
        "code": code
    }
    
    async with httpx.AsyncClient(timeout=35.0) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        
        # La respuesta tiene estructura: {'statusCode': 200, 'body': '{"output": ..., "errors": ..., "results": {...}}'}
        lambda_response = response.json()
        
        # Parsear el body que viene como string JSON
        if 'body' in lambda_response and isinstance(lambda_response['body'], str):
            body = json.loads(lambda_response['body'])
        else:
            body = lambda_response
        
        # Retornar en el formato esperado
        return {
            "stdout": body.get("output", ""),
            "stderr": body.get("errors", ""),
            "return_code": body.get("results", {}).get("return_code", 1)
        }


async def _execute_code_with_test(code: str, test: str) -> Dict[str, Any]:
      
    url = f"{LAMBDA_API_URL}/EdurunCodeTestTarea"
    
    payload = {
        "code": code,
        "test": test
    }
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, json=payload)
            
            
            lambda_response = response.json()
            
            # Parsear el body que viene como string JSON
            if 'body' in lambda_response and isinstance(lambda_response['body'], str):
                body = json.loads(lambda_response['body'])
            else:
                body = lambda_response
            
            # Retornar en el formato esperado (incluso si el código del usuario falló)
            return {
                "stdout": body.get("stdout", ""),
                "stderr": body.get("stderr", ""),
                "return_code": body.get("return_code", 1)
            }
    except Exception as e:
        return {
            "stdout": "",
            "stderr": f"Error inesperado: {str(e)}",
            "return_code": 1
        }


async def execute_code_test(code: str, tarea_id: int) -> Dict[str, Any]:
    from functions.tareas import get_tarea_test
    
    # Obtener el test de la tarea desde la base de datos
    tarea_data = get_tarea_test(tarea_id)
    
    if not tarea_data or not tarea_data.get("test"):
        return {
            "stdout": "",
            "stderr": "No se encontró el test para la tarea especificada",
            "return_code": 1
        }
    
    test = tarea_data.get("test")
    return await _execute_code_with_test(code, test)


async def execute_code_test_evaluacion(code: str, evaluacion_id: int) -> Dict[str, Any]:
    from functions.evaluaciones import get_evaluacion_test
    
    # Obtener el test de la evaluación desde la base de datos
    evaluacion_data = get_evaluacion_test(evaluacion_id)
    if not evaluacion_data or not evaluacion_data.get("test"):
        return {
            "stdout": "",
            "stderr": "No se encontró el test para la evaluación especificada",
            "return_code": 1
        }
    
    test = evaluacion_data.get("test")
    return await _execute_code_with_test(code, test)


async def evaluate_activity(code: str, evaluacion_id: int) -> Dict[str, Any]:
    """
    Evalúa una actividad (evaluación) y extrae el puntaje obtenido.
    Similar a execute_code_test_evaluacion pero retorna también el score.
    """
    import re
    from functions.evaluaciones import get_evaluacion_test
    
    # Obtener el test de la evaluación desde la base de datos
    evaluacion_data = get_evaluacion_test(evaluacion_id)
    if not evaluacion_data or not evaluacion_data.get("test"):
        return {
            "score": 0,
            "stdout": "",
            "stderr": "No se encontró el test para la evaluación especificada",
            "return_code": 1
        }
    
    test = evaluacion_data.get("test")
    result = await _execute_code_with_test(code, test)
    
    # Extraer el puntaje del output
    score = 0
    output = result.get("stdout", "")
    
    score_match = re.search(r'Puntaje obtenido: (\d+)%', output)
    if score_match:
        score = int(score_match.group(1))
    
    # Retornar con el score incluido
    return {
        "score": score,
        "stdout": result.get("stdout", ""),
        "stderr": result.get("stderr", ""),
        "return_code": result.get("return_code", 1)
    }

