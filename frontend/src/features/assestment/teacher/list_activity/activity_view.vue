<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getEvaluacion, getTarea } from '../../shared'
import type { Actividad } from '../../shared/activity.types'

const router = useRouter()
const route = useRoute()

const loading = ref(true)
const actividad = ref<Actividad | null>(null)
const errorMessage = ref('')
const tipo = ref<'evaluacion' | 'tarea'>('evaluacion')

// Computed properties
const titulo = computed(() => actividad.value?.titulo || '')
const contenido = computed(() => actividad.value?.contenido || '')
const test = computed(() => actividad.value?.test || '')
const hasTest = computed(() => test.value && test.value.trim() !== '')

onMounted(async () => {
  try {
    const activityId = Number(route.params.id)
    tipo.value = route.params.tipo as 'evaluacion' | 'tarea'

    if (isNaN(activityId)) {
      errorMessage.value = 'ID de actividad inválido'
      loading.value = false
      return
    }

    if (tipo.value === 'evaluacion') {
      actividad.value = await getEvaluacion(activityId)
    } else {
      actividad.value = await getTarea(activityId)
    }
  } catch (error) {
    console.error('Error al cargar la actividad:', error)
    errorMessage.value = 'Error al cargar los detalles de la actividad'
  } finally {
    loading.value = false
  }
})

function handleVolver() {
  router.push({ name: 'actividades-docente' })
}

function handleEditar() {
  router.push({ 
    name: 'actividad-editar', 
    params: { 
      id: actividad.value?.id, 
      tipo: tipo.value 
    } 
  })
}

function formatLineNumbers(code: string): string[] {
  return code.split('\n')
}

async function copiarCodigo() {
  try {
    await navigator.clipboard.writeText(test.value)
  } catch (error) {
    console.error('Error al copiar código:', error)
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
              <div 
                class="p-2 rounded-xl shadow-lg"
                :class="tipo === 'evaluacion' 
                  ? 'bg-gradient-to-br from-purple-400 to-blue-600' 
                  : 'bg-gradient-to-br from-emerald-400 to-teal-600'"
              >
                <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path 
                    v-if="tipo === 'evaluacion'"
                    stroke-linecap="round" 
                    stroke-linejoin="round" 
                    stroke-width="2" 
                    d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"
                  ></path>
                  <path 
                    v-else
                    stroke-linecap="round" 
                    stroke-linejoin="round" 
                    stroke-width="2" 
                    d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"
                  ></path>
                </svg>
              </div>
              <div>
                <h1 class="text-2xl font-bold bg-gradient-to-r from-purple-400 to-blue-500 bg-clip-text text-transparent">
                  Detalles de {{ tipo === 'evaluacion' ? 'Evaluación' : 'Tarea' }}
                </h1>
                <p class="text-sm text-slate-400">Vista completa de la actividad</p>
              </div>
            </div>
            <div class="flex items-center gap-3">
              <button
                @click="handleEditar"
                class="inline-flex items-center gap-2 rounded-lg px-4 py-2.5 text-sm font-medium transition-all duration-200 hover:scale-105 shadow-lg"
                :class="tipo === 'evaluacion' 
                  ? 'bg-gradient-to-r from-purple-600 to-blue-700 text-white hover:from-purple-500 hover:to-blue-600' 
                  : 'bg-gradient-to-r from-emerald-600 to-teal-700 text-white hover:from-emerald-500 hover:to-teal-600'"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                </svg>
                Editar
              </button>
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
          <div v-if="loading" class="rounded-2xl border border-white/10 bg-slate-950/40 backdrop-blur-md shadow-2xl overflow-hidden">
            <div class="p-8">
              <div class="animate-pulse space-y-6">
                <div class="h-8 w-2/3 rounded bg-slate-700/50"></div>
                <div class="h-4 w-40 rounded bg-slate-800/50"></div>
                <div class="space-y-3">
                  <div class="h-4 w-full rounded bg-slate-800/50"></div>
                  <div class="h-4 w-full rounded bg-slate-800/50"></div>
                  <div class="h-4 w-3/4 rounded bg-slate-800/50"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- Error State -->
          <div v-else-if="errorMessage" class="rounded-2xl border border-red-500/20 bg-red-950/40 backdrop-blur-md shadow-2xl overflow-hidden">
            <div class="p-8 text-center">
              <div class="mx-auto w-20 h-20 rounded-full bg-red-500/20 flex items-center justify-center mb-6">
                <svg class="w-10 h-10 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <h3 class="text-2xl font-bold text-white mb-2">Error</h3>
              <p class="text-red-200 mb-6">{{ errorMessage }}</p>
              <button
                @click="handleVolver"
                class="inline-flex items-center gap-2 rounded-lg bg-slate-700 hover:bg-slate-600 px-6 py-3 text-sm font-medium text-white transition-all duration-200 hover:scale-105"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
                </svg>
                Volver al listado
              </button>
            </div>
          </div>

          <!-- Activity Details -->
          <div v-else-if="actividad" class="space-y-6">
            <!-- Título y Tipo -->
            <div class="rounded-2xl border border-white/10 bg-slate-950/40 backdrop-blur-md shadow-2xl overflow-hidden">
              <div class="p-8">
                <div class="flex items-start justify-between gap-4 mb-4">
                  <div class="flex-grow">
                    <div class="flex items-center gap-3 mb-2">
                      <span 
                        class="inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-medium"
                        :class="tipo === 'evaluacion' 
                          ? 'bg-purple-500/20 text-purple-300 border border-purple-500/30' 
                          : 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'"
                      >
                        <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                          <circle cx="10" cy="10" r="3"></circle>
                        </svg>
                        {{ tipo === 'evaluacion' ? 'Evaluación' : 'Tarea' }}
                      </span>
                      <span class="text-slate-500 text-sm">ID: {{ actividad.id }}</span>
                    </div>
                    <h2 class="text-3xl font-bold text-white mb-2">
                      {{ titulo }}
                    </h2>
                  </div>
                </div>
              </div>
            </div>

            <!-- Contenido/Descripción -->
            <div class="rounded-2xl border border-white/10 bg-slate-950/40 backdrop-blur-md shadow-2xl overflow-hidden">
              <div class="p-8">
                <div class="flex items-center gap-3 mb-6 pb-4 border-b border-white/10">
                  <div class="bg-gradient-to-br from-sky-500/20 to-blue-600/20 p-2 rounded-lg">
                    <svg class="w-6 h-6 text-sky-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h7"></path>
                    </svg>
                  </div>
                  <h3 class="text-xl font-bold text-white">Descripción</h3>
                </div>
                <div class="prose prose-invert max-w-none">
                  <p class="text-slate-300 leading-relaxed whitespace-pre-wrap">{{ contenido }}</p>
                </div>
              </div>
            </div>

            <!-- Código de Prueba (si existe) -->
            <div v-if="hasTest" class="rounded-2xl border border-white/10 bg-slate-950/40 backdrop-blur-md shadow-2xl overflow-hidden">
              <div class="p-8">
                <div class="flex items-center justify-between mb-6 pb-4 border-b border-white/10">
                  <div class="flex items-center gap-3">
                    <div class="bg-gradient-to-br from-green-500/20 to-emerald-600/20 p-2 rounded-lg">
                      <svg class="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path>
                      </svg>
                    </div>
                    <div>
                      <h3 class="text-xl font-bold text-white">Código de Prueba (Pytest)</h3>
                      <p class="text-sm text-slate-400">Código que se ejecutará para evaluar las entregas</p>
                    </div>
                  </div>
                  <span class="inline-flex items-center gap-2 rounded-lg bg-slate-800/50 px-3 py-1.5 text-xs font-medium text-slate-300">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
                    </svg>
                    Python
                  </span>
                </div>
                
                <!-- Code Display -->
                <div class="rounded-lg border border-white/10 bg-slate-900/90 overflow-hidden">
                  <div class="flex items-center justify-between px-4 py-2 bg-slate-800/50 border-b border-white/10">
                    <span class="text-xs font-medium text-slate-400">test_code.py</span>
                    <button
                      @click="copiarCodigo"
                      class="inline-flex items-center gap-1.5 rounded px-2 py-1 text-xs font-medium text-slate-300 hover:bg-slate-700/50 transition-colors"
                      title="Copiar código"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
                      </svg>
                      Copiar
                    </button>
                  </div>
                  <div class="p-4 overflow-x-auto">
                    <pre class="text-sm"><code class="language-python text-slate-200 font-mono">{{ test }}</code></pre>
                  </div>
                </div>
              </div>
            </div>

            <!-- Info adicional si no hay test -->
            <div v-else class="rounded-2xl border border-amber-500/20 bg-amber-950/20 backdrop-blur-md shadow-2xl overflow-hidden">
              <div class="p-6">
                <div class="flex items-start gap-3">
                  <svg class="w-6 h-6 text-amber-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  <div>
                    <h4 class="text-lg font-semibold text-amber-300 mb-1">Sin código de prueba</h4>
                    <p class="text-amber-200/80 text-sm">
                      Esta actividad no incluye código de prueba automatizado. La evaluación será manual.
                    </p>
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
/* Smooth transitions */
* {
  transition-property: color, background-color, border-color, text-decoration-color, fill, stroke, opacity, box-shadow, transform;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}

/* Code styling */
pre {
  margin: 0;
  white-space: pre;
  word-wrap: normal;
}

code {
  display: block;
  line-height: 1.6;
}

/* Prose styling for content */
.prose {
  color: #e2e8f0;
}

.prose p {
  margin-bottom: 1rem;
}

.prose p:last-child {
  margin-bottom: 0;
}
</style>
