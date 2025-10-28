<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

// CodeMirror imports
import { EditorView, basicSetup } from 'codemirror'
import { python } from '@codemirror/lang-python'
import { oneDark } from '@codemirror/theme-one-dark'

// Servicios
import { updateEvaluacion, updateTarea } from './edit_activity.service'
import { getEvaluacion, getTarea } from '../../shared'
import type { Actividad } from '../../shared/activity.types'

const router = useRouter()
const route = useRoute()

const formData = ref({
  titulo: '',
  contenido: '',
  test: '',
  tipo: 'tarea' as 'tarea' | 'evaluacion'
})

const isSubmitting = ref(false)
const isLoading = ref(true)
const errorMessage = ref('')
const successMessage = ref('')
const activityId = ref<number>(0)

// CodeMirror
const editorContainer = ref<HTMLElement | null>(null)
let editorView: EditorView | null = null

onMounted(async () => {
  try {
    activityId.value = Number(route.params.id)
    formData.value.tipo = route.params.tipo as 'evaluacion' | 'tarea'

    if (isNaN(activityId.value)) {
      errorMessage.value = 'ID de actividad inválido'
      isLoading.value = false
      return
    }

    // Cargar datos de la actividad
    let actividad: Actividad
    if (formData.value.tipo === 'evaluacion') {
      actividad = await getEvaluacion(activityId.value)
    } else {
      actividad = await getTarea(activityId.value)
    }

    // Rellenar formulario
    formData.value.titulo = actividad.titulo
    formData.value.contenido = actividad.contenido
    formData.value.test = actividad.test || ''

  } catch (error) {
    console.error('Error al cargar la actividad:', error)
    errorMessage.value = 'Error al cargar los datos de la actividad'
  } finally {
    isLoading.value = false
    
    // Inicializar CodeMirror después de que el componente esté completamente montado
    // Usamos nextTick para asegurar que el DOM esté listo
    await new Promise(resolve => setTimeout(resolve, 100))
    
    if (editorContainer.value && !errorMessage.value) {
      editorView = new EditorView({
        doc: formData.value.test || '',
        extensions: [
          basicSetup,
          python(),
          oneDark,
          EditorView.updateListener.of((update) => {
            if (update.docChanged) {
              formData.value.test = update.state.doc.toString()
            }
          }),
        ],
        parent: editorContainer.value,
      })
    }
  }
})

const handleSubmit = async () => {
  errorMessage.value = ''
  successMessage.value = ''

  if (!formData.value.titulo || !formData.value.contenido) {
    errorMessage.value = 'Por favor complete todos los campos obligatorios'
    return
  }

  isSubmitting.value = true

  try {
    const data = {
      titulo: formData.value.titulo,
      contenido: formData.value.contenido,
      test: formData.value.test || null,
    }

    if (formData.value.tipo === 'evaluacion') {
      await updateEvaluacion(activityId.value, data)
      successMessage.value = 'Evaluación actualizada exitosamente'
    } else {
      await updateTarea(activityId.value, data)
      successMessage.value = 'Tarea actualizada exitosamente'
    }
    
    setTimeout(() => {
      handleCancel()
    }, 2000)

  } catch (error) {
    console.error('Error al actualizar:', error)
    errorMessage.value = error instanceof Error ? error.message : `Error al actualizar la ${formData.value.tipo}`
  } finally {
    isSubmitting.value = false
  }
}

const handleCancel = () => {
  if (editorView) {
    editorView.destroy()
  }
  
  router.push({ name: 'actividad-detalles', params: { id: activityId.value, tipo: formData.value.tipo } })
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
              <div 
                class="p-2 rounded-xl shadow-lg"
                :class="formData.tipo === 'evaluacion' 
                  ? 'bg-gradient-to-br from-purple-400 to-blue-600' 
                  : 'bg-gradient-to-br from-emerald-400 to-teal-600'"
              >
                <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                </svg>
              </div>
              <div>
                <h1 class="text-2xl font-bold bg-gradient-to-r from-sky-400 to-blue-500 bg-clip-text text-transparent">
                  Editar {{ formData.tipo === 'evaluacion' ? 'Evaluación' : 'Tarea' }}
                </h1>
                <p class="text-sm text-slate-400">Modifica los datos de la actividad</p>
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
                Cancelar
              </button>
            </div>
          </div>
        </div>
      </header>

      <!-- Main Content -->
      <main class="flex flex-grow items-start justify-center px-4 py-8">
        <div class="mx-auto max-w-7xl w-full">
          
          <!-- Loading State -->
          <div v-if="isLoading" class="rounded-2xl border border-white/10 bg-slate-950/40 backdrop-blur-md shadow-2xl overflow-hidden">
            <div class="p-8">
              <div class="animate-pulse space-y-6">
                <div class="h-8 w-2/3 rounded bg-slate-700/50"></div>
                <div class="h-4 w-40 rounded bg-slate-800/50"></div>
                <div class="space-y-3">
                  <div class="h-10 w-full rounded bg-slate-800/50"></div>
                  <div class="h-32 w-full rounded bg-slate-800/50"></div>
                  <div class="h-64 w-full rounded bg-slate-800/50"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- Form Content -->
          <div v-else>
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
              <form @submit.prevent="handleSubmit" class="p-8">
                <!-- Layout de dos columnas -->
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                  
                  <!-- Columna Izquierda: Opciones del formulario -->
                  <div class="space-y-6">
                    <h2 class="text-xl font-semibold text-slate-100 border-b border-white/10 pb-3">
                      Información General
                    </h2>

                    <!-- Tipo de actividad (solo lectura) -->
                    <div class="space-y-2">
                      <label class="block text-sm font-medium text-slate-200">
                        Tipo de Actividad
                      </label>
                      <div class="flex items-center gap-4 p-4 rounded-lg bg-slate-900/50 border border-white/10">
                        <div 
                          class="flex-1 px-4 py-3 rounded-lg font-medium text-center"
                          :class="formData.tipo === 'tarea'
                            ? 'bg-gradient-to-r from-emerald-500 to-teal-600 text-white shadow-lg'
                            : formData.tipo === 'evaluacion'
                            ? 'bg-gradient-to-r from-purple-500 to-blue-600 text-white shadow-lg'
                            : 'bg-slate-800/50 text-slate-400'"
                        >
                          {{ formData.tipo === 'tarea' ? '📝 Tarea' : '📊 Evaluación' }}
                        </div>
                      </div>
                      <p class="text-xs text-slate-500">El tipo de actividad no puede ser modificado</p>
                    </div>

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
                        placeholder="Ingrese el título"
                        class="w-full rounded-lg border border-white/10 bg-slate-900/50 px-4 py-3 text-slate-100 placeholder:text-slate-500 focus:border-sky-500/50 focus:outline-none focus:ring-2 focus:ring-sky-500/20 transition-all"
                      />
                    </div>

                    <!-- Contenido -->
                    <div class="space-y-2">
                      <label for="contenido" class="block text-sm font-medium text-slate-200">
                        Descripción <span class="text-red-400">*</span>
                      </label>
                      <textarea
                        id="contenido"
                        v-model="formData.contenido"
                        rows="8"
                        required
                        placeholder="Ingrese la descripción y detalles de la actividad"
                        class="w-full rounded-lg border border-white/10 bg-slate-900/50 px-4 py-3 text-slate-100 placeholder:text-slate-500 focus:border-sky-500/50 focus:outline-none focus:ring-2 focus:ring-sky-500/20 transition-all resize-vertical"
                      ></textarea>
                    </div>
                  </div>

                  <!-- Columna Derecha: Editor de código Pytest -->
                  <div class="space-y-4">
                    <div class="flex items-center justify-between border-b border-white/10 pb-3">
                      <h2 class="text-xl font-semibold text-slate-100">
                        Código de Prueba (Pytest)
                      </h2>
                      <span class="text-slate-500 text-xs">(opcional)</span>
                    </div>
                    
                    <div class="space-y-3">
                    <p class="text-slate-400 text-sm flex items-start gap-2">
                      <svg class="w-4 h-4 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                      </svg>
                      <span>
                        Escriba el código de prueba Pytest que se ejecutará para evaluar las entregas de los estudiantes.
                        Deje vacío si no requiere pruebas automatizadas.
                      </span>
                    </p>                      <!-- CodeMirror Container -->
                      <div 
                        ref="editorContainer" 
                        class="rounded-lg border border-white/10 overflow-hidden shadow-lg"
                        style="height: 500px;"
                      ></div>
                    </div>
                  </div>
                </div>

                <!-- Form Actions -->
                <div class="flex items-center justify-end gap-4 pt-8 mt-8 border-t border-white/10">
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
                    class="inline-flex items-center gap-2 rounded-lg px-6 py-3 text-sm font-medium text-white shadow-lg transition-all duration-200 hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
                    :class="formData.tipo === 'evaluacion' 
                      ? 'bg-gradient-to-r from-purple-500 to-blue-600 hover:shadow-purple-500/50 shadow-purple-500/30' 
                      : 'bg-gradient-to-r from-emerald-500 to-teal-600 hover:shadow-emerald-500/50 shadow-emerald-500/30'"
                  >
                    <svg v-if="isSubmitting" class="w-5 h-5 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                    </svg>
                    <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                    {{ isSubmitting ? 'Guardando...' : 'Guardar Cambios' }}
                  </button>
                </div>
              </form>
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
/* Estilos para CodeMirror */
:deep(.cm-editor) {
  height: 100%;
  font-size: 14px;
}

:deep(.cm-scroller) {
  font-family: 'Fira Code', 'Consolas', 'Monaco', 'Courier New', monospace;
}

:deep(.cm-gutters) {
  border-right: 1px solid rgba(255, 255, 255, 0.1);
}

/* Smooth transitions */
* {
  transition-property: color, background-color, border-color, text-decoration-color, fill, stroke, opacity, box-shadow, transform;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}
</style>
