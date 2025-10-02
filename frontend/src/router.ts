import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/Home.vue'
import Interprete from '@/evaluacion/pages/interprete.vue'
import EvaluacionList from '@/evaluacion/pages/evaluacion_list.vue'

export const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: Home },
    { path: '/evaluaciones', name: 'evaluaciones', component: EvaluacionList },
    { path: '/evaluacion/:id', name: 'entorno-evaluacion', component: Interprete, props: true },
  ],
  scrollBehavior: () => ({ top: 0 }),
})

export default router