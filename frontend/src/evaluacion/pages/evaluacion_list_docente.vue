<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getUserInfo } from '@/lti/services/info'
import { getRol } from '@/lti/interfaces/roles'

const userName = ref<string>('')
const loading = ref(true)

onMounted(async () => {
  try {
    const info = await getUserInfo()
    userName.value = info.userId
  } catch (error) {
    console.error('Error al obtener información del usuario:', error)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center px-4">
    <!-- Decorative background elements -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-20 left-10 w-72 h-72 bg-purple-500/10 rounded-full blur-3xl"></div>
      <div class="absolute bottom-20 right-10 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl"></div>
    </div>

    <div class="relative max-w-2xl w-full">
      <div class="rounded-2xl border border-white/10 bg-slate-950/40 backdrop-blur-md shadow-2xl overflow-hidden">
        <!-- Header -->
        <div class="bg-gradient-to-r from-purple-600 to-blue-700 px-8 py-6">
          <div class="flex items-center gap-3">
            <div class="bg-white/20 p-3 rounded-lg">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
              </svg>
            </div>
            <h1 class="text-3xl font-bold text-white">Panel de Evaluaciones</h1>
          </div>
        </div>

        <!-- Body -->
        <div class="p-12">
          <div v-if="loading" class="text-center">
            <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-purple-500"></div>
            <p class="mt-4 text-slate-300">Cargando...</p>
          </div>

          <div v-else class="text-center space-y-6">
            <!-- Role Badge -->
            <div class="inline-flex items-center justify-center">
              <div class="relative">
                <div class="absolute inset-0 bg-purple-500 blur-xl opacity-50"></div>
                <div class="relative bg-gradient-to-r from-purple-600 to-purple-700 px-8 py-4 rounded-2xl border border-purple-400/30">
                  <div class="flex items-center gap-3">
                    <svg class="w-6 h-6 text-purple-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                    </svg>
                    <span class="text-2xl font-bold text-white">Docente</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Welcome Message -->
            <div class="space-y-3">
              <h2 class="text-4xl font-extrabold">
                <span class="bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
                  Logueado como Docente
                </span>
              </h2>
              
              <div class="flex items-center justify-center gap-2 text-slate-300">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                </svg>
                <p class="text-lg">{{ userName }}</p>
              </div>
            </div>

            <!-- Info Card -->
            <div class="mt-8 rounded-xl bg-gradient-to-br from-slate-800/50 to-slate-900/50 p-6 border border-white/5">
              <div class="flex items-start gap-4">
                <div class="flex-shrink-0">
                  <svg class="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                </div>
                <div class="text-left">
                  <h3 class="text-lg font-semibold text-white mb-1">Vista de Docente</h3>
                  <p class="text-sm text-slate-400">
                    Has iniciado sesión con permisos de docente. Aquí podrás gestionar y crear evaluaciones para tus estudiantes.
                  </p>
                </div>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="flex gap-4 justify-center mt-8">
              <RouterLink 
                to="/"
                class="inline-flex items-center gap-2 rounded-lg bg-slate-700 hover:bg-slate-600 px-6 py-3 text-sm font-medium text-white transition-all duration-200 hover:scale-105">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
                </svg>
                Volver al inicio
              </RouterLink>
            </div>
          </div>
        </div>
      </div>
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
</style>
