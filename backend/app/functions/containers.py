import subprocess
import uuid
import os
from fastapi.responses import JSONResponse

SCRIPTS_DIR = "/tmp/scripts"
os.makedirs(SCRIPTS_DIR, exist_ok=True)

def run_code_in_docker(code: str):
    file_id = str(uuid.uuid4())
    script_path = os.path.join(SCRIPTS_DIR, f"{file_id}.py")
    
    with open(script_path, "w") as f:
        try:
            f.write(code)
        except Exception as e:
            return JSONResponse(content={"error": "Error al escribir el script"}, status_code=500)

    # 2. Ejecutar el código dentro de un contenedor Docker
    cmd = [
        "docker", "run", "--rm",
        "-m", "128m", "--cpus=0.5",  # límites de recursos
        "-v", f"{script_path}:/app/script.py:ro",  # montar archivo
        "python:3.11-slim",
        "python", "/app/script.py"
    ]

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=10
        )
    except subprocess.TimeoutExpired:
        return JSONResponse(content={"error": "Tiempo de ejecución excedido"}, status_code=408)

    output = result.stdout
    errors = result.stderr

    return {
        "stdout": output,
        "stderr": errors,
        "return_code": result.returncode
    }

def run_evaluacion_unittest_in_docker(code: str, evaluacion_id: int):
    from functions.evaluaciones import get_evaluacion_test
    test = get_evaluacion_test(evaluacion_id).get("test")
    
    user_file_id = str(uuid.uuid4())
    test_file_id = str(uuid.uuid4())
    user_script_path = os.path.join(SCRIPTS_DIR, f"{user_file_id}.py")
    test_script_path = os.path.join(SCRIPTS_DIR, f"{test_file_id}_test.py")
    

    with open(user_script_path, "w") as f:
        try:
            f.write(code)
        except Exception as e:
            return JSONResponse(content={"error": "Error al escribir el script del usuario"}, status_code=500)

    with open(test_script_path, "w") as f:
        try:
            f.write(test)
        except Exception as e:
            return JSONResponse(content={"error": "Error al escribir el script de prueba"}, status_code=500)

    cmd = [
        "docker", "run", "--rm",
        "-m", "256m", "--cpus=1",
        "-v", f"{user_script_path}:/app/app.py:ro",
        "-v", f"{test_script_path}:/app/test_code.py:ro",
        "edurun-pytest:latest",
        "python", "-m", "pytest", "-q", "/app/test_code.py"
    ]

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=30
        )
    except subprocess.TimeoutExpired:
        return JSONResponse(content={"error": "Tiempo de ejecución excedido"}, status_code=408)

    output = result.stdout
    errors = result.stderr

    return {
        "stdout": output,
        "stderr": errors,
        "return_code": result.returncode
    }
    
def run_tarea_unittest_in_docker(code: str, tarea_id: int):
    from functions.tareas import get_tarea_test
    test = get_tarea_test(tarea_id).get("test")
    
    user_file_id = str(uuid.uuid4())
    test_file_id = str(uuid.uuid4())
    user_script_path = os.path.join(SCRIPTS_DIR, f"{user_file_id}.py")
    test_script_path = os.path.join(SCRIPTS_DIR, f"{test_file_id}_test.py")
    

    with open(user_script_path, "w") as f:
        try:
            f.write(code)
        except Exception as e:
            return JSONResponse(content={"error": "Error al escribir el script del usuario"}, status_code=500)

    with open(test_script_path, "w") as f:
        try:
            f.write(test)
        except Exception as e:
            return JSONResponse(content={"error": "Error al escribir el script de prueba"}, status_code=500)

    cmd = [
        "docker", "run", "--rm",
        "-m", "256m", "--cpus=1",
        "-v", f"{user_script_path}:/app/app.py:ro",
        "-v", f"{test_script_path}:/app/test_code.py:ro",
        "edurun-pytest:latest",
        "python", "-m", "pytest", "-q", "/app/test_code.py"
    ]

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=30
        )
    except subprocess.TimeoutExpired:
        return JSONResponse(content={"error": "Tiempo de ejecución excedido"}, status_code=408)

    output = result.stdout
    errors = result.stderr

    return {
        "stdout": output,
        "stderr": errors,
        "return_code": result.returncode
    }