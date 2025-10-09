<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import type { Evaluacion } from '../interfaces/evaluacion'

const router = useRouter()

// Form data
const formData = ref({
  id_curso: null as number | null,
  titulo: '',
  contenido: '',
  fecha_limite: '',
  test: ''
})

const isSubmitting = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

const handleSubmit = async () => {
  errorMessage.value = ''
  successMessage.value = ''

  // Validate required fields
  if (!formData.value.id_curso || !formData.value.titulo || !formData.value.contenido) {
    errorMessage.value = 'Por favor complete todos los campos obligatorios'
    return
  }

  isSubmitting.value = true

  try {
    // Prepare the data to send
    const evaluacionData: Partial<Evaluacion> = {
      id_curso: formData.value.id_curso,
      titulo: formData.value.titulo,
      contenido: formData.value.contenido,
      fecha_limite: formData.value.fecha_limite || undefined,
      test: formData.value.test || undefined,
      // fecha_registro will be set by the backend
    }

    // TODO: Add the actual API call here
    // Example:
    // const response = await createEvaluacion(evaluacionData)
    
    console.log('Datos de evaluación a enviar:', evaluacionData)
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    successMessage.value = 'Evaluación creada exitosamente'
    
    // Reset form after successful submission
    setTimeout(() => {
      handleCancel()
    }, 2000)

  } catch (error) {
    console.error('Error al crear evaluación:', error)
    errorMessage.value = error instanceof Error ? error.message : 'Error al crear la evaluación'
  } finally {
    isSubmitting.value = false
  }
}

const handleCancel = () => {
  // Reset form
  formData.value = {
    id_curso: null,
    titulo: '',
    contenido: '',
    fecha_limite: '',
    test: ''
  }
  errorMessage.value = ''
  successMessage.value = ''
  
  // Navigate back or to list
  router.back()
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
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
                </svg>
              </div>
              <div>
                <h1 class="text-2xl font-bold bg-gradient-to-r from-sky-400 to-blue-500 bg-clip-text text-transparent">
                  Crear Nueva Evaluación
                </h1>
                <p class="text-sm text-slate-400">Completa los datos de la evaluación</p>
              </div>
            </div>
            <div class="flex items-center gap-3">
              <button
                @click="handleCancel"
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
      <main class="flex flex-grow items-center justify-center px-4 py-8">
        <div class="mx-auto max-w-4xl w-full">
          <!-- Success Message -->
          <div v-if="successMessage" class="mb-6 rounded-xl border border-green-500/20 bg-green-950/40 backdrop-blur-md p-4">
            <div class="flex items-center gap-3">
              <svg class="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              <p class="text-green-200 font-medium">{{ successMessage }}</p>
            </div>
          </div>

          <!-- Error Message -->
          <div v-if="errorMessage" class="mb-6 rounded-xl border border-red-500/20 bg-red-950/40 backdrop-blur-md p-4">
            <div class="flex items-center gap-3">
              <svg class="w-6 h-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              <p class="text-red-200 font-medium">{{ errorMessage }}</p>
            </div>
          </div>

          <!-- Form Card -->
          <div class="rounded-2xl border border-white/10 bg-slate-950/40 backdrop-blur-md shadow-2xl overflow-hidden">
            <form @submit.prevent="handleSubmit" class="p-8 space-y-6">
                <!-- Título -->
              <div class="space-y-2">
                <label for="titulo" class="block text-sm font-medium text-slate-200">
                  Título <span class="text-red-400">*</span>
                </label>
                <input
                  id="titulo"
                  v-model="formData.titulo"
                  type="text"
                  required
                  placeholder="Ingrese el título de la evaluación"
                  class="w-full rounded-lg border border-white/10 bg-slate-900/50 px-4 py-3 text-slate-100 placeholder:text-slate-500 focus:border-sky-500/50 focus:outline-none focus:ring-2 focus:ring-sky-500/20 transition-all"
                />
              </div>

                <!-- Contenido -->
              <div class="space-y-2">
                <label for="contenido" class="block text-sm font-medium text-slate-200">
                  Contenido <span class="text-red-400">*</span>
                </label>
                <textarea
                  id="contenido"
                  v-model="formData.contenido"
                  rows="8"
                  required
                  placeholder="Ingrese la descripción y detalles de la evaluación"
                  class="w-full rounded-lg border border-white/10 bg-slate-900/50 px-4 py-3 text-slate-100 placeholder:text-slate-500 focus:border-sky-500/50 focus:outline-none focus:ring-2 focus:ring-sky-500/20 transition-all resize-vertical"
                ></textarea>
              </div>

              <!-- Fecha Límite -->
              <div class="space-y-2">
                <label for="fecha_limite" class="block text-sm font-medium text-slate-200">
                  Fecha Límite
                </label>
                <input
                  id="fecha_limite"
                  v-model="formData.fecha_limite"
                  type="datetime-local"
                  class="w-full rounded-lg border border-white/10 bg-slate-900/50 px-4 py-3 text-slate-100 placeholder:text-slate-500 focus:border-sky-500/50 focus:outline-none focus:ring-2 focus:ring-sky-500/20 transition-all"
                />
              </div>

              <!-- Test (Código Pytest) -->
              <div class="space-y-2">
                <label for="test" class="block text-sm font-medium text-slate-200">
                  Código de Prueba (Pytest)
                  <span class="text-slate-500 text-xs ml-2">(opcional)</span>
                </label>
                <textarea
                  id="test"
                  v-model="formData.test"
                  rows="10"
                  placeholder="Ingrese el código de pytest para evaluar las tareas&#10;Ejemplo:&#10;def test_example():&#10;    assert 1 + 1 == 2"
                  class="w-full rounded-lg border border-white/10 bg-slate-900/50 px-4 py-3 text-slate-100 placeholder:text-slate-500 focus:border-sky-500/50 focus:outline-none focus:ring-2 focus:ring-sky-500/20 transition-all resize-vertical font-mono text-sm"
                ></textarea>
                <p class="text-slate-400 text-xs flex items-center gap-1">
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  Escriba el código de prueba que se ejecutará para evaluar las tareas de los estudiantes
                </p>
              </div>

              <!-- Form Actions -->
              <div class="flex items-center justify-end gap-4 pt-6 border-t border-white/10">
                <button
                  type="button"
                  @click="handleCancel"
                  class="rounded-lg px-6 py-3 text-sm font-medium text-slate-200 hover:bg-white/10 transition-all duration-200 hover:scale-105"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  :disabled="isSubmitting"
                  class="inline-flex items-center gap-2 rounded-lg bg-gradient-to-r from-sky-500 to-blue-600 px-6 py-3 text-sm font-medium text-white shadow-lg shadow-sky-500/30 transition-all duration-200 hover:scale-105 hover:shadow-sky-500/50 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
                >
                  <svg v-if="isSubmitting" class="w-5 h-5 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                  </svg>
                  <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                  {{ isSubmitting ? 'Creando...' : 'Crear Evaluación' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>



<style scoped>
/* Este componente usa Tailwind CSS, sin estilos personalizados adicionales */
</style>
