import { getCourseInfo } from "../../lti/services/info"
import { getCourseIdByLmsId } from "../../lti/services/lti_fastapi"

// URL base para las APIs
const API_URL = 'https://edurunbackend.loca.lt'

// Interfaz para los datos de creación
export interface CreateEvaluacionTareaData {
  id_curso: number
  titulo: string
  contenido: string
  fecha_limite: string | null
  test: string | null
}

/**
 * Crea una nueva evaluación en el sistema
 * @param data Datos de la evaluación a crear
 * @returns Respuesta del servidor con la evaluación creada
 */
export async function createEvaluacion(data: Omit<CreateEvaluacionTareaData, 'id_curso'>): Promise<any> {

  // Obtener el ID del curso LMS desde el servicio LTI
  const courseInfo = await getCourseInfo()
  
  // Obtener el ID de la base de datos del curso usando el ID del LMS
  const courseDbInfo = await getCourseIdByLmsId(courseInfo.id)
  
  if ('error' in courseDbInfo) {
    throw new Error(courseDbInfo.error)
  }
  
  const payload: CreateEvaluacionTareaData = {
    id_curso: courseDbInfo.id,
    ...data
  }
  console.log('Payload para crear evaluación:', payload)
  const response = await fetch(`${API_URL}/api/evaluacion`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload)
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Error al crear la evaluación' }))
    throw new Error(error.detail || 'Error al crear la evaluación')
  }

  return response.json()
}

/**
 * Crea una nueva tarea en el sistema
 * @param data Datos de la tarea a crear
 * @returns Respuesta del servidor con la tarea creada
 */
export async function createTarea(data: Omit<CreateEvaluacionTareaData, 'id_curso'>): Promise<any> {

  // Obtener el ID del curso LMS desde el servicio LTI
  const courseInfo = await getCourseInfo()
  
  // Obtener el ID de la base de datos del curso usando el ID del LMS
  const courseDbInfo = await getCourseIdByLmsId(courseInfo.id)
  
  if ('error' in courseDbInfo) {
    throw new Error(courseDbInfo.error)
  }
  
  const payload: CreateEvaluacionTareaData = {
    id_curso: courseDbInfo.id,
    ...data
  }
  console.log('Payload para crear tarea:', payload)
  const response = await fetch(`${API_URL}/api/tarea`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload)
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Error al crear la tarea' }))
    throw new Error(error.detail || 'Error al crear la tarea')
  }

  return response.json()
}
