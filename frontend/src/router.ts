import { createRouter, createWebHistory } from 'vue-router'
import type { NavigationGuardNext, RouteLocationNormalized } from 'vue-router'
import Home from '@/Home.vue'
import Interprete from '@/evaluacion/pages/interprete.vue'
import EvaluacionList from '@/evaluacion/pages/evaluacion_list.vue'
import EvaluacionListDocente from '@/evaluacion/pages/evaluacion_list_docente.vue'
import EvaluacionListEstudiante from '@/evaluacion/pages/evaluacion_list_estudiante.vue'
import endpointtest from './lti/pages/endpointtest.vue'
import { getUserInfo } from './lti/services/info'
import { getRol } from './lti/interfaces/roles'

// Navigation guard para redirigir según el rol
async function evaluacionesGuard(
  to: RouteLocationNormalized,
  from: RouteLocationNormalized,
  next: NavigationGuardNext
) {
  try {
    const info = await getUserInfo()
    const rol = getRol(info.roles)
    
    if (rol === 'docente') {
      // Redirige a la página de docente
      next({ name: 'evaluaciones-docente' })
    } else if (rol === 'estudiante') {
      // Redirige a la página de estudiante
      next({ name: 'evaluaciones-estudiante' })
    } else {
      // Si no hay rol o es desconocido, redirige al home
      next({ name: 'home' })
    }
  } catch (error) {
    console.error('Error al obtener el rol del usuario:', error)
    next({ name: 'home' })
  }
}

export const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: Home },
    // Ruta intermedia que redirige según el rol
    { 
      path: '/evaluaciones', 
      name: 'evaluaciones', 
      component: EvaluacionList,
      beforeEnter: evaluacionesGuard
    },
    // Rutas específicas por rol
    { 
      path: '/evaluaciones/estudiante', 
      name: 'evaluaciones-estudiante', 
      component: EvaluacionListEstudiante 
    },
    { 
      path: '/evaluaciones/docente', 
      name: 'evaluaciones-docente', 
      component: EvaluacionListDocente
    },
    { path: '/evaluacion/:id', name: 'entorno-evaluacion', component: Interprete, props: true },
    { path: '/testendpoint', name: 'testendpoint', component: endpointtest },
  ],
  scrollBehavior: () => ({ top: 0 }),
})

export default router