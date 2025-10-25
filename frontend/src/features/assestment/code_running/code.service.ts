import configs from '@/core/configs'

export async function runCode(code: string): Promise<Response> {
    const body = new FormData()
    body.append('code', code)

    const res = await fetch(`${configs.apiBaseUrl}/api/run-code/`, {
        method: 'POST',
        body: body,
    })
    return res
}

export async function sendCode(code: string, evaluacionId: number): Promise<Response> {
    const data = new FormData()
    data.append('code', code)
    data.append('evaluacion_id', evaluacionId.toString())

    const res = await fetch(`${configs.apiBaseUrl}/api/send-code/`, {
        method: 'POST',
        body: data,
    })
    return res
}

export async function sendGrade(grade: number) {
  const ltik = sessionStorage.getItem('ltik')
  if (!ltik) throw new Error('Token LTI (ltik) no disponible')

  const res = await fetch(`${configs.ltiBaseUrl}/grade`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${ltik}`,
        },
        body: JSON.stringify({ grade }),
    })
  return res
}

export async function runTareaTests(code: string, tareaId: number): Promise<Response> {
    const data = new FormData()
    data.append('code', code)
    data.append('tarea_id', tareaId.toString())

    const res = await fetch(`${configs.apiBaseUrl}/api/run-tarea-test/`, {
        method: 'POST',
        body: data,
    })
    return res
}

export async function runEvaluacionTests(code: string, evaluacionId: number): Promise<Response> {
    const data = new FormData()
    data.append('code', code)
    data.append('evaluacion_id', evaluacionId.toString())

    const res = await fetch(`${configs.apiBaseUrl}/api/run-evaluacion-test/`, {
        method: 'POST',
        body: data,
    })
    return res
}