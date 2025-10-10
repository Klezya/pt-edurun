from pydantic import BaseModel
from typing import Optional

class Evaluacion(BaseModel):
    id_curso: int
    titulo: str
    contenido: str
    fecha_limite: Optional[str] = None
    test: Optional[str] = None
    fecha_registro: Optional[str] = None        