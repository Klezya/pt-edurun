from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from settings import FRONTEND_URL

app = FastAPI(title="Edurun Python")

origins = [
    "http://localhost",
    "http://127.0.0.1",
    FRONTEND_URL,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
from router.api import router as evaluaciones_router
from router.lti import router as lti_router

app.include_router(evaluaciones_router, prefix="/api")
app.include_router(lti_router, prefix="/lti")

