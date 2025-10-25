import { createRouter, createWebHistory } from 'vue-router'
import type { NavigationGuardNext, RouteLocationNormalized } from 'vue-router'
// Vistas
import Home from '@/Home.vue'
import Interprete from '@/features/assestment/code_running/interprete_evaluacion.vue'
import TareasListEstudiante from '@/features/assestment/student/tareas_list.vue'
import TareasListDocente from '@/features/assestment/teacher/list_activity/activity_list.vue'
import SeleccionarEvaluacion from '@/features/assestment/teacher/deeplinks/select_evaluacion.vue'
import CreateEvaluacion from '@/features/assestment/teacher/create_activity/create_activity.vue'

import { getUserInfo, getRol } from './features/lti_protocol'


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
    { path: '/crear_evaluacion', name: 'crear-evaluacion', component: CreateEvaluacion },
  ],
  scrollBehavior: () => ({ top: 0 }),
})

export default router