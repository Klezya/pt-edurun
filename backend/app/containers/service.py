import subprocess
import tempfile
import uuid
import os
from fastapi.responses import JSONResponse

SCRIPTS_DIR = "/tmp/scripts"
os.makedirs(SCRIPTS_DIR, exist_ok=True)

def run_code_in_docker(code: str):
    file_id = str(uuid.uuid4())
    script_path = os.path.join(SCRIPTS_DIR, f"{file_id}.py")
    
    with open(script_path, "w") as f:
        f.write(code)

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

def run_unittest_in_docker(code: str, evaluacion_id: int):
    from api.db import get_evaluacion_test
    test = get_evaluacion_test(evaluacion_id).get("tests")
    
    user_file_id = str(uuid.uuid4())
    test_file_id = str(uuid.uuid4())
    user_script_path = os.path.join(SCRIPTS_DIR, f"{user_file_id}.py")
    test_script_path = os.path.join(SCRIPTS_DIR, f"{test_file_id}_test.py")
    
    with open(user_script_path, "w") as f:
        f.write(code)
    
    with open(test_script_path, "w") as f:
        f.write(test)

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
    