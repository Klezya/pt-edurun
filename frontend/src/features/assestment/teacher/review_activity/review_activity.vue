<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const userId = ref<string>('')
const assessmentId = ref<string>('')
const loading = ref(true)

onMounted(async () => {
  try {
    // Obtener user_id de los parámetros de la URL
    userId.value = route.query.user_id as string || ''
    assessmentId.value = route.query.assessment_id as string || ''
    
    if (!userId.value) {
      console.warn('No se encontró user_id en los parámetros de URL')
    }
  } catch (error) {
    console.error('Error al cargar la información:', error)
  } finally {
    loading.value = false
  }
})

function handleVolver() {
  router.back()
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
      <header class="border-b border-white/10 bg-slate-950/30 backdrop-blur-sm">
        <div class="mx-auto max-w-7xl px-4 py-6">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-4">
              <div class="bg-gradient-to-br from-purple-500/20 to-blue-600/20 p-3 rounded-xl">
                <svg class="w-8 h-8 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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
          <div v-if="loading" class="rounded-2xl border border-white/10 bg-slate-950/40 backdrop-blur-md shadow-2xl overflow-hidden">
            <div class="p-8">
              <div class="animate-pulse space-y-6">
                <div class="h-8 w-2/3 rounded bg-slate-700/50"></div>
                <div class="h-4 w-40 rounded bg-slate-800/50"></div>
              </div>
            </div>
          </div>

          <!-- Content -->
          <div v-else class="space-y-6">
            <!-- User ID Card -->
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
                  <div v-else class="flex items-center gap-3 p-4 rounded-lg bg-amber-500/10 border border-amber-500/20">
                    <svg class="w-6 h-6 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
                    </svg>
                    <div>
                      <h4 class="text-lg font-semibold text-amber-300 mb-1">ID de usuario no encontrado</h4>
                      <p class="text-amber-200/80 text-sm">
                        No se encontró el parámetro user_id en la URL
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Review Message Card -->
            <div class="rounded-2xl border border-white/10 bg-slate-950/40 backdrop-blur-md shadow-2xl overflow-hidden">
              <div class="p-8">
                <div class="flex items-center gap-3 mb-6 pb-4 border-b border-white/10">
                  <div class="bg-gradient-to-br from-green-500/20 to-emerald-600/20 p-2 rounded-lg">
                    <svg class="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                  </div>
                  <h3 class="text-xl font-bold text-white">Estado de Revisión</h3>
                </div>
                <div class="text-center py-8">
                  <p class="text-2xl font-semibold text-slate-200">
                    🎓 Estás revisando la evaluación
                  </p>
                  <p class="text-slate-400 mt-2">
                    La funcionalidad de revisión completa estará disponible próximamente
                  </p>
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
