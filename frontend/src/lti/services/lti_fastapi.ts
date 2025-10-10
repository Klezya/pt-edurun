import type { UserInfo, CourseInfo, PlatformInfo } from '../interfaces/info'

const URL = 'https://edurunbackend.loca.lt/lti'


export async function isUserRegistered(userIdLms: string) {
  const result = await fetch(`${URL}/check_user/${userIdLms}`).then(res => res.json())
  return result
}

export async function getCourseIdByLmsId(courseIdLms: string): Promise<{ id: number } | { error: string }> {
  const result = await fetch(`${URL}/course/${courseIdLms}`).then(res => res.json())
  return result
}

export async function registerInstance(
  userInfo: UserInfo,
  courseInfo: CourseInfo,
  platformInfo: PlatformInfo
) {
  const payload = {
    usuario: {
      id_lms: userInfo.userId,
      nombre: userInfo.name? userInfo.name : null,
    },
    curso: {
      nombre: courseInfo.title,
      etiqueta: courseInfo.label,
      id_curso_lms: courseInfo.id,
      id_plataforma: 0 // Este valor debería ser actualizado cuando se registre la plataforma
    },
    plataforma: {
      guid: platformInfo.guid,
      nombre: platformInfo.name,
      version: platformInfo.version,
      family_code: platformInfo.product_family_code
    }
  }
  const result = await fetch(`${URL}/register_instance/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload)
  })

  return result
}
