import json
import subprocess
import tempfile
import os

def lambda_handler(event, context):
    try:
        # Manejo flexible del body para diferentes formatos de event
        body = None
        
        # Caso 1: event tiene 'body' (API Gateway)
        if 'body' in event:
            body = event['body']
            if isinstance(body, str):
                try:
                    body = json.loads(body)
                except json.JSONDecodeError:
                    return {
                        "statusCode": 400,
                        "body": json.dumps({
                            "output": "",
                            "errors": "El body no es un JSON válido",
                            "results": {
                                "return_code": 1
                            }
                        })
                    }
        # Caso 2: event es directamente el body (invocación directa)
        elif 'code' in event:
            body = event
        # Caso 3: body vacío
        else:
            body = {}
    
        code = body.get('code', '') if body else ''
        

        if not code:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "output": "",
                    "errors": "No se proporcionó código para ejecutar",
                    "results": {
                        "return_code": 1
                    }
                })
            }
        
        # Crear un archivo temporal con el código
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            temp_file.write(code)
            temp_file_path = temp_file.name
        
        try:
            # Ejecutar el código Python
            result = subprocess.run(
                ['python3', temp_file_path],
                capture_output=True,
                text=True,
                timeout=30  # Timeout de 30 segundos para evitar ejecuciones infinitas
            )
            
            output = result.stdout
            errors = result.stderr
            return_code = result.returncode
            
        except subprocess.TimeoutExpired:
            output = ""
            errors = "Error: El código excedió el tiempo límite de ejecución (30 segundos)"
            return_code = 124
        
        except Exception as e:
            output = ""
            errors = f"Error al ejecutar el código: {str(e)}"
            return_code = 1
    
        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
        
        # Determinar el statusCode basado en el resultado de la ejecución
        status_code = 200 if return_code == 0 else 400
        
        return {
            "statusCode": status_code,
            "body": json.dumps({
                "output": output,
                "errors": errors,
                "results": {
                    "return_code": return_code
                }
            })
        }
    
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "output": "",
                "errors": f"Error en la función Lambda: {str(e)}",
                "results": {
                    "return_code": 1
                }
            })
        }  
