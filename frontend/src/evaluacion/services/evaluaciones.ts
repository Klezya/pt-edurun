const URL = 'https://edurunbackend.loca.lt/api'

const LTIURL = 'https://kn3dxs-ip-190-101-201-29.tunnelmole.net'

export async function getEvaluacionesByCourseLmsId(courseId: string) {
  const result = await fetch(`${URL}/evaluaciones/${courseId}`).then(res => res.json())
  console.log('Evaluaciones del curso obtenidas:', result)
  return result
}

export async function getEvaluacion(id: number) {
  console.log('Fetching evaluacion with id:', id)
  const result = await fetch(`${URL}/evaluacion/${id}`).then(res => res.json())
  console.log('Evaluacion obtenida:', result)
  return result
}

export async function getTestCases(evaluacionId: number) {
  const result = await fetch(`${URL}/evaluacion/${evaluacionId}/test-cases`).then(res => res.json())
  console.log('Test cases obtenidos:', result)
  return result
}


export async function sendGrade(grade: number) {
  const ltik = sessionStorage.getItem('ltik')
  if (!ltik) throw new Error('Token LTI (ltik) no disponible')

  const res = await fetch(`${LTIURL}/grade`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${ltik}`,
        },
        body: JSON.stringify({ grade }),
    })
  return res
}