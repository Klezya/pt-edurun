import configs from "@/core/configs"

export async function getMembers() {
    const ltik = sessionStorage.getItem('ltik')
    if (!ltik) throw new Error('Token LTI (ltik) no disponible')

    const res = await fetch(`${configs.ltiBaseUrl}/members`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${ltik}`,
        },
    })

    const data = await res.json()
    console.log('Members data:', data)
    return data
}
