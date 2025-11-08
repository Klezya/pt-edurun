import { getUserInfo, getRol } from '@/features/lti_protocol'
import type { NavigationGuardNext, RouteLocationNormalized } from 'vue-router'

export async function actividadesGuard(
    to: RouteLocationNormalized,
    from: RouteLocationNormalized,
    next: NavigationGuardNext
) {
    try {
        const info = await getUserInfo()
        const rol = getRol(info.roles)

        if (rol === 'docente') {
            next({ name: 'actividades-docente' })
        } else if (rol === 'estudiante') {
            next({ name: 'tareas-estudiante' })
        } else {
            next({ name: 'home' })
        }
    } catch (error) {
        console.error('Error en el guard:', error)
        next({ name: 'home' })
    }
}

export async function evaluacionGuard(
    to: RouteLocationNormalized,
    from: RouteLocationNormalized,
    next: NavigationGuardNext
) {
    try {
        const info = await getUserInfo()
        const rol = getRol(info.roles)

        if (rol === 'docente') {
            next({ name: 'entorno-evaluacion', params: { id: to.params.id } })
        } else if (rol === 'estudiante') {
            next({ name: 'entorno-evaluacion', params: { id: to.params.id } })
        } else {
            next({ name: 'home' })
        }
    } catch (error) {
        console.error('Error en el guard:', error)
        next({ name: 'home' })
    }
}