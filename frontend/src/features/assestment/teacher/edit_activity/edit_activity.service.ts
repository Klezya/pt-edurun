import configs from "@/core/configs"

export interface UpdateActivityData {
  titulo: string
  contenido: string
  test: string | null
}

export async function updateEvaluacion(evaluacionId: number, data: UpdateActivityData): Promise<any> {
  console.log('Actualizando evaluación:', evaluacionId, data)
  const response = await fetch(`${configs.apiBaseUrl}/api/evaluacion/${evaluacionId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data)
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Error al actualizar la evaluación' }))
    throw new Error(error.detail || 'Error al actualizar la evaluación')
  }

  return response.json()
}

export async function updateTarea(tareaId: number, data: UpdateActivityData): Promise<any> {
  console.log('Actualizando tarea:', tareaId, data)
  
  const response = await fetch(`${configs.apiBaseUrl}/api/tarea/${tareaId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data)
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Error al actualizar la tarea' }))
    throw new Error(error.detail || 'Error al actualizar la tarea')
  }

  return response.json()
}

export async function deleteEvaluacion(evaluacionId: number): Promise<any> {
  const response = await fetch(`${configs.apiBaseUrl}/api/evaluacion/${evaluacionId}`, {
    method: 'DELETE',
    headers: { 'Content-Type': 'application/json' }
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Error al eliminar la evaluación' }))
    throw new Error(error.detail || 'Error al eliminar la evaluación')
  }

  return response.json()
}

export async function deleteTarea(tareaId: number): Promise<any> {
  const response = await fetch(`${configs.apiBaseUrl}/api/tarea/${tareaId}`, {
    method: 'DELETE',
    headers: { 'Content-Type': 'application/json' }
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Error al eliminar la tarea' }))
    throw new Error(error.detail || 'Error al eliminar la tarea')
  }

  return response.json()
}
