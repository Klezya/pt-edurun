import configs from '@/core/configs'

export async function getEvaluacionesByCourseLmsId(courseId: string) {
  const result = await fetch(`${configs.apiBaseUrl}/api/evaluaciones/${courseId}`).then(res => res.json())
  console.log('Evaluaciones del curso obtenidas:', result)
  return result
}

export async function getTareasByCourseLmsId(courseId: string) {
  const result = await fetch(`${configs.apiBaseUrl}/api/tareas/${courseId}`).then(res => res.json())
  console.log('Tareas del curso obtenidas:', result)
  return result
}

export async function getTestCases(evaluacionId: number) {
  const result = await fetch(`${configs.apiBaseUrl}/api/evaluacion/${evaluacionId}/test-cases`).then(res => res.json())
  console.log('Test cases obtenidos:', result)
  return result
}

export async function getEvaluacion(id: number) {
  console.log('Fetching evaluacion with id:', id)
  const result = await fetch(`${configs.apiBaseUrl}/api/evaluacion/${id}`).then(res => res.json())
  console.log('Evaluacion obtenida:', result)
  return result
}

export async function getTarea(id: number) {
  console.log('Fetching tarea with id:', id)
  const result = await fetch(`${configs.apiBaseUrl}/api/tarea/${id}`).then(res => res.json())
  console.log('Tarea obtenida:', result)
  return result
}

