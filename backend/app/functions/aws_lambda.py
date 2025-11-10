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


async def execute_tarea_test(code: str, tarea_id: int) -> Dict[str, Any]:
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
    
    url = f"{LAMBDA_API_URL}/TestTarea"
    
    payload = {
        "code": code,
        "test": test
    }
    
    async with httpx.AsyncClient(timeout=35.0) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        
        # La respuesta tiene estructura: {'statusCode': 200, 'body': '{"stdout": ..., "stderr": ..., "return_code": ...}'}
        lambda_response = response.json()
        
        # Parsear el body que viene como string JSON
        if 'body' in lambda_response and isinstance(lambda_response['body'], str):
            body = json.loads(lambda_response['body'])
        else:
            body = lambda_response
        
        # Retornar en el formato esperado (mismo que el Docker)
        return {
            "stdout": body.get("stdout", ""),
            "stderr": body.get("stderr", ""),
            "return_code": body.get("return_code", 1)
        }

