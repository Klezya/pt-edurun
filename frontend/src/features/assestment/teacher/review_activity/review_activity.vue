<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getEntregaEvaluacion} from './review_activity.service'
import type { EntregaEvaluacionResponse } from './review_activity.types'

const route = useRoute()
const router = useRouter()

const userId = ref<string>('')
const assessmentId = ref<string>('')
const loading = ref(true)
const entregaData = ref<EntregaEvaluacionResponse | null>(null)
const errorMessage = ref<string>('')

onMounted(async () => {
  try {
    // Obtener user_id y assessment_id de los parámetros de la URL
    userId.value = route.query.user_id as string || ''
    assessmentId.value = route.query.assessment_id as string || ''
    
    if (!userId.value) {
      console.warn('No se encontró user_id en los parámetros de URL')
      errorMessage.value = 'No se encontró el ID del usuario'
      return
    }

    if (!assessmentId.value) {
      console.warn('No se encontró assessment_id en los parámetros de URL')
      errorMessage.value = 'No se encontró el ID de la evaluación'
      return
    }

    // Llamar al servicio para obtener la entrega
    entregaData.value = await getEntregaEvaluacion(userId.value, parseInt(assessmentId.value))
    
    if (!entregaData.value) {
      errorMessage.value = 'No se encontró ninguna entrega para este estudiante'
    }
  } catch (error) {
    console.error('Error al cargar la información:', error)
    errorMessage.value = error instanceof Error ? error.message : 'Error al cargar la información de la entrega'
  } finally {
    loading.value = false
  }
})

function handleVolver() {
  router.back()
}

function formatTime(segundos: number): string {
  const horas = Math.floor(segundos / 3600)
  const minutos = Math.floor((segundos % 3600) / 60)
  const segs = segundos % 60
  
  if (horas > 0) {
    return `${horas}h ${minutos}m`
  } else if (minutos > 0) {
    return `${minutos}m ${segs}s`
  } else {
    return `${segs}s`
  }
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
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
              </div>
              <div>
                <h1 class="text-2xl font-bold bg-gradient-to-r from-purple-400 to-blue-500 bg-clip-text text-transparent">
                  Revisar Actividad
                </h1>
                <p class="text-sm text-slate-400">Revisión de entrega del estudiante</p>
              </div>
            </div>
            <div class="flex items-center gap-3">
              <button
                @click="handleVolver"
                class="inline-flex items-center gap-2 rounded-lg px-4 py-2.5 text-sm font-medium text-slate-200 hover:bg-white/10 hover:text-white transition-all duration-200 hover:scale-105"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
                </svg>
                Volver
              </button>
            </div>
          </div>
        </div>
      </header>

      <!-- Main Content -->
      <main class="flex flex-grow items-start justify-center px-4 py-8">
        <div class="mx-auto max-w-7xl w-full">
          <!-- Loading State -->
          <div v-if="loading" class="space-y-6">
            <div class="rounded-2xl border border-white/10 bg-slate-950/40 backdrop-blur-md shadow-2xl overflow-hidden">
              <div class="p-8 animate-pulse">
                <div class="h-6 w-48 bg-slate-700/50 rounded mb-4"></div>
                <div class="space-y-3">
                  <div class="h-4 w-full bg-slate-700/50 rounded"></div>
                  <div class="h-4 w-3/4 bg-slate-700/50 rounded"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- Error State -->
          <div v-else-if="errorMessage" class="rounded-2xl border border-red-500/20 bg-slate-950/40 backdrop-blur-md shadow-2xl overflow-hidden">
            <div class="p-8 text-center">
              <div class="mx-auto w-16 h-16 rounded-full bg-red-500/20 flex items-center justify-center mb-4">
                <svg class="w-8 h-8 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <h3 class="text-xl font-bold text-white mb-2">Error</h3>
              <p class="text-slate-400">{{ errorMessage }}</p>
            </div>
          </div>

          <!-- Content -->
          <div v-else class="space-y-6">
            <!-- Información del Estudiante -->
            <div class="rounded-2xl border border-white/10 bg-slate-950/40 backdrop-blur-md shadow-2xl overflow-hidden">
              <div class="p-8">
                <div class="flex items-center gap-3 mb-6 pb-4 border-b border-white/10">
                  <div class="bg-gradient-to-br from-sky-500/20 to-blue-600/20 p-2 rounded-lg">
                    <svg class="w-6 h-6 text-sky-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                    </svg>
                  </div>
                  <h3 class="text-xl font-bold text-white">Información del Estudiante</h3>
                </div>
                <div class="space-y-4">
                  <div v-if="userId" class="flex items-center gap-4 p-4 rounded-lg bg-slate-900/50 border border-white/10">
                    <span class="text-sm font-medium text-slate-400">ID de Usuario:</span>
                    <span class="text-lg font-mono font-semibold text-white bg-slate-800/50 px-4 py-2 rounded-lg">
                      {{ userId }}
                    </span>
                  </div>
                  <div v-if="assessmentId" class="flex items-center gap-4 p-4 rounded-lg bg-slate-900/50 border border-white/10">
                    <span class="text-sm font-medium text-slate-400">ID de Evaluación:</span>
                    <span class="text-lg font-mono font-semibold text-white bg-slate-800/50 px-4 py-2 rounded-lg">
                      {{ assessmentId }}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Información de la Entrega -->
            <div v-if="entregaData" class="space-y-6">
              <!-- Alerta de evaluación inválida -->
              <div 
                v-if="entregaData.detalles?.salio_pantalla_completa" 
                class="rounded-2xl border border-red-500/50 bg-red-950/40 backdrop-blur-md shadow-2xl overflow-hidden"
              >
                <div class="p-8">
                  <div class="flex items-center gap-4">
                    <div class="bg-red-500 p-3 rounded-xl shadow-lg">
                      <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
                      </svg>
                    </div>
                    <div class="flex-1">
                      <h3 class="text-2xl font-bold text-red-200 mb-2">⚠️ EVALUACIÓN INVALIDADA</h3>
                      <p class="text-red-300">
                        El estudiante salió de pantalla completa durante la evaluación. Esta prueba no es válida.
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Nota obtenida -->
              <div 
                :class="[
                  'rounded-2xl border backdrop-blur-md shadow-2xl overflow-hidden',
                  entregaData.detalles?.salio_pantalla_completa 
                    ? 'border-red-500/50 bg-red-950/20' 
                    : 'border-white/10 bg-slate-950/40'
                ]"
              >
                <div class="p-8">
                  <div class="flex items-center gap-3 mb-6 pb-4 border-b border-white/10">
                    <div 
                      :class="[
                        'p-2 rounded-lg',
                        entregaData.detalles?.salio_pantalla_completa
                          ? 'bg-red-500/20'
                          : 'bg-gradient-to-br from-emerald-500/20 to-teal-600/20'
                      ]"
                    >
                      <svg 
                        :class="[
                          'w-6 h-6',
                          entregaData.detalles?.salio_pantalla_completa ? 'text-red-400' : 'text-emerald-400'
                        ]" 
                        fill="none" 
                        stroke="currentColor" 
                        viewBox="0 0 24 24"
                      >
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                      </svg>
                    </div>
                    <h3 class="text-xl font-bold text-white">Resultado de la Evaluación</h3>
                    <span 
                      v-if="entregaData.detalles?.salio_pantalla_completa"
                      class="ml-auto px-3 py-1 rounded-full bg-red-500/20 text-red-300 text-xs font-semibold border border-red-500/30"
                    >
                      NO VÁLIDA
                    </span>
                  </div>
                  <div class="text-center py-6">
                    <p class="text-sm text-slate-400 mb-2">Puntaje obtenido de los Test Unitarios</p>
                    <p 
                      :class="[
                        'text-6xl font-bold bg-clip-text text-transparent',
                        entregaData.detalles?.salio_pantalla_completa
                          ? 'bg-gradient-to-r from-red-400 to-red-600'
                          : 'bg-gradient-to-r from-emerald-400 to-teal-500'
                      ]"
                    >
                      {{ entregaData.nota }}/100
                    </p>
                  </div>
                </div>
              </div>

              <!-- Código enviado -->
              <div v-if="entregaData.codigo" class="rounded-2xl border border-white/10 bg-slate-950/40 backdrop-blur-md shadow-2xl overflow-hidden">
                <div class="p-8">
                  <div class="flex items-center gap-3 mb-6 pb-4 border-b border-white/10">
                    <div class="bg-gradient-to-br from-purple-500/20 to-blue-600/20 p-2 rounded-lg">
                      <svg class="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path>
                      </svg>
                    </div>
                    <h3 class="text-xl font-bold text-white">Código Enviado</h3>
                  </div>
                  <div class="rounded-lg bg-slate-900/50 border border-white/10 overflow-hidden">
                    <pre class="p-4 overflow-x-auto text-sm text-slate-300 font-mono"><code>{{ entregaData.codigo }}</code></pre>
                  </div>
                </div>
              </div>

              <!-- Actividad de Desarrollo -->
              <div v-if="entregaData.detalles" class="rounded-2xl border border-white/10 bg-slate-950/40 backdrop-blur-md shadow-2xl overflow-hidden">
                <div class="p-8">
                  <div class="flex items-center gap-3 mb-6 pb-4 border-b border-white/10">
                    <div class="bg-gradient-to-br from-blue-500/20 to-purple-600/20 p-2 rounded-lg">
                      <svg class="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                      </svg>
                    </div>
                    <h3 class="text-xl font-bold text-white">Actividad de Desarrollo</h3>
                  </div>
                  
                  <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div class="p-6 rounded-xl bg-gradient-to-br from-blue-900/30 to-blue-800/20 border border-blue-500/30">
                      <div class="flex items-center gap-3 mb-2">
                        <div class="bg-blue-500/20 p-2 rounded-lg">
                          <svg class="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"></path>
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                          </svg>
                        </div>
                        <p class="text-sm font-medium text-blue-300">Ejecuciones de código</p>
                      </div>
                      <p class="text-4xl font-bold text-blue-200">{{ entregaData.detalles.ejecuciones_codigo || 0 }}</p>
                      <p class="text-xs text-blue-400/70 mt-1">Veces que ejecutó su código</p>
                    </div>
                    <div class="p-6 rounded-xl bg-gradient-to-br from-purple-900/30 to-purple-800/20 border border-purple-500/30">
                      <div class="flex items-center gap-3 mb-2">
                        <div class="bg-purple-500/20 p-2 rounded-lg">
                          <svg class="w-5 h-5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                          </svg>
                        </div>
                        <p class="text-sm font-medium text-purple-300">Ejecuciones de tests</p>
                      </div>
                      <p class="text-4xl font-bold text-purple-200">{{ entregaData.detalles.ejecuciones_tests || 0 }}</p>
                      <p class="text-xs text-purple-400/70 mt-1">Veces que corrió los tests</p>
                    </div>
                    <div class="p-6 rounded-xl bg-gradient-to-br from-emerald-900/30 to-emerald-800/20 border border-emerald-500/30">
                      <div class="flex items-center gap-3 mb-2">
                        <div class="bg-emerald-500/20 p-2 rounded-lg">
                          <svg class="w-5 h-5 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                          </svg>
                        </div>
                        <p class="text-sm font-medium text-emerald-300">Tiempo total</p>
                      </div>
                      <p class="text-4xl font-bold text-emerald-200">{{ formatTime(entregaData.detalles.tiempo_total_segundos || 0) }}</p>
                      <p class="text-xs text-emerald-400/70 mt-1">Duración de la evaluación</p>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Acciones Sospechosas -->
              <div v-if="entregaData.detalles" class="rounded-2xl border border-white/10 bg-slate-950/40 backdrop-blur-md shadow-2xl overflow-hidden">
                <div class="p-8">
                  <div class="flex items-center gap-3 mb-6 pb-4 border-b border-white/10">
                    <div class="bg-gradient-to-br from-amber-500/20 to-orange-600/20 p-2 rounded-lg">
                      <svg class="w-6 h-6 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
                      </svg>
                    </div>
                    <h3 class="text-xl font-bold text-white">Acciones Sospechosas</h3>
                  </div>
                  
                  <!-- Estado de pantalla completa -->
                  <div 
                    :class="[
                      'mb-6 p-5 rounded-xl border flex items-center gap-4',
                      entregaData.detalles.salio_pantalla_completa
                        ? 'bg-red-950/30 border-red-500/50'
                        : 'bg-emerald-950/30 border-emerald-500/50'
                    ]"
                  >
                    <div 
                      :class="[
                        'p-3 rounded-xl shadow-lg',
                        entregaData.detalles.salio_pantalla_completa
                          ? 'bg-red-500'
                          : 'bg-emerald-500'
                      ]"
                    >
                      <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path 
                          v-if="entregaData.detalles.salio_pantalla_completa"
                          stroke-linecap="round" 
                          stroke-linejoin="round" 
                          stroke-width="2" 
                          d="M6 18L18 6M6 6l12 12"
                        ></path>
                        <path 
                          v-else
                          stroke-linecap="round" 
                          stroke-linejoin="round" 
                          stroke-width="2" 
                          d="M5 13l4 4L19 7"
                        ></path>
                      </svg>
                    </div>
                    <div class="flex-1">
                      <p 
                        :class="[
                          'text-sm font-medium mb-1',
                          entregaData.detalles.salio_pantalla_completa
                            ? 'text-red-300'
                            : 'text-emerald-300'
                        ]"
                      >
                        Estado de Pantalla Completa
                      </p>
                      <p 
                        :class="[
                          'text-xl font-bold',
                          entregaData.detalles.salio_pantalla_completa
                            ? 'text-red-200'
                            : 'text-emerald-200'
                        ]"
                      >
                        {{ entregaData.detalles.salio_pantalla_completa ? 'Salió de pantalla completa' : 'Permaneció en pantalla completa' }}
                      </p>
                    </div>
                  </div>

                  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    <div class="p-4 rounded-lg bg-slate-900/50 border border-white/10">
                      <p class="text-xs text-slate-400 mb-1">Intentos de copiar</p>
                      <p class="text-2xl font-bold text-white">{{ entregaData.detalles.intentos_copiar }}</p>
                    </div>
                    <div class="p-4 rounded-lg bg-slate-900/50 border border-white/10">
                      <p class="text-xs text-slate-400 mb-1">Intentos de pegar</p>
                      <p class="text-2xl font-bold text-white">{{ entregaData.detalles.intentos_pegar }}</p>
                    </div>
                    <div class="p-4 rounded-lg bg-slate-900/50 border border-white/10">
                      <p class="text-xs text-slate-400 mb-1">Intentos de cortar</p>
                      <p class="text-2xl font-bold text-white">{{ entregaData.detalles.intentos_cortar }}</p>
                    </div>
                    <div class="p-4 rounded-lg bg-slate-900/50 border border-white/10">
                      <p class="text-xs text-slate-400 mb-1">Cambios de ventana</p>
                      <p class="text-2xl font-bold text-white">{{ entregaData.detalles.cambios_ventana }}</p>
                    </div>
                    <div class="p-4 rounded-lg bg-slate-900/50 border border-white/10">
                      <p class="text-xs text-slate-400 mb-1">Tiempo fuera de la Evaluacion</p>
                      <p class="text-2xl font-bold text-white">{{ entregaData.detalles.tiempo_inactividad_segundos }}s</p>
                    </div>
                  </div>
                  <div v-if="entregaData.detalles.timestamp" class="mt-4 p-4 rounded-lg bg-slate-900/50 border border-white/10">
                    <p class="text-xs text-slate-400 mb-1">Fecha y hora de entrega</p>
                    <p class="text-sm text-white font-mono">{{ new Date(entregaData.detalles.timestamp).toLocaleString('es-ES') }}</p>
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
          <div class="flex flex-col items-center justify-center gap-2">
            <p class="text-sm text-slate-400">Sistema de Gestión de Actividades</p>
            <p class="text-xs text-slate-500">© 2025 - Plataforma Educativa</p>
          </div>
        </div>
      </footer>
    </div>
  </div>
</template>

<style scoped>
/* Estilos adicionales si son necesarios */
</style>
