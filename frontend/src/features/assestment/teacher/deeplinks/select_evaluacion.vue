<script setup lang="ts">
import { ref, onMounted } from 'vue'

import { getCourseInfo } from '@/features/lti_protocol/info/info.service'

import { getEvaluacionesByCourseLmsId } from '../../shared'
import type { Actividad } from '../../shared/activity.types'
import configs from '@/core/configs'

const loading = ref(true)
const evaluaciones = ref<Actividad[]>([])
const formHtml = ref<string>('')
const isSubmitting = ref(false)

onMounted(async () => {
  try {
    // Obtener el ltik de la URL y guardarlo en sessionStorage si existe
    const urlParams = new URLSearchParams(window.location.search)
    const ltik = urlParams.get('ltik')
    if (ltik) {
      sessionStorage.setItem('ltik', ltik)
    }
    
    const courseInfo = await getCourseInfo()
    
    const courseId = courseInfo.id
    evaluaciones.value = await getEvaluacionesByCourseLmsId(courseId) as Actividad[]
  } catch (error) {
    console.error('Error al cargar las evaluaciones:', error)
  } finally {
    loading.value = false
  }
})


async function seleccionarEvaluacion(evaluacion: Actividad) {

    const ltik = sessionStorage.getItem('ltik')
    isSubmitting.value = true
    
    try {
        const res = await fetch(`${configs.ltiBaseUrl}/deeplink`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${ltik}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: evaluacion.titulo, 
                value: evaluacion.id 
            }),
        })

        const data = await res.text()
        formHtml.value = data
        
        // Esperar a que Vue renderice el HTML
        await new Promise(resolve => setTimeout(resolve, 100))
        
        // Buscar y enviar el formulario manualmente
        const form = document.querySelector('form[id^="ltijs_submit"]') as HTMLFormElement
        if (form) {
            form.submit()
        } else {
            console.error('No se encontró el formulario de DeepLink')
        }
    } catch (error) {
        console.error('Error al seleccionar evaluación:', error)
        isSubmitting.value = false
    }
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 p-8">
    <div v-if="isSubmitting" class="flex flex-col items-center justify-center min-h-screen">
      <div class="relative">
        <div class="w-20 h-20 border-4 border-purple-200 border-t-purple-600 rounded-full animate-spin"></div>
        <div class="absolute inset-0 flex items-center justify-center">
          <svg class="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
        </div>
      </div>
      <p class="mt-6 text-lg text-white font-semibold">Finalizando...</p>
      <p class="mt-2 text-slate-400">Redirigiendo a Canvas. Por favor, espera un momento.</p>
      <div v-if="formHtml" v-html="formHtml" class="hidden"></div>
    </div>
    <!-- Loading State -->
    <div v-if="loading" class="max-w-4xl mx-auto space-y-4">
      <div v-for="i in 3" :key="i" class="rounded-xl border border-white/10 bg-slate-950/40 backdrop-blur-md shadow-xl overflow-hidden">
        <div class="p-6">
          <div class="animate-pulse flex items-center justify-between">
            <div class="flex-grow space-y-3">
              <div class="h-6 w-2/3 rounded bg-slate-700/50"></div>
              <div class="h-4 w-40 rounded bg-slate-800/50"></div>
            </div>
            <div class="h-10 w-32 rounded bg-slate-700/50"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else-if="evaluaciones.length === 0" class="max-w-4xl mx-auto">
      <div class="rounded-xl border border-white/10 bg-slate-950/40 backdrop-blur-md shadow-xl overflow-hidden">
        <div class="p-12 text-center">
          <div class="mx-auto w-20 h-20 rounded-full bg-gradient-to-br from-slate-700/50 to-slate-800/50 flex items-center justify-center mb-6">
            <svg class="w-10 h-10 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
          </div>
          <h3 class="text-2xl font-bold text-white mb-2">No hay evaluaciones disponibles</h3>
          <p class="text-slate-400">No se encontraron evaluaciones registradas en este curso.</p>
        </div>
      </div>
    </div>

    <!-- Evaluaciones List -->
    <div v-else class="max-w-4xl mx-auto space-y-4">
      <div
        v-for="evaluacion in evaluaciones"
        :key="evaluacion.id"
        class="group rounded-xl border border-white/10 bg-slate-950/40 backdrop-blur-md shadow-xl hover:border-purple-500/50 transition-all duration-300 overflow-hidden"
      >
        <div class="p-6 flex items-center justify-between gap-6">
          <!-- Evaluación Info -->
          <div class="flex-grow">
            <div class="flex items-start gap-3">
              <div class="flex-shrink-0 mt-1">
                <div class="bg-gradient-to-br from-purple-400 to-blue-600 p-2 rounded-lg shadow-lg">
                  <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                  </svg>
                </div>
              </div>
              <div class="flex-grow">
                <h3 class="text-xl font-bold text-white group-hover:text-purple-400 transition-colors mb-2">
                  {{ evaluacion.titulo }}
                </h3>
                <div class="flex flex-wrap items-center gap-4">
                </div>
              </div>
            </div>
          </div>
          
          <!-- Seleccionar Button -->
          <div class="flex-shrink-0">
            <button
              @click="seleccionarEvaluacion(evaluacion)"
              class="inline-flex items-center gap-2 rounded-lg bg-gradient-to-r from-emerald-600 to-teal-700 px-6 py-3 text-sm font-semibold text-white hover:from-emerald-500 hover:to-teal-600 transition-all duration-200 hover:scale-105 shadow-lg"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              Seleccionar
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Smooth transitions for all interactive elements */
* {
  transition-property: color, background-color, border-color, text-decoration-color, fill, stroke, opacity, box-shadow, transform;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}
</style>
