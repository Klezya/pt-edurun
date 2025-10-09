<script setup lang="ts">
import { ref } from 'vue'
import { getUserInfo, getCourseInfo, getPlatformInfo, getAssignmentInfo } from '../services/info'
import type { UserInfo, CourseInfo, PlatformInfo } from '../interfaces/info'
import { isUserRegistered } from '../services/lti_fastapi'

// Estados de carga
const loadingUser = ref(false)
const loadingCourse = ref(false)
const loadingPlatform = ref(false)
const loadingUserRegistered = ref(false)
const loadingAssignment = ref(false)

// Datos
const userInfo = ref<UserInfo | null>(null)
const courseInfo = ref<CourseInfo | null>(null)
const platformInfo = ref<PlatformInfo | null>(null)
const userRegisteredData = ref<any>(null)
const assignmentInfo = ref<any>(null)

// Input para userIdLms
const userIdLmsInput = ref('')

// Errores
const errorUser = ref<string | null>(null)
const errorCourse = ref<string | null>(null)
const errorPlatform = ref<string | null>(null)
const errorUserRegistered = ref<string | null>(null)
const errorAssignment = ref<string | null>(null)

// Función para copiar JSON al portapapeles
const copyToClipboard = (text: string) => {
  navigator.clipboard.writeText(text)
}

// Función para formatear JSON
const formatJSON = (obj: any) => {
  return JSON.stringify(obj, null, 2)
}

// Funciones de prueba
const testUserInfo = async () => {
  loadingUser.value = true
  errorUser.value = null
  userInfo.value = null
  
  try {
    const data = await getUserInfo()
    userInfo.value = data
  } catch (e: any) {
    errorUser.value = e.message || 'Error al obtener información del usuario'
  } finally {
    loadingUser.value = false
  }
}

const testCourseInfo = async () => {
  loadingCourse.value = true
  errorCourse.value = null
  courseInfo.value = null
  
  try {
    const data = await getCourseInfo()
    courseInfo.value = data
  } catch (e: any) {
    errorCourse.value = e.message || 'Error al obtener información del curso'
  } finally {
    loadingCourse.value = false
  }
}

const testPlatformInfo = async () => {
  loadingPlatform.value = true
  errorPlatform.value = null
  platformInfo.value = null
  
  try {
    const data = await getPlatformInfo()
    platformInfo.value = data
  } catch (e: any) {
    errorPlatform.value = e.message || 'Error al obtener información de la plataforma'
  } finally {
    loadingPlatform.value = false
  }
}

const testUserRegistered = async () => {
  if (!userIdLmsInput.value.trim()) {
    errorUserRegistered.value = 'Por favor ingresa un User ID LMS'
    return
  }
  
  loadingUserRegistered.value = true
  errorUserRegistered.value = null
  userRegisteredData.value = null
  
  try {
    const data = await isUserRegistered(userIdLmsInput.value.trim())
    userRegisteredData.value = data
  } catch (e: any) {
    errorUserRegistered.value = e.message || 'Error al verificar si el usuario está registrado'
  } finally {
    loadingUserRegistered.value = false
  }
}

const testAssignmentInfo = async () => {
  loadingAssignment.value = true
  errorAssignment.value = null
  assignmentInfo.value = null
  
  try {
    const data = await getAssignmentInfo()
    assignmentInfo.value = data
  } catch (e: any) {
    errorAssignment.value = e.message || 'Error al obtener información de la asignación'
  } finally {
    loadingAssignment.value = false
  }
}

const testAllEndpoints = async () => {
  await Promise.all([
    testUserInfo(),
    testCourseInfo(),
    testPlatformInfo(),
    testAssignmentInfo()
  ])
}

const clearAll = () => {
  userInfo.value = null
  courseInfo.value = null
  platformInfo.value = null
  userRegisteredData.value = null
  assignmentInfo.value = null
  errorUser.value = null
  errorCourse.value = null
  errorPlatform.value = null
  errorUserRegistered.value = null
  errorAssignment.value = null
  userIdLmsInput.value = ''
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 via-indigo-900 to-slate-900">
    <!-- Background decoration -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-20 left-10 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl"></div>
      <div class="absolute bottom-20 right-10 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl"></div>
    </div>

    <div class="relative min-h-screen">
      <!-- Header -->
      <header class="border-b border-white/10 bg-slate-950/30 backdrop-blur-md shadow-lg">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div class="flex h-20 items-center justify-between">
            <div class="flex items-center gap-4">
              <div class="bg-gradient-to-br from-indigo-500 to-purple-600 p-2.5 rounded-xl shadow-lg">
                <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z"></path>
                </svg>
              </div>
              <div>
                <h1 class="text-2xl font-bold text-white">LTI Endpoints Tester</h1>
                <p class="text-sm text-slate-400">Prueba los servicios de LTI</p>
              </div>
            </div>
            
            <div class="flex items-center gap-3">
              <RouterLink 
                to="/"
                class="rounded-lg px-4 py-2 text-sm font-medium text-slate-300 hover:text-white hover:bg-white/10 transition-all">
                <span class="flex items-center gap-2">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
                  </svg>
                  Volver
                </span>
              </RouterLink>
            </div>
          </div>
        </div>
      </header>

      <!-- Main Content -->
      <main class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
        <!-- Control Panel -->
        <div class="mb-8 rounded-2xl border border-white/10 bg-slate-950/40 backdrop-blur-md p-6 shadow-xl">
          <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <div>
              <h2 class="text-xl font-bold text-white flex items-center gap-2">
                <svg class="w-6 h-6 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                </svg>
                Panel de Control
              </h2>
              <p class="text-sm text-slate-400 mt-1">Ejecuta las pruebas de los endpoints</p>
            </div>
            
            <div class="flex flex-wrap gap-3">
              <button
                @click="testAllEndpoints"
                :disabled="loadingUser || loadingCourse || loadingPlatform || loadingAssignment"
                class="rounded-lg bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 px-6 py-2.5 text-sm font-semibold text-white shadow-lg hover:shadow-indigo-500/50 transition-all duration-200 hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100">
                <span class="flex items-center gap-2">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"></path>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  Probar Todo
                </span>
              </button>
              
              <button
                @click="clearAll"
                class="rounded-lg bg-slate-700 hover:bg-slate-600 px-6 py-2.5 text-sm font-semibold text-white transition-all duration-200 hover:scale-105">
                <span class="flex items-center gap-2">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                  </svg>
                  Limpiar
                </span>
              </button>
            </div>
          </div>
        </div>

        <!-- Endpoints Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <!-- User Info Endpoint -->
          <div class="rounded-2xl border border-white/10 bg-slate-950/40 backdrop-blur-md shadow-xl overflow-hidden">
            <div class="bg-gradient-to-r from-blue-600 to-cyan-600 px-6 py-4">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-3">
                  <div class="bg-white/20 p-2 rounded-lg">
                    <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                    </svg>
                  </div>
                  <div>
                    <h3 class="text-lg font-bold text-white">User Info</h3>
                    <p class="text-xs text-blue-100">/info/user</p>
                  </div>
                </div>
              </div>
            </div>

            <div class="p-6 space-y-4">
              <button
                @click="testUserInfo"
                :disabled="loadingUser"
                class="w-full rounded-lg bg-blue-600 hover:bg-blue-500 px-4 py-3 text-sm font-semibold text-white transition-all duration-200 hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100">
                <span v-if="loadingUser" class="flex items-center justify-center gap-2">
                  <svg class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
                  </svg>
                  Cargando...
                </span>
                <span v-else class="flex items-center justify-center gap-2">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"></path>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  Ejecutar
                </span>
              </button>

              <!-- Error State -->
              <div v-if="errorUser" class="rounded-lg bg-red-900/30 border border-red-500/50 p-4">
                <div class="flex items-start gap-2">
                  <svg class="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  <p class="text-sm text-red-300">{{ errorUser }}</p>
                </div>
              </div>

              <!-- Success State -->
              <div v-if="userInfo && !errorUser" class="space-y-3">
                <div class="flex items-center justify-between">
                  <span class="text-sm font-medium text-emerald-400 flex items-center gap-2">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    Respuesta exitosa
                  </span>
                  <button
                    @click="copyToClipboard(formatJSON(userInfo))"
                    class="text-slate-400 hover:text-white transition-colors"
                    title="Copiar JSON">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
                    </svg>
                  </button>
                </div>
                <pre class="bg-slate-900/60 rounded-lg p-4 text-xs text-slate-300 overflow-x-auto border border-white/5">{{ formatJSON(userInfo) }}</pre>
              </div>
            </div>
          </div>

          <!-- Course Info Endpoint -->
          <div class="rounded-2xl border border-white/10 bg-slate-950/40 backdrop-blur-md shadow-xl overflow-hidden">
            <div class="bg-gradient-to-r from-purple-600 to-pink-600 px-6 py-4">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-3">
                  <div class="bg-white/20 p-2 rounded-lg">
                    <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
                    </svg>
                  </div>
                  <div>
                    <h3 class="text-lg font-bold text-white">Course Info</h3>
                    <p class="text-xs text-purple-100">/info/course</p>
                  </div>
                </div>
              </div>
            </div>

            <div class="p-6 space-y-4">
              <button
                @click="testCourseInfo"
                :disabled="loadingCourse"
                class="w-full rounded-lg bg-purple-600 hover:bg-purple-500 px-4 py-3 text-sm font-semibold text-white transition-all duration-200 hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100">
                <span v-if="loadingCourse" class="flex items-center justify-center gap-2">
                  <svg class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
                  </svg>
                  Cargando...
                </span>
                <span v-else class="flex items-center justify-center gap-2">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"></path>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  Ejecutar
                </span>
              </button>

              <!-- Error State -->
              <div v-if="errorCourse" class="rounded-lg bg-red-900/30 border border-red-500/50 p-4">
                <div class="flex items-start gap-2">
                  <svg class="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  <p class="text-sm text-red-300">{{ errorCourse }}</p>
                </div>
              </div>

              <!-- Success State -->
              <div v-if="courseInfo && !errorCourse" class="space-y-3">
                <div class="flex items-center justify-between">
                  <span class="text-sm font-medium text-emerald-400 flex items-center gap-2">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    Respuesta exitosa
                  </span>
                  <button
                    @click="copyToClipboard(formatJSON(courseInfo))"
                    class="text-slate-400 hover:text-white transition-colors"
                    title="Copiar JSON">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
                    </svg>
                  </button>
                </div>
                <pre class="bg-slate-900/60 rounded-lg p-4 text-xs text-slate-300 overflow-x-auto border border-white/5">{{ formatJSON(courseInfo) }}</pre>
              </div>
            </div>
          </div>

          <!-- Platform Info Endpoint -->
          <div class="rounded-2xl border border-white/10 bg-slate-950/40 backdrop-blur-md shadow-xl overflow-hidden">
            <div class="bg-gradient-to-r from-emerald-600 to-teal-600 px-6 py-4">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-3">
                  <div class="bg-white/20 p-2 rounded-lg">
                    <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2m-2-4h.01M17 16h.01"></path>
                    </svg>
                  </div>
                  <div>
                    <h3 class="text-lg font-bold text-white">Platform Info</h3>
                    <p class="text-xs text-emerald-100">/info/platform</p>
                  </div>
                </div>
              </div>
            </div>

            <div class="p-6 space-y-4">
              <button
                @click="testPlatformInfo"
                :disabled="loadingPlatform"
                class="w-full rounded-lg bg-emerald-600 hover:bg-emerald-500 px-4 py-3 text-sm font-semibold text-white transition-all duration-200 hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100">
                <span v-if="loadingPlatform" class="flex items-center justify-center gap-2">
                  <svg class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
                  </svg>
                  Cargando...
                </span>
                <span v-else class="flex items-center justify-center gap-2">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"></path>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  Ejecutar
                </span>
              </button>

              <!-- Error State -->
              <div v-if="errorPlatform" class="rounded-lg bg-red-900/30 border border-red-500/50 p-4">
                <div class="flex items-start gap-2">
                  <svg class="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  <p class="text-sm text-red-300">{{ errorPlatform }}</p>
                </div>
              </div>

              <!-- Success State -->
              <div v-if="platformInfo && !errorPlatform" class="space-y-3">
                <div class="flex items-center justify-between">
                  <span class="text-sm font-medium text-emerald-400 flex items-center gap-2">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    Respuesta exitosa
                  </span>
                  <button
                    @click="copyToClipboard(formatJSON(platformInfo))"
                    class="text-slate-400 hover:text-white transition-colors"
                    title="Copiar JSON">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
                    </svg>
                  </button>
                </div>
                <pre class="bg-slate-900/60 rounded-lg p-4 text-xs text-slate-300 overflow-x-auto border border-white/5">{{ formatJSON(platformInfo) }}</pre>
              </div>
            </div>
          </div>

          <!-- Assignment Info Endpoint -->
          <div class="rounded-2xl border border-white/10 bg-slate-950/40 backdrop-blur-md shadow-xl overflow-hidden">
            <div class="bg-gradient-to-r from-rose-600 to-red-600 px-6 py-4">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-3">
                  <div class="bg-white/20 p-2 rounded-lg">
                    <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                    </svg>
                  </div>
                  <div>
                    <h3 class="text-lg font-bold text-white">Assignment Info</h3>
                    <p class="text-xs text-rose-100">/info/assignment</p>
                  </div>
                </div>
              </div>
            </div>

            <div class="p-6 space-y-4">
              <button
                @click="testAssignmentInfo"
                :disabled="loadingAssignment"
                class="w-full rounded-lg bg-rose-600 hover:bg-rose-500 px-4 py-3 text-sm font-semibold text-white transition-all duration-200 hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100">
                <span v-if="loadingAssignment" class="flex items-center justify-center gap-2">
                  <svg class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
                  </svg>
                  Cargando...
                </span>
                <span v-else class="flex items-center justify-center gap-2">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"></path>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  Ejecutar
                </span>
              </button>

              <!-- Error State -->
              <div v-if="errorAssignment" class="rounded-lg bg-red-900/30 border border-red-500/50 p-4">
                <div class="flex items-start gap-2">
                  <svg class="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  <p class="text-sm text-red-300">{{ errorAssignment }}</p>
                </div>
              </div>

              <!-- Success State -->
              <div v-if="assignmentInfo && !errorAssignment" class="space-y-3">
                <div class="flex items-center justify-between">
                  <span class="text-sm font-medium text-emerald-400 flex items-center gap-2">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    Respuesta exitosa
                  </span>
                  <button
                    @click="copyToClipboard(formatJSON(assignmentInfo))"
                    class="text-slate-400 hover:text-white transition-colors"
                    title="Copiar JSON">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
                    </svg>
                  </button>
                </div>
                <pre class="bg-slate-900/60 rounded-lg p-4 text-xs text-slate-300 overflow-x-auto border border-white/5">{{ formatJSON(assignmentInfo) }}</pre>
              </div>
            </div>
          </div>
        </div>

        <!-- User Registered Check Section -->
        <div class="mt-6">
          <div class="rounded-2xl border border-white/10 bg-slate-950/40 backdrop-blur-md shadow-xl overflow-hidden">
            <div class="bg-gradient-to-r from-amber-600 to-orange-600 px-6 py-4">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-3">
                  <div class="bg-white/20 p-2 rounded-lg">
                    <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
                    </svg>
                  </div>
                  <div>
                    <h3 class="text-lg font-bold text-white">Check User Registered</h3>
                    <p class="text-xs text-amber-100">/lti/check_user/:userIdLms</p>
                  </div>
                </div>
              </div>
            </div>

            <div class="p-6 space-y-4">
              <!-- Input for User ID LMS -->
              <div class="space-y-2">
                <label for="userIdLms" class="block text-sm font-medium text-slate-300">
                  User ID LMS
                </label>
                <input
                  id="userIdLms"
                  v-model="userIdLmsInput"
                  type="text"
                  placeholder="Ingresa el User ID LMS"
                  class="w-full rounded-lg bg-slate-900/60 border border-white/10 px-4 py-3 text-white placeholder-slate-500 focus:border-amber-500 focus:outline-none focus:ring-2 focus:ring-amber-500/20 transition-all"
                  @keyup.enter="testUserRegistered"
                />
              </div>

              <button
                @click="testUserRegistered"
                :disabled="loadingUserRegistered || !userIdLmsInput.trim()"
                class="w-full rounded-lg bg-amber-600 hover:bg-amber-500 px-4 py-3 text-sm font-semibold text-white transition-all duration-200 hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100">
                <span v-if="loadingUserRegistered" class="flex items-center justify-center gap-2">
                  <svg class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
                  </svg>
                  Verificando...
                </span>
                <span v-else class="flex items-center justify-center gap-2">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
                  </svg>
                  Verificar Usuario
                </span>
              </button>

              <!-- Error State -->
              <div v-if="errorUserRegistered" class="rounded-lg bg-red-900/30 border border-red-500/50 p-4">
                <div class="flex items-start gap-2">
                  <svg class="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  <p class="text-sm text-red-300">{{ errorUserRegistered }}</p>
                </div>
              </div>

              <!-- Success State -->
              <div v-if="userRegisteredData && !errorUserRegistered" class="space-y-3">
                <div class="flex items-center justify-between">
                  <span class="text-sm font-medium text-emerald-400 flex items-center gap-2">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    Respuesta exitosa
                  </span>
                  <button
                    @click="copyToClipboard(formatJSON(userRegisteredData))"
                    class="text-slate-400 hover:text-white transition-colors"
                    title="Copiar JSON">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
                    </svg>
                  </button>
                </div>
                <pre class="bg-slate-900/60 rounded-lg p-4 text-xs text-slate-300 overflow-x-auto border border-white/5">{{ formatJSON(userRegisteredData) }}</pre>
              </div>
            </div>
          </div>
        </div>

        <!-- Info Section -->
        <div class="mt-8 rounded-2xl border border-white/10 bg-slate-950/40 backdrop-blur-md p-6 shadow-xl">
          <div class="flex items-start gap-4">
            <div class="bg-blue-500/20 p-2 rounded-lg">
              <svg class="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <div class="flex-1">
              <h3 class="text-lg font-bold text-white mb-2">Información de uso</h3>
              <ul class="space-y-2 text-sm text-slate-300">
                <li class="flex items-start gap-2">
                  <svg class="w-4 h-4 text-blue-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  <span>Asegúrate de tener un token LTI válido en sessionStorage</span>
                </li>
                <li class="flex items-start gap-2">
                  <svg class="w-4 h-4 text-blue-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  <span>Puedes probar cada endpoint individualmente o todos a la vez (excepto Check User Registered)</span>
                </li>
                <li class="flex items-start gap-2">
                  <svg class="w-4 h-4 text-blue-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  <span>El botón "Probar Todo" ejecutará User Info, Course Info, Platform Info y Assignment Info simultáneamente</span>
                </li>
                <li class="flex items-start gap-2">
                  <svg class="w-4 h-4 text-blue-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  <span>Para "Check User Registered", ingresa un User ID LMS en el campo de texto y presiona Enter o el botón</span>
                </li>
                <li class="flex items-start gap-2">
                  <svg class="w-4 h-4 text-blue-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  <span>Haz clic en el icono de copiar para copiar la respuesta JSON al portapapeles</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<style scoped>
/* Smooth scroll */
html {
  scroll-behavior: smooth;
}
</style>
