import { createRouter, createWebHistory } from 'vue-router'
import type { NavigationGuardNext, RouteLocationNormalized } from 'vue-router'
// Vistas
import Home from '@/Home.vue'
import Interprete from '@/evaluacion/pages/interprete.vue'
import TareasListEstudiante from './evaluacion/pages/tareas_list_estudiante.vue'
import TareasListDocente from './evaluacion/pages/tareas_list_docente.vue'
import SeleccionarEvaluacion from './evaluacion/pages/docente_select_evaluacion.vue'
import endpointtest from './lti/pages/endpointtest.vue'
// Funciones
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
      next({ name: 'evaluaciones-docente' })
    } else if (rol === 'estudiante') {
      next({ name: 'evaluaciones-estudiante' })
    } else {
      next({ name: 'home' })
    }
  } catch (error) {
    console.error('Error al obtener el rol del usuario:', error)
    next({ name: 'home' })
  }
}

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'home', component: Home },
    // Ruta que redirige según el rol del usuario
    { 
      path: '/tareas', 
      name: 'tareas', 
      redirect: (to) => {
        return { name: 'home' }
      },
      beforeEnter: evaluacionesGuard
    },
    { 
      path: '/tareas/estudiante', 
      name: 'tareas-estudiante', 
      component: TareasListEstudiante 
    },
    { 
      path: '/tareas/docente', 
      name: 'tareas-docente', 
      component: TareasListDocente
    },
    { path: '/tarea/:id', name: 'entorno-tarea', component: Interprete, props: true },
    { path: '/evaluacion/:id', name: 'entorno-evaluacion', component: Interprete, props: true },
    { path: '/seleccionar_evaluacion', name: 'seleccionar-evaluacion', component: SeleccionarEvaluacion },
    { path: '/testendpoint', name: 'testendpoint', component: endpointtest },
  ],
  scrollBehavior: () => ({ top: 0 }),
})

export default router