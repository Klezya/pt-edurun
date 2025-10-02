const URL = 'https://fastapilti.loca.lt'


export async function getEvaluaciones() {
  const result = await fetch(`${URL}/evaluaciones`).then(res => res.json())
  console.log('Evaluaciones obtenidas:', result)
  return result
}

export async function getEvaluacion(id: number) {
  const result = await fetch(`${URL}/evaluaciones/${id}`).then(res => res.json())
  console.log('Evaluacion obtenida:', result)
  return result
}

export async function getTestCases(evaluacionId: number) {
  const result = await fetch(`${URL}/evaluaciones/${evaluacionId}/test-cases`).then(res => res.json())
  console.log('Test cases obtenidos:', result)
  return result
}