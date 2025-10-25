<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

import { getCourseInfo } from '@/features/lti_protocol/info/info.service'

import { getTareasByCourseLmsId, getEvaluacionesByCourseLmsId } from '../../shared'
import type { Actividad } from '../../shared/activity.types'

const loading = ref(true)
const evaluaciones = ref<Actividad[]>([])
const tareas = ref<Actividad[]>([])
const courseName = ref<string>('')
const router = useRouter()

// Estados de desplegables
const evaluacionesExpanded = ref(true)
const tareasExpanded = ref(true)

onMounted(async () => {
  try {
    const courseInfo = await getCourseInfo()
    courseName.value = courseInfo.title || courseInfo.label
    
    const courseId = courseInfo.id
    const [evaluacionesData, tareasData] = await Promise.all([
      getEvaluacionesByCourseLmsId(courseId),
      getTareasByCourseLmsId(courseId)
    ])

    evaluaciones.value = evaluacionesData as Actividad[]
    tareas.value = tareasData as Actividad[]
  } catch (error) {
    console.error('Error al cargar las actividades:', error)
  } finally {
    loading.value = false
  }
})

function verDetallesEvaluacion(actividad: Actividad) {
  // TODO: Implementar vista de detalles de la evaluación
  console.log('Ver detalles de evaluación:', actividad.id)
  // router.push({ name: 'evaluacion-detalles', params: { id: actividad.id } })
}

function editarEvaluacion(actividad: Actividad) {
  // TODO: Implementar edición de evaluación
  console.log('Editar evaluación:', actividad.id)
  // router.push({ name: 'evaluacion-editar', params: { id: actividad.id } })
}

function verDetallesTarea(actividad: Actividad) {
  // TODO: Implementar vista de detalles de la tarea
  console.log('Ver detalles de tarea:', actividad.id)
  // router.push({ name: 'tarea-detalles', params: { id: actividad.id } })
}

function editarTarea(actividad: Actividad) {
  // TODO: Implementar edición de tarea
  console.log('Editar tarea:', actividad.id)
  // router.push({ name: 'tarea-editar', params: { id: tarea.id } })
}

function crearActividad() {
  router.push({ name: 'crear-actividad' })
}

function toggleEvaluaciones() {
  evaluacionesExpanded.value = !evaluacionesExpanded.value
}

function toggleTareas() {
  tareasExpanded.value = !tareasExpanded.value
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
    <!-- Decorative background elements -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-20 left-10 w-72 h-72 bg-purple-500/10 rounded-full blur-3xl"></div>
      <div class="absolute bottom-20 right-10 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl"></div>
    </div>

    <div class="relative flex min-h-screen flex-col">
      <!-- Header -->
      <header class="border-b border-white/10 bg-slate-950/30 backdrop-blur-sm shadow-lg">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div class="flex h-20 items-center justify-between">
            <div class="flex items-center gap-3">
              <div class="bg-gradient-to-br from-purple-400 to-blue-600 p-2 rounded-xl shadow-lg">
                <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
                </svg>
              </div>
              <div>
                <h1 class="text-2xl font-bold bg-gradient-to-r from-purple-400 to-blue-500 bg-clip-text text-transparent">
                  <p v-if="courseName">{{ courseName }}</p>
                </h1>
                  Panel de Actividades
              </div>
            </div>
            <div class="flex items-center gap-3">
              <button
                @click="crearActividad"
                class="inline-flex items-center gap-2 rounded-lg bg-gradient-to-r from-emerald-600 to-teal-700 px-4 py-2.5 text-sm font-medium text-white hover:from-emerald-500 hover:to-teal-600 transition-all duration-200 hover:scale-105 shadow-lg"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
                </svg>
                Crear Actividad
              </button>
              <RouterLink
                to="/"
                class="inline-flex items-center gap-2 rounded-lg px-4 py-2.5 text-sm font-medium text-slate-200 hover:bg-white/10 hover:text-white transition-all duration-200 hover:scale-105"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
                </svg>
                Volver
              </RouterLink>
            </div>
          </div>
        </div>
      </header>

      <!-- Main Content -->
      <main class="flex flex-grow items-center justify-center px-4 py-8">
        <div class="mx-auto max-w-5xl w-full">
          <!-- Loading State -->
          <div v-if="loading" class="space-y-4">
            <div class="rounded-2xl border border-white/10 bg-slate-950/40 backdrop-blur-md shadow-2xl overflow-hidden">
              <div class="p-6">
                <div class="animate-pulse space-y-4">
                  <div class="h-6 w-2/3 rounded bg-slate-700/50"></div>
                  <div class="h-4 w-40 rounded bg-slate-800/50"></div>
                  <div class="flex gap-2">
                    <div class="h-10 w-24 rounded bg-slate-800/50"></div>
                    <div class="h-10 w-24 rounded bg-slate-800/50"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Empty State -->
          <div v-else-if="evaluaciones.length === 0 && tareas.length === 0" class="rounded-2xl border border-white/10 bg-slate-950/40 backdrop-blur-md shadow-2xl overflow-hidden">
            <div class="p-12 text-center">
              <div class="mx-auto w-20 h-20 rounded-full bg-gradient-to-br from-slate-700/50 to-slate-800/50 flex items-center justify-center mb-6">
                <svg class="w-10 h-10 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
              </div>
              <h3 class="text-2xl font-bold text-white mb-2">No hay actividades creadas</h3>
              <p class="text-slate-400 mb-6">Comienza creando tu primera actividad para este curso.</p>
              <button
                @click="crearActividad"
                class="inline-flex items-center gap-2 rounded-lg bg-gradient-to-r from-emerald-600 to-teal-700 px-6 py-3 text-sm font-medium text-white hover:from-emerald-500 hover:to-teal-600 transition-all duration-200 hover:scale-105 shadow-lg"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
                </svg>
                Crear Primera Actividad
              </button>
            </div>
          </div>

          <!-- Actividades List -->
          <div v-else class="space-y-6">
            
            <!-- Evaluaciones Section -->
            <div class="rounded-2xl border border-white/10 bg-slate-950/40 backdrop-blur-md shadow-2xl overflow-hidden">
              <!-- Header -->
              <button
                @click="toggleEvaluaciones"
                class="w-full flex items-center justify-between p-6 hover:bg-white/5 transition-all duration-200"
              >
                <div class="flex items-center gap-3">
                  <div class="bg-gradient-to-br from-purple-400 to-blue-600 p-2 rounded-lg shadow-lg">
                    <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"></path>
                    </svg>
                  </div>
                  <div class="text-left">
                    <h2 class="text-xl font-bold text-white">Evaluaciones</h2>
                    <p class="text-sm text-slate-400">{{ evaluaciones.length }} evaluaciones disponibles</p>
                  </div>
                </div>
                <svg 
                  class="w-6 h-6 text-slate-400 transition-transform duration-200"
                  :class="{ 'rotate-180': evaluacionesExpanded }"
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                </svg>
              </button>

              <!-- Content -->
              <div 
                v-show="evaluacionesExpanded"
                class="border-t border-white/10"
              >
                <div v-if="evaluaciones.length === 0" class="p-6 text-center text-slate-400">
                  No hay evaluaciones creadas para este curso.
                </div>
                <div v-else class="divide-y divide-white/10">
                  <div
                    v-for="evaluacion in evaluaciones"
                    :key="evaluacion.id"
                    class="p-6 hover:bg-white/5 transition-all duration-200"
                  >
                    <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
                      <div class="flex-grow">
                        <h3 class="text-lg font-bold text-white mb-2">
                          {{ evaluacion.titulo }}
                        </h3>
                      </div>
                      
                      <!-- Action Buttons -->
                      <div class="flex flex-wrap gap-2">
                        <button
                          @click="verDetallesEvaluacion(evaluacion)"
                          class="inline-flex items-center gap-2 rounded-lg bg-slate-700 hover:bg-slate-600 px-4 py-2.5 text-sm font-medium text-white transition-all duration-200 hover:scale-105"
                        >
                          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                          </svg>
                          Ver
                        </button>
                        <button
                          @click="editarEvaluacion(evaluacion)"
                          class="inline-flex items-center gap-2 rounded-lg bg-gradient-to-r from-purple-600 to-blue-700 px-4 py-2.5 text-sm font-medium text-white hover:from-purple-500 hover:to-blue-600 transition-all duration-200 hover:scale-105 shadow-lg"
                        >
                          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                          </svg>
                          Editar
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Tareas Section -->
            <div class="rounded-2xl border border-white/10 bg-slate-950/40 backdrop-blur-md shadow-2xl overflow-hidden">
              <!-- Header -->
              <button
                @click="toggleTareas"
                class="w-full flex items-center justify-between p-6 hover:bg-white/5 transition-all duration-200"
              >
                <div class="flex items-center gap-3">
                  <div class="bg-gradient-to-br from-emerald-400 to-teal-600 p-2 rounded-lg shadow-lg">
                    <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"></path>
                    </svg>
                  </div>
                  <div class="text-left">
                    <h2 class="text-xl font-bold text-white">Tareas</h2>
                    <p class="text-sm text-slate-400">{{ tareas.length }} tareas disponibles</p>
                  </div>
                </div>
                <svg 
                  class="w-6 h-6 text-slate-400 transition-transform duration-200"
                  :class="{ 'rotate-180': tareasExpanded }"
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                </svg>
              </button>

              <!-- Content -->
              <div 
                v-show="tareasExpanded"
                class="border-t border-white/10"
              >
                <div v-if="tareas.length === 0" class="p-6 text-center text-slate-400">
                  No hay tareas creadas para este curso.
                </div>
                <div v-else class="divide-y divide-white/10">
                  <div
                    v-for="tarea in tareas"
                    :key="tarea.id"
                    class="p-6 hover:bg-white/5 transition-all duration-200"
                  >
                    <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
                      <div class="flex-grow">
                        <h3 class="text-lg font-bold text-white mb-2">
                          {{ tarea.titulo }}
                        </h3>
                      </div>
                      
                      <!-- Action Buttons -->
                      <div class="flex flex-wrap gap-2">
                        <button
                          @click="verDetallesTarea(tarea)"
                          class="inline-flex items-center gap-2 rounded-lg bg-slate-700 hover:bg-slate-600 px-4 py-2.5 text-sm font-medium text-white transition-all duration-200 hover:scale-105"
                        >
                          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                          </svg>
                          Ver
                        </button>
                        <button
                          @click="editarTarea(tarea)"
                          class="inline-flex items-center gap-2 rounded-lg bg-gradient-to-r from-emerald-600 to-teal-700 px-4 py-2.5 text-sm font-medium text-white hover:from-emerald-500 hover:to-teal-600 transition-all duration-200 hover:scale-105 shadow-lg"
                        >
                          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                          </svg>
                          Editar
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

          </div>
        </div>
      </main>

      <!-- Footer -->
      <footer class="border-t border-white/10 bg-slate-950/30 backdrop-blur-sm">
        <div class="mx-auto max-w-7xl px-4 py-8">
          <div class="flex flex-col md:flex-row items-center justify-between gap-4">
            <p class="text-sm text-slate-400">
              © 2025 Edurun. Todos los derechos reservados.
            </p>
          </div>
        </div>
      </footer>
    </div>
  </div>
</template>

<style scoped>
@keyframes gradient {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

.animate-gradient {
  background-size: 200% 200%;
  animation: gradient 3s ease infinite;
}

/* Smooth transitions for all interactive elements */
* {
  transition-property: color, background-color, border-color, text-decoration-color, fill, stroke, opacity, box-shadow, transform;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}
</style>

