<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getUserInfo } from './lti/services/info'
import { getRol } from './lti/interfaces/roles'
import type { UserInfo } from './lti/interfaces/info'

const router = useRouter()
const loadingData = ref(true)
const userInfo = ref<UserInfo | null>(null)
const role = ref<string | null>(null)
const error = ref<string | null>(null)

// Función para navegar a evaluaciones según el rol
const navigateToEvaluaciones = () => {
  if (role.value === 'docente') {
    router.push({ name: 'evaluaciones-docente' })
  } else if (role.value === 'estudiante') {
    router.push({ name: 'evaluaciones-estudiante' })
  } else {
    // Si no hay rol, navega a la ruta genérica
    router.push({ name: 'evaluaciones' })
  }
}

onMounted(async () => {
  // Lee "ltik" de la URL y guárdalo para las peticiones
  const urlParams = new URLSearchParams(window.location.search)
  const ltik = urlParams.get('ltik')
  if (ltik) {
    sessionStorage.setItem('ltik', ltik)
    console.log('ltik recibida')
  }

  try {
    const info = await getUserInfo()
    userInfo.value = info
    role.value = getRol(info.roles)
  } catch (e) {
    console.error(e)
    error.value = 'No se pudo cargar tu información.'
  } finally {
    loadingData.value = false
  }
})
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
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path>
                </svg>
              </div>
              <span class="text-3xl font-bold bg-gradient-to-r from-sky-400 to-blue-500 bg-clip-text text-transparent">
                Edurun
              </span>
            </div>
            <nav class="hidden md:block">
              <div class="flex items-center space-x-2">
                <button 
                  @click="navigateToEvaluaciones"
                  class="rounded-lg px-4 py-2.5 text-sm font-medium text-slate-200 hover:bg-white/10 hover:text-white transition-all duration-200 hover:scale-105 cursor-pointer">
                  <span class="flex items-center gap-2">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
                    </svg>
                    Evaluaciones
                  </span>
                </button>
              </div>
              <div class="hidden md:block w-px h-6 bg-white/10 mx-4">
                <RouterLink 
                  to="/testendpoint" 
                  class="rounded-lg px-4 py-2.5 text-sm font-medium text-slate-200 hover:bg-white/10 hover:text-white transition-all duration-200 hover:scale-105">
                  <span class="flex items-center gap-2">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
                    </svg>
                    testEndpoint
                  </span>
                </RouterLink>
              </div>
            </nav>
          </div>
        </div>
      </header>

      <!-- Main Content -->
      <main class="flex flex-grow items-center justify-center px-4 py-16">
        <div class="mx-auto max-w-4xl w-full">
          <div class="space-y-8 transform transition-all duration-500 ease-in-out">
            <!-- Welcome Section - Always visible -->
            <div class="text-center space-y-4">
              <div class="inline-block">
                <h1 class="text-5xl sm:text-6xl lg:text-7xl font-extrabold">
                  <span class="block text-white drop-shadow-lg">Bienvenido a</span>
                  <span class="block mt-2 bg-gradient-to-r from-sky-400 via-blue-500 to-purple-600 bg-clip-text text-transparent animate-gradient">
                    Edurun
                  </span>
                </h1>
              </div>
              <p class="text-xl text-slate-300 max-w-2xl mx-auto">
                Tu plataforma inteligente de evaluaciones en línea
              </p>
            </div>

            <!-- User Info Card -->
            <div class="rounded-2xl border border-white/10 bg-slate-950/40 backdrop-blur-md shadow-2xl overflow-hidden">
              <!-- Card Header -->
              <div class="bg-gradient-to-r from-sky-600 to-blue-700 px-8 py-6">
                <div class="flex items-center gap-3">
                  <div class="bg-white/20 p-2 rounded-lg">
                    <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                    </svg>
                  </div>
                  <h2 class="text-2xl font-bold text-white">Tu Perfil</h2>
                </div>
              </div>

              <!-- Card Body -->
              <div class="p-8">
                <!-- Error state within card -->
                <div v-if="error" class="rounded-xl border border-red-500/30 bg-gradient-to-br from-red-900/40 to-red-800/20 p-6 backdrop-blur-sm">
                  <div class="flex items-start gap-4">
                    <div class="flex-shrink-0">
                      <svg class="h-6 w-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                      </svg>
                    </div>
                    <div>
                      <h3 class="text-lg font-bold text-red-300">No se pudo cargar la información</h3>
                      <p class="mt-1 text-sm text-red-200">{{ error }}</p>
                    </div>
                  </div>
                </div>

                <!-- Data cards - Show loading or data -->
                <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <!-- User ID Card -->
                  <div class="group relative overflow-hidden rounded-xl bg-gradient-to-br from-slate-800/50 to-slate-900/50 p-6 border border-white/5 hover:border-sky-500/50 transition-all duration-300 hover:shadow-lg hover:shadow-sky-500/20">
                    <div class="absolute top-0 right-0 w-32 h-32 bg-sky-500/10 rounded-full blur-2xl group-hover:bg-sky-500/20 transition-all duration-300"></div>
                    <div class="relative">
                      <div class="flex items-center gap-2 mb-3">
                        <svg class="w-5 h-5 text-sky-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V8a2 2 0 00-2-2h-5m-4 0V5a2 2 0 114 0v1m-4 0a2 2 0 104 0m-5 8a2 2 0 100-4 2 2 0 000 4zm0 0c1.306 0 2.417.835 2.83 2M9 14a3.001 3.001 0 00-2.83 2M15 11h3m-3 4h2"></path>
                        </svg>
                        <dt class="text-sm font-medium text-slate-400 uppercase tracking-wider">ID de Usuario</dt>
                      </div>
                      
                      <!-- Loading skeleton or data -->
                      <dd v-if="loadingData" class="animate-pulse">
                        <div class="h-8 bg-slate-700/50 rounded w-3/4"></div>
                      </dd>
                      <dd v-else class="text-2xl font-bold text-white break-all">
                        {{ userInfo?.userId || 'No disponible' }}
                      </dd>
                    </div>
                  </div>

                  <!-- Role Card -->
                  <div class="group relative overflow-hidden rounded-xl bg-gradient-to-br from-blue-800/50 to-purple-900/50 p-6 border border-white/5 hover:border-purple-500/50 transition-all duration-300 hover:shadow-lg hover:shadow-purple-500/20">
                    <div class="absolute top-0 right-0 w-32 h-32 bg-purple-500/10 rounded-full blur-2xl group-hover:bg-purple-500/20 transition-all duration-300"></div>
                    <div class="relative">
                      <div class="flex items-center gap-2 mb-3">
                        <svg class="w-5 h-5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"></path>
                        </svg>
                        <dt class="text-sm font-medium text-slate-400 uppercase tracking-wider">Rol</dt>
                      </div>
                      
                      <!-- Loading skeleton or data -->
                      <dd v-if="loadingData" class="animate-pulse">
                        <div class="flex items-center gap-2">
                          <div class="h-10 bg-purple-700/50 rounded w-32"></div>
                          <div class="h-6 bg-purple-700/50 rounded-full w-16"></div>
                        </div>
                      </dd>
                      <dd v-else class="flex items-center gap-2">
                        <span class="text-3xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
                          {{ role || 'Desconocido' }}
                        </span>
                        <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-purple-500/20 text-purple-300 border border-purple-500/30">
                          Activo
                        </span>
                      </dd>
                    </div>
                  </div>
                </div>

                <!-- Additional Info Section -->
                <div class="mt-8 pt-6 border-t border-white/10">
                  <div class="flex items-center justify-between">
                    <div class="flex items-center gap-2 text-sm text-slate-400">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                      </svg>
                      <span v-if="loadingData">Verificando sesión...</span>
                      <span v-else>Sesión verificada</span>
                    </div>
                    <div class="flex items-center gap-2 text-sm text-slate-400">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                      </svg>
                      <span>{{ new Date().toLocaleDateString('es-ES', { year: 'numeric', month: 'long', day: 'numeric' }) }}</span>
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
