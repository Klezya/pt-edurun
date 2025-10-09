<script setup lang="ts">
// Core Vue imports
import { onMounted, onBeforeUnmount, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

// Servicios y tipos
import { getEvaluacion } from '../services/evaluaciones'
import type { Evaluacion } from '../interfaces/evaluacion'
import { runCode, sendCode } from '../services/codigo'

// CodeMirror imports
import { EditorState } from '@codemirror/state'
import { EditorView, keymap, lineNumbers, highlightActiveLineGutter, ViewUpdate } from '@codemirror/view'
import { defaultKeymap, history, historyKeymap, indentMore } from '@codemirror/commands'
import { indentOnInput, bracketMatching } from '@codemirror/language'
import { python } from '@codemirror/lang-python'
import { oneDark } from '@codemirror/theme-one-dark'


const route = useRoute()

const evaluacion = ref<Evaluacion | null>(null)
const loadingEvaluacion = ref(true)

const isCodeRunning = ref(false)
const textCode = ref(`
print("Hola mundo")\n
`)

const consoleText = ref('')
const isErrorInTerminal = ref(false)

const codeMirrorContainer = ref<HTMLDivElement | null>(null)
let view: EditorView | null = null

// Estado del modal de confirmación
const showConfirm = ref(false)
function onEnviarClick() {
  showConfirm.value = true
}
function cancelEnviar() {
  showConfirm.value = false
}
async function confirmEnviar() {
  showConfirm.value = false
  await enviar()
}

async function cargarEvaluacion() {
  loadingEvaluacion.value = true
  evaluacion.value = null

  const id = Number(route.params.id)

  try {
    evaluacion.value = await getEvaluacion(id) as Evaluacion
  } catch (e: any) {
    console.log('Error al cargar la evaluación:', e)
  } finally {
    loadingEvaluacion.value = false
  }
}

async function run() {
  if (isCodeRunning.value) return
  isCodeRunning.value = true
  try {
    const res = await runCode(textCode.value)

    if (!res.ok) {
      console.log('Error en la respuesta de /code-run/:', res.statusText)
      return
    }
    const data = await res.json()
    console.log('Respuesta de /run-code/:', data)
    if (data.stderr) {
      consoleText.value = data.stderr
      isErrorInTerminal.value = true
    } else {
      consoleText.value = data.stdout
      isErrorInTerminal.value = false
    }
  } catch (e) {
    console.log('Error al llamar /run-code/:', e)
  } finally {
    isCodeRunning.value = false
  }
}


async function enviar() {
  if (isCodeRunning.value) return
  try {
    const res = await sendCode(textCode.value, evaluacion.value?.id as number)

    const data = await res.json()
    console.log('Respuesta de /send-code/:', data)
    if (data.stderr) {
      consoleText.value = data.stderr
      isErrorInTerminal.value = true
    } else {
      consoleText.value = data.stdout
      isErrorInTerminal.value = false
    }
  } catch (e) {
    console.log('Error al enviar el código:', e)
  } finally {
    // noop
  }
}

onMounted(() => {
  cargarEvaluacion()

  if (codeMirrorContainer.value && !view) {
    const startState = EditorState.create({
      doc: textCode.value,
      extensions: [
        lineNumbers(),
        highlightActiveLineGutter(),
        keymap.of([
          ...defaultKeymap,
          ...historyKeymap,
          { key: 'Tab', preventDefault: true, run: indentMore },
        ]),
        history(),
        indentOnInput(),
        bracketMatching(),
        python(),
        oneDark,
        EditorView.lineWrapping,
        EditorView.updateListener.of((vu: ViewUpdate) => {
          if (vu.docChanged) {
            textCode.value = vu.state.doc.toString()
          }
        }),
        EditorView.theme({
          '&': {
            height: '65vh',
            borderRadius: '0.75rem',
            border: '1px solid rgba(148, 163, 184, 0.1)',
            backgroundColor: 'rgba(15, 23, 42, 0.6)',
          },
          '.cm-scroller': {
            fontFamily:
              'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace',
            fontSize: '1rem',
          },
          '.cm-gutters': {
            backgroundColor: 'rgba(15, 23, 42, 0.4)',
            borderRight: '1px solid rgba(148, 163, 184, 0.1)',
          },
        }),
      ],
    })
    view = new EditorView({ state: startState, parent: codeMirrorContainer.value })
  }
})


onBeforeUnmount(() => {
  if (view) {
    view.destroy()
    view = null
  }
})
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
    <!-- Decorative background elements -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-20 left-10 w-72 h-72 bg-emerald-500/10 rounded-full blur-3xl"></div>
      <div class="absolute bottom-20 right-10 w-96 h-96 bg-sky-500/10 rounded-full blur-3xl"></div>
      <div class="absolute top-1/2 left-1/2 w-80 h-80 bg-purple-500/5 rounded-full blur-3xl"></div>
    </div>

    <div class="relative flex min-h-screen flex-col">
      <!-- Header -->
      <header class="border-b border-white/10 bg-slate-950/30 backdrop-blur-sm shadow-lg">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div class="flex h-20 items-center justify-between">
            <div class="flex items-center gap-3">
              <div class="bg-gradient-to-br from-emerald-400 to-teal-600 p-2 rounded-xl shadow-lg">
                <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path>
                </svg>
              </div>
              <div>
                <h1 class="text-2xl font-bold bg-gradient-to-r from-emerald-400 to-teal-500 bg-clip-text text-transparent">
                  Intérprete de Python
                </h1>
                <p v-if="evaluacion" class="text-sm text-slate-400">{{ evaluacion.titulo }}</p>
              </div>
            </div>
            <RouterLink
              to="/evaluaciones"
              class="inline-flex items-center gap-2 rounded-lg px-4 py-2.5 text-sm font-medium text-slate-200 hover:bg-white/10 hover:text-white transition-all duration-200 hover:scale-105"
              title="Salir del intérprete"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
              </svg>
              Volver
            </RouterLink>
          </div>
        </div>
      </header>

      <!-- Main Content -->
      <main class="relative flex-grow w-full px-3 sm:px-4 lg:px-6 py-6 grid gap-4 md:grid-cols-[22rem_minmax(0,1fr)] lg:grid-cols-[26rem_minmax(0,1fr)]">
        <!-- Enunciado Sidebar -->
        <aside class="hidden md:block">
          <div class="sticky top-4 rounded-2xl border border-white/10 bg-slate-950/40 backdrop-blur-md shadow-2xl p-6">
            <div class="flex items-center gap-2 mb-4">
              <div class="bg-gradient-to-br from-amber-400 to-orange-600 p-2 rounded-lg shadow-lg">
                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
              </div>
              <h2 class="text-lg font-semibold text-white">Enunciado</h2>
            </div>

            <div v-if="loadingEvaluacion" class="animate-pulse space-y-3">
              <div class="h-4 w-5/6 rounded bg-slate-700/50"></div>
              <div class="h-4 w-4/6 rounded bg-slate-700/50"></div>
              <div class="h-4 w-3/6 rounded bg-slate-700/50"></div>
              <div class="h-4 w-2/6 rounded bg-slate-700/50"></div>
            </div>
            <p v-else class="text-sm text-slate-300 whitespace-pre-wrap leading-relaxed">
              {{ evaluacion?.contenido }}
            </p>
          </div>
        </aside>

        <!-- Editor and Terminal -->
        <div class="flex flex-col gap-4">
          <!-- Editor Section -->
          <section class="flex flex-col gap-3">
            <div class="rounded-2xl border border-white/10 bg-slate-950/40 backdrop-blur-md shadow-2xl p-6">
              <div class="flex items-center justify-between mb-4">
                <div class="flex items-center gap-2">
                  <div class="bg-gradient-to-br from-sky-400 to-blue-600 p-2 rounded-lg shadow-lg">
                    <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path>
                    </svg>
                  </div>
                  <span class="text-lg font-semibold text-white">Editor de Código</span>
                </div>
                <div class="flex items-center gap-2">
                  <button
                    class="inline-flex items-center gap-2 rounded-lg bg-gradient-to-r from-sky-600 to-blue-700 px-4 py-2.5 text-white text-sm font-medium hover:from-sky-500 hover:to-blue-600 transition-all duration-200 hover:scale-105 shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
                    :disabled="isCodeRunning"
                    @click="run"
                  >
                    <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <polygon points="8,5 19,12 8,19"></polygon>
                    </svg>
                    <span>{{ isCodeRunning ? 'Ejecutando…' : 'Ejecutar' }}</span>
                  </button>

                  <button
                    class="inline-flex items-center gap-2 rounded-lg bg-gradient-to-r from-emerald-600 to-teal-700 px-4 py-2.5 text-white text-sm font-medium hover:from-emerald-500 hover:to-teal-600 transition-all duration-200 hover:scale-105 shadow-lg"
                    @click="onEnviarClick"
                  >
                    <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M22 3L9 14"/>
                      <path d="M22 3l-7 18-3-7-7-3 17-8Z"/>
                    </svg>
                    <span>Enviar</span>
                  </button>
                </div>
              </div>
              <div ref="codeMirrorContainer" class="w-full"></div>
            </div>
          </section>

          <!-- Terminal Section -->
          <section class="flex flex-col gap-3">
            <div class="rounded-2xl border border-white/10 bg-slate-950/40 backdrop-blur-md shadow-2xl p-6">
              <div class="flex items-center gap-2 mb-4">
                <div :class="[
                  'p-2 rounded-lg shadow-lg',
                  isErrorInTerminal 
                    ? 'bg-gradient-to-br from-rose-400 to-red-600' 
                    : 'bg-gradient-to-br from-slate-400 to-slate-600'
                ]">
                  <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                  </svg>
                </div>
                <span class="text-lg font-semibold text-white">Terminal</span>
              </div>
              <pre :class="[
                'h-[220px] w-full overflow-auto rounded-lg border p-4 text-sm font-mono',
                isErrorInTerminal
                  ? 'border-rose-500/50 bg-rose-950/50 text-rose-200'
                  : 'border-slate-700/50 bg-slate-900/50 text-slate-100'
              ]">{{ consoleText || '—' }}</pre>
            </div>
          </section>
        </div>
      </main>
    </div>

    <!-- Modal de confirmación -->
    <div v-if="showConfirm" class="fixed inset-0 z-50 flex items-center justify-center">
      <div class="absolute inset-0 bg-slate-950/80 backdrop-blur-sm" @click="cancelEnviar"></div>
      <div class="relative mx-4 w-full max-w-md rounded-2xl border border-white/10 bg-slate-950/90 backdrop-blur-md shadow-2xl p-6">
        <div class="flex items-center gap-3 mb-4">
          <div class="bg-gradient-to-br from-emerald-400 to-teal-600 p-2 rounded-lg shadow-lg">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          <h3 class="text-xl font-bold text-white">Enviar evaluación</h3>
        </div>
        <p class="text-sm text-slate-300 mb-6">
          ¿Confirmas que deseas enviar tu solución para esta evaluación? Esta acción será registrada.
        </p>
        <div class="flex justify-end gap-3">
          <button 
            class="inline-flex items-center gap-2 rounded-lg px-4 py-2.5 text-sm font-medium text-slate-200 hover:bg-white/10 hover:text-white transition-all duration-200" 
            @click="cancelEnviar"
          >
            Cancelar
          </button>
          <button 
            class="inline-flex items-center gap-2 rounded-lg bg-gradient-to-r from-emerald-600 to-teal-700 px-4 py-2.5 text-white text-sm font-medium hover:from-emerald-500 hover:to-teal-600 transition-all duration-200 hover:scale-105 shadow-lg" 
            @click="confirmEnviar"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
            </svg>
            <span>Confirmar</span>
          </button>
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

/* Smooth transitions for all interactive elements */
* {
  transition-property: color, background-color, border-color, text-decoration-color, fill, stroke, opacity, box-shadow, transform;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}
</style>


