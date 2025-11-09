import type { CourseInfo, PlatformInfo, UserInfo } from './info.types'
import configs from "@/core/configs"


export async function getUserInfo(): Promise<UserInfo> {
    const ltik = sessionStorage.getItem('ltik')
    if (!ltik) throw new Error('Token LTI (ltik) no disponible')

    const res = await fetch(`${configs.ltiBaseUrl}/info/user`, {
        method: 'GET',
        headers: {
            'credentials': 'include',
            'Authorization': `Bearer ${ltik}`,
        },
    })

    const data = await res.json()
    return data
}

export async function getCourseInfo(): Promise<CourseInfo> {
    const ltik = sessionStorage.getItem('ltik')
    if (!ltik) throw new Error('Token LTI (ltik) no disponible')

    const res = await fetch(`${configs.ltiBaseUrl}/info/course`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${ltik}`,
        },
    })

    const data = await res.json()
    return data
}

export async function getPlatformInfo(): Promise<PlatformInfo> {
    const ltik = sessionStorage.getItem('ltik')
    if (!ltik) throw new Error('Token LTI (ltik) no disponible')

    const res = await fetch(`${configs.ltiBaseUrl}/info/platform`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${ltik}`,
        },
    })

    const data = await res.json()
    return data
}

export async function getAssignmentInfo() {
    const ltik = sessionStorage.getItem('ltik')
    if (!ltik) throw new Error('Token LTI (ltik) no disponible')

    const res = await fetch(`${configs.ltiBaseUrl}/info/assignment`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${ltik}`,
        },
    })

    const data = await res.json()
    return data
}
