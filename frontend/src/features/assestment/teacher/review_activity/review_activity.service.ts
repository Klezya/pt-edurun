import configs from '@/core/configs'
import type { EntregaEvaluacionResponse } from '@/features/assestment/teacher/review_activity/review_activity.types'


export interface EntregaEvaluacionRequest {
  user_id_lms: string
  evaluacion_id: number
}

export async function getEntregaEvaluacion(
  userId: string, 
  evaluacionId: number
): Promise<EntregaEvaluacionResponse | null> {
  try {
    const requestBody: EntregaEvaluacionRequest = {
      user_id_lms: userId,
      evaluacion_id: evaluacionId
    }

    const response = await fetch(
      `${configs.apiBaseUrl}/api/evaluacion/entrega/`,
      {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody)
      }
    )

    if (!response.ok) {
      if (response.status === 404) {
        return null
      }
      const error = await response.json().catch(() => ({ 
        detail: 'Error al obtener la entrega' 
      }))
      throw new Error(error.detail || 'Error al obtener la entrega')
    }

    const data = await response.json()
    return data
  } catch (error) {
    console.error('Error al obtener la entrega:', error)
    throw error
  }
}
