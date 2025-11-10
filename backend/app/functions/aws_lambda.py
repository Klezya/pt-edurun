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
    """
    Función interna para ejecutar código con tests usando Lambda.
    Reutilizable para tareas y evaluaciones.
    """
    # Validar que code y test no estén vacíos
    if not code or not code.strip():
        return {
            "stdout": "",
            "stderr": "El código no puede estar vacío",
            "return_code": 1
        }
    
    if not test or not test.strip():
        return {
            "stdout": "",
            "stderr": "El test no puede estar vacío",
            "return_code": 1
        }
    
    url = f"{LAMBDA_API_URL}/EdurunCodeTestTarea"
    
    payload = {
        "code": code,
        "test": test
    }
    
    # Debug: imprimir el payload
    print(f"[DEBUG] Enviando a Lambda: {url}")
    print(f"[DEBUG] Payload keys: code={len(code)} chars, test={len(test)} chars")
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, json=payload)
            
            print(f"[DEBUG] Lambda HTTP status: {response.status_code}")
            print(f"[DEBUG] Lambda response: {response.text[:500]}")
            
            # API Gateway siempre retorna 200 si Lambda se ejecutó
            # El statusCode dentro del body es el resultado de la ejecución
            if response.status_code != 200:
                return {
                    "stdout": "",
                    "stderr": f"Error de API Gateway (HTTP {response.status_code}): {response.text}",
                    "return_code": 1
                }
            
            # La respuesta tiene estructura: {'statusCode': 200/400, 'body': '{"stdout": ..., "stderr": ..., "return_code": ...}'}
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
    except httpx.HTTPStatusError as e:
        print(f"[ERROR] HTTP Status Error: {e}")
        print(f"[ERROR] Response: {e.response.text}")
        return {
            "stdout": "",
            "stderr": f"Error HTTP {e.response.status_code}: {e.response.text}",
            "return_code": 1
        }
    except Exception as e:
        print(f"[ERROR] Exception: {str(e)}")
        return {
            "stdout": "",
            "stderr": f"Error inesperado: {str(e)}",
            "return_code": 1
        }


async def execute_code_test(code: str, tarea_id: int) -> Dict[str, Any]:
    from functions.tareas import get_tarea_test
    
    print(f"[DEBUG] execute_code_test - tarea_id: {tarea_id}")
    
    # Obtener el test de la tarea desde la base de datos
    tarea_data = get_tarea_test(tarea_id)
    
    print(f"[DEBUG] tarea_data: {tarea_data}")
    
    if not tarea_data or not tarea_data.get("test"):
        return {
            "stdout": "",
            "stderr": "No se encontró el test para la tarea especificada",
            "return_code": 1
        }
    
    test = tarea_data.get("test")
    print(f"[DEBUG] test obtenido, longitud: {len(test) if test else 0} chars")
    
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

