import { getCourseInfo } from "@/features/lti_protocol"
import { getCourseIdByLmsId } from "@/features/assestment/shared/course.service"
import type { CreateActivityData } from "./create_activity.type"
import configs from "@/core/configs"

export async function createEvaluacion(data: Omit<CreateActivityData, 'id_curso'>): Promise<any> {
  const courseInfo = await getCourseInfo()
  const courseDbInfo = await getCourseIdByLmsId(courseInfo.id)
  
  if ('error' in courseDbInfo) {
    throw new Error(courseDbInfo.error)
  }
  
  const payload: CreateActivityData = {
    id_curso: courseDbInfo.id,
    ...data
  }
  console.log('Payload para crear evaluación:', payload)
  const response = await fetch(`${configs.apiBaseUrl}/api/evaluacion`, {
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


export async function createTarea(data: Omit<CreateActivityData, 'id_curso'>): Promise<any> {
  const courseInfo = await getCourseInfo()
  const courseDbInfo = await getCourseIdByLmsId(courseInfo.id)

  if ('error' in courseDbInfo) {
    throw new Error(courseDbInfo.error)
  }
  
  const payload: CreateActivityData = {
    id_curso: courseDbInfo.id,
    ...data
  }
  console.log('Payload para crear tarea:', payload)
  const response = await fetch(`${configs.apiBaseUrl}/api/tarea`, {
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
