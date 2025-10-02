<script setup lang="ts">
// Vue
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
// Evaluación
import { getEvaluaciones } from '../services/evaluaciones'
import { formatDate } from '../helpers/format_date'
import type { Evaluacion } from '../interfaces/evaluacion'

const loading = ref(true)
const evaluaciones = ref<Evaluacion[]>([])
const router = useRouter()

onMounted(async () => {
  try {
    evaluaciones.value = await getEvaluaciones() as Evaluacion[]
  } finally {
    loading.value = false
  }
})

function comenzar(evaluacion: Evaluacion) {
  router.push({ name: 'entorno-evaluacion', params: { id: evaluacion.id } })
}
</script>

<template>
  <div class="min-h-dvh bg-slate-900 text-slate-100">
    <header class="border-b border-slate-800 bg-slate-950">
      <div class="mx-auto max-w-7xl px-4 py-4 flex items-center justify-between">
        <h1 class="text-xl font-semibold">Lista de Evaluaciones</h1>
        <RouterLink
          to="/"
          class="inline-flex items-center rounded-md border border-slate-700 bg-slate-900 px-3 py-2 text-sm font-medium text-slate-200 hover:bg-slate-800 hover:text-white"
        >
          Volver
        </RouterLink>
      </div>
    </header>

    <main class="mx-auto max-w-2xl px-4 py-8">
      <div v-if="loading">
        <ul class="space-y-4">
          <li class="rounded-lg border border-slate-800 bg-slate-950 p-4">
            <div class="animate-pulse space-y-3">
              <div class="h-5 w-2/3 rounded bg-slate-700"></div>
              <div class="h-3 w-40 rounded bg-slate-800"></div>
              <div class="h-9 w-28 rounded bg-slate-800"></div>
            </div>
          </li>
          <li class="rounded-lg border border-slate-800 bg-slate-950 p-4">
            <div class="animate-pulse space-y-3">
              <div class="h-5 w-1/2 rounded bg-slate-700"></div>
              <div class="h-3 w-32 rounded bg-slate-800"></div>
              <div class="h-9 w-28 rounded bg-slate-800"></div>
            </div>
          </li>
          <li class="rounded-lg border border-slate-800 bg-slate-950 p-4">
            <div class="animate-pulse space-y-3">
              <div class="h-5 w-3/4 rounded bg-slate-700"></div>
              <div class="h-3 w-44 rounded bg-slate-800"></div>
              <div class="h-9 w-28 rounded bg-slate-800"></div>
            </div>
          </li>
        </ul>
      </div>

      <ul v-else class="space-y-4">
        <li
          v-for="evaluacion in evaluaciones"
          :key="evaluacion.id"
          class="flex items-center justify-between rounded-lg border border-slate-800 bg-slate-950 p-4"
        >
          <div>
            <div class="text-lg font-medium text-sky-400">
              {{ evaluacion.titulo }}
            </div>
            <div class="mt-1 text-xs text-slate-400">
              Fecha límite: {{ formatDate(evaluacion.fecha_limite) }}
            </div>
          </div>
          <button
            class="rounded-md bg-emerald-600 px-4 py-2 text-white text-sm font-medium hover:bg-emerald-700"
            @click="comenzar(evaluacion)"
          >
            Comenzar
          </button>
        </li>
      </ul>
    </main>
  </div>
</template>

<style scoped></style>