<script setup lang="ts">
// Vue
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
// LTI Services
import { getCourseInfo } from '@/lti/services/info'
// Tareas
import { getTareasByCourseLmsId } from '../services/tareas'
// Helpers
import { formatDate } from '../helpers/format_date'
import type { Evaluacion } from '../interfaces/evaluacion'

const loading = ref(true)
const evaluaciones = ref<Evaluacion[]>([])
const courseName = ref<string>('')
const router = useRouter()

onMounted(async () => {
  try {
    // Obtener información del curso
    const courseInfo = await getCourseInfo()
    courseName.value = courseInfo.title || courseInfo.label
    
    // Obtener evaluaciones del curso
    const courseId = courseInfo.id
    evaluaciones.value = await getTareasByCourseLmsId(courseId) as Evaluacion[]
  } catch (error) {
    console.error('Error al cargar las evaluaciones:', error)
  } finally {
    loading.value = false
  }
})

function comenzar(evaluacion: Evaluacion) {
  router.push({ name: 'entorno-evaluacion', params: { id: evaluacion.id } })
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
    <!-- Decorative background elements -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-20 left-10 w-72 h-72 bg-sky-500/10 rounded-full blur-3xl"></div>
      <div class="absolute bottom-20 right-10 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl"></div>
    </div>

    <div class="relative flex min-h-screen flex-col">
      <!-- Header -->
      <header class="border-b border-white/10 bg-slate-950/30 backdrop-blur-sm shadow-lg">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div class="flex h-20 items-center justify-between">
            <div class="flex items-center gap-3">
              <div class="bg-gradient-to-br from-sky-400 to-blue-600 p-2 rounded-xl shadow-lg">
                <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
                </svg>
              </div>
              <div>
                <h1 class="text-2xl font-bold bg-gradient-to-r from-sky-400 to-blue-500 bg-clip-text text-transparent">
                  Mis Evaluaciones
                </h1>
                <p v-if="courseName" class="text-sm text-slate-400">{{ courseName }}</p>
              </div>
            </div>
            <div class="flex items-center gap-3">
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
        <div class="mx-auto max-w-4xl w-full">
          <!-- Loading State -->
          <div v-if="loading" class="space-y-4">
            <div class="rounded-2xl border border-white/10 bg-slate-950/40 backdrop-blur-md shadow-2xl overflow-hidden">
              <div class="p-6">
                <div class="animate-pulse space-y-4">
                  <div class="h-6 w-2/3 rounded bg-slate-700/50"></div>
                  <div class="h-4 w-40 rounded bg-slate-800/50"></div>
                  <div class="h-10 w-28 rounded bg-slate-800/50"></div>
                </div>
              </div>
            </div>
            <div class="rounded-2xl border border-white/10 bg-slate-950/40 backdrop-blur-md shadow-2xl overflow-hidden">
              <div class="p-6">
                <div class="animate-pulse space-y-4">
                  <div class="h-6 w-1/2 rounded bg-slate-700/50"></div>
                  <div class="h-4 w-32 rounded bg-slate-800/50"></div>
                  <div class="h-10 w-28 rounded bg-slate-800/50"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- Empty State -->
          <div v-else-if="evaluaciones.length === 0" class="rounded-2xl border border-white/10 bg-slate-950/40 backdrop-blur-md shadow-2xl overflow-hidden">
            <div class="p-12 text-center">
              <div class="mx-auto w-20 h-20 rounded-full bg-gradient-to-br from-slate-700/50 to-slate-800/50 flex items-center justify-center mb-6">
                <svg class="w-10 h-10 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
              </div>
              <h3 class="text-2xl font-bold text-white mb-2">No hay evaluaciones disponibles</h3>
              <p class="text-slate-400">Tu docente aún no ha asignado evaluaciones para este curso.</p>
            </div>
          </div>

          <!-- Evaluaciones List -->
          <div v-else class="space-y-4">
            <div
              v-for="evaluacion in evaluaciones"
              :key="evaluacion.id"
              class="group relative overflow-hidden rounded-2xl border border-white/10 bg-slate-950/40 backdrop-blur-md shadow-2xl hover:border-sky-500/50 transition-all duration-300 hover:shadow-lg hover:shadow-sky-500/20"
            >
              <!-- Decorative gradient blob -->
              <div class="absolute top-0 right-0 w-64 h-64 bg-sky-500/10 rounded-full blur-3xl group-hover:bg-sky-500/20 transition-all duration-300"></div>
              
              <div class="relative p-6">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                  <div class="flex-grow">
                    <div class="flex items-start gap-3 mb-3">
                      <div class="flex-shrink-0 mt-1">
                        <div class="bg-gradient-to-br from-sky-400 to-blue-600 p-2 rounded-lg shadow-lg">
                          <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                          </svg>
                        </div>
                      </div>
                      <div>
                        <h3 class="text-xl font-bold text-white group-hover:text-sky-400 transition-colors">
                          {{ evaluacion.titulo }}
                        </h3>
                        <div class="flex items-center gap-2 mt-2 text-sm text-slate-400">
                          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                          </svg>
                          <span>Fecha límite: {{ formatDate(evaluacion.fecha_limite) }}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <button
                    @click="comenzar(evaluacion)"
                    class="flex-shrink-0 inline-flex items-center gap-2 rounded-lg bg-gradient-to-r from-sky-600 to-blue-700 px-6 py-3 text-sm font-medium text-white hover:from-sky-500 hover:to-blue-600 transition-all duration-200 hover:scale-105 shadow-lg hover:shadow-sky-500/50"
                  >
                    <span>Comenzar</span>
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path>
                    </svg>
                  </button>
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
