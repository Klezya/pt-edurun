import type { UserInfo, CourseInfo, PlatformInfo } from '@/features/lti_protocol'
import configs from "@/core/configs"

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

  const result = await fetch(`${configs.apiBaseUrl}/lti/register_instance/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload)
  })

  return result
}
