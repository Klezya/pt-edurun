from fastapi import FastAPI, UploadFile, Form, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from api.db import get_evaluacion_test
from containers.service import run_code_in_docker, run_unittest_in_docker

app = FastAPI(title="Edurun Python")

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "https://dithionous-unautomatically-cheri.ngrok-free.dev",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/evaluaciones/")
async def read_evaluaciones():
    from api.db import get_evaluaciones
    return get_evaluaciones()

@app.get("/evaluaciones/{evaluacion_id}")
async def read_evaluacion(evaluacion_id: int):
    from api.db import get_evaluacion_by_id
    return get_evaluacion_by_id(evaluacion_id)

@app.post("/send-code/")
async def send_code(code: str = Form(...), evaluacion_id: int = Form(...)):
    return run_unittest_in_docker(code, evaluacion_id)

@app.post("/run-code/")
async def run_code(code: str = Form(...)):
    return run_code_in_docker(code)
