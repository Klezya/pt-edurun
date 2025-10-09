from pydantic import BaseModel
from typing import Optional


class Usuario(BaseModel):
    id_lms: str
    nombre: Optional[str] = None

class Curso(BaseModel):
    nombre: str 
    etiqueta: Optional[str] = None
    id_curso_lms: str
    id_plataforma: int

class Plataforma(BaseModel):
    guid: str
    nombre: str
    version: Optional[str] = None
    family_code: Optional[str] = None



# Modelo para el registro completo LTI Launch
class LTILaunchData(BaseModel):
    # Datos del usuario
    user_id_lms: str
    user_name: Optional[str] = None
    
    # Datos del curso
    course_id_lms: str
    course_name: str
    course_label: Optional[str] = None
    
    # Datos de la plataforma
    platform_guid: str
    platform_name: str
    platform_version: Optional[str] = None
    platform_family_code: Optional[str] = None
    