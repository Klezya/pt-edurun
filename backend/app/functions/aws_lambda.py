import httpx
import json
import asyncio
from typing import Dict, Any


async def execute_python_code(code: str) -> Dict[str, Any]:
    """
    Ejecuta código Python mediante la función Lambda de AWS.
    
    Args:
        code: Código Python a ejecutar
        
    Returns:
        Dict con la respuesta de la Lambda que contiene:
        - stdout: Salida estándar del código
        - stderr: Errores de ejecución
        - return_code: Código de retorno de la ejecución
        
    Raises:
        httpx.HTTPError: Si hay un error en la comunicación con la API
    """
    url = "https://psvg354cic.execute-api.us-east-1.amazonaws.com/default/CodeRun"
    
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


def execute_python_code_sync(code: str) -> Dict[str, Any]:
    """
    Versión síncrona: Ejecuta código Python mediante la función Lambda de AWS.
    
    Args:
        code: Código Python a ejecutar
        
    Returns:
        Dict con la respuesta de la Lambda que contiene:
        - stdout: Salida estándar del código
        - stderr: Errores de ejecución
        - return_code: Código de retorno de la ejecución
        
    Raises:
        httpx.HTTPError: Si hay un error en la comunicación con la API
    """
    url = "https://psvg354cic.execute-api.us-east-1.amazonaws.com/default/CodeRun"
    
    payload = {
        "code": code
    }
    
    with httpx.Client(timeout=35.0) as client:
        response = client.post(url, json=payload)
        response.raise_for_status()
        
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

if __name__ == "__main__":
    sample_code = 'print("Hello from AWS Lambda!")'
    
    # Probar versión async
    async def test_async():
        print("=== Probando versión async ===")
        result = await execute_python_code(sample_code)
        print(result)
        print("stdout:", result.get("stdout"))
        print("stderr:", result.get("stderr"))
        print("return_code:", result.get("return_code"))
        return result
    
    # Ejecutar la función async
    result = asyncio.run(test_async())
    
    # También probar versión sync
    print("\n=== Probando versión sync ===")
    result_sync = execute_python_code_sync(sample_code)
    print(result_sync)
    print("stdout:", result_sync.get("stdout"))
    print("stderr:", result_sync.get("stderr"))
    print("return_code:", result_sync.get("return_code"))