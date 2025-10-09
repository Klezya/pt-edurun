const URL = 'https://edurunbackend.loca.lt/api'


export async function runCode(code: string): Promise<Response> {
    const body = new FormData()
    body.append('code', code)

    const res = await fetch(`${URL}/run-code/`, {
        method: 'POST',
        body: body,
    })
    return res
}

export async function sendCode(code: string, evaluacionId: number): Promise<Response> {
    const data = new FormData()
    data.append('code', code)
    data.append('evaluacion_id', evaluacionId.toString())

    const res = await fetch(`${URL}/send-code/`, {
        method: 'POST',
        body: data,
    })
    return res
}