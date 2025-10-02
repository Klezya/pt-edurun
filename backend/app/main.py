from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Edurun Python")

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "https://frontend.loca.lt",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
from router.evaluaciones import router as evaluaciones_router
from router.lti import router as lti_router

app.include_router(evaluaciones_router, prefix="/api")
app.include_router(lti_router, prefix="/lti")

