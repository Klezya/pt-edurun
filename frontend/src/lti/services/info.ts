import type { CourseInfo, PlatformInfo, UserInfo } from "../interfaces/info"

const URL = 'https://dithionous-unautomatically-cheri.ngrok-free.dev'

// Obtiene la información completa del usuario desde el endpoint /info
export async function getUserInfo(): Promise<UserInfo> {
    const ltik = sessionStorage.getItem('ltik')
    if (!ltik) throw new Error('Token LTI (ltik) no disponible')

    const res = await fetch(`${URL}/info/user`, {
        method: 'GET',
        headers: {
            'ngrok-skip-browser-warning': 'any',
            'Authorization': `Bearer ${ltik}`,
        },
    })

    const data = await res.json()
    return data
}

export async function getCourseInfo(): Promise<CourseInfo> {
    const ltik = sessionStorage.getItem('ltik')
    if (!ltik) throw new Error('Token LTI (ltik) no disponible')

    const res = await fetch(`${URL}/info/course`, {
        method: 'GET',
        headers: {
            'ngrok-skip-browser-warning': 'any',
            'Authorization': `Bearer ${ltik}`,
        },
    })

    const data = await res.json()
    return data
}

export async function getPlatformInfo(): Promise<PlatformInfo> {
    const ltik = sessionStorage.getItem('ltik')
    if (!ltik) throw new Error('Token LTI (ltik) no disponible')

    const res = await fetch(`${URL}/info/platform`, {
        method: 'GET',
        headers: {
            'ngrok-skip-browser-warning': 'any',
            'Authorization': `Bearer ${ltik}`,
        },
    })

    const data = await res.json()
    console.log(data)
    return data
}
