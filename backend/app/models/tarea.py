from pydantic import BaseModel
from typing import Optional

class Tarea(BaseModel):
    id_curso: int
    titulo: str
    contenido: str
    fecha_limite: Optional[str] = None
    test: Optional[str] = None
    fecha_registro: Optional[str] = None

class TareaUpdate(BaseModel):
    titulo: str
    contenido: str
    test: Optional[str] = None