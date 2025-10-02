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
            borderRadius: '0.5rem',
            border: '1px solid rgb(51 65 85)',
            backgroundColor: '#0b1220',
          },
          '.cm-scroller': {
            fontFamily:
              'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace',
            fontSize: '1rem',
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
  <div class="min-h-dvh bg-slate-900 text-slate-100">
    <header class="border-b border-slate-800 bg-slate-950">
      <div class="mx-auto max-w-7xl px-4 py-4 flex items-center justify-between">
        <h1 class="text-xl font-semibold">Intérprete de Python</h1>
        <RouterLink
          to="/evaluaciones"
          class="inline-flex items-center rounded-md border border-slate-700 bg-slate-900 px-3 py-2 text-sm font-medium text-slate-200 hover:bg-slate-800 hover:text-white"
          title="Salir del intérprete"
        >
          Volver
        </RouterLink>
      </div>
    </header>

    <main class="w-full px-3 sm:px-4 lg:px-6 py-6 grid gap-4 md:grid-cols-[22rem_minmax(0,1fr)] lg:grid-cols-[26rem_minmax(0,1fr)]">
      <aside class="hidden md:block">
        <div class="sticky top-4 rounded-lg border border-slate-800 bg-slate-950 p-4">
          <h2 class="mb-2 text-sm font-semibold text-slate-200">Enunciado</h2>

          <div v-if="loadingEvaluacion" class="animate-pulse space-y-2">
            <div class="h-4 w-5/6 rounded bg-slate-800"></div>
            <div class="h-4 w-4/6 rounded bg-slate-800"></div>
            <div class="h-4 w-3/6 rounded bg-slate-800"></div>
            <div class="h-4 w-2/6 rounded bg-slate-800"></div>
          </div>
          <p v-else class="text-sm text-slate-400 whitespace-pre-wrap">
            {{ evaluacion?.contenido }}
          </p>
        </div>
      </aside>

      <div class="flex flex-col gap-4">
        <section class="flex flex-col gap-3">
          <div class="mt-1 flex items-center justify-between">
            <div class="flex items-center gap-2 text-sm text-slate-400">
              <span>Editor</span>
            </div>
            <div class="flex items-center gap-2">
              <button
                class="inline-flex items-center rounded-md bg-sky-600 px-3 py-2 text-white text-sm font-medium hover:bg-sky-700 disabled:opacity-50"
                :disabled="isCodeRunning"
                @click="run"
              >
                <svg class="mr-2 h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                  <polygon points="8,5 19,12 8,19"></polygon>
                </svg>
                {{ isCodeRunning ? 'Ejecutando…' : 'Ejecutar' }}
              </button>

              <button
                class="inline-flex items-center rounded-md bg-emerald-600 px-3 py-2 text-white text-sm font-medium hover:bg-emerald-700"
                @click="onEnviarClick"
              >
                <svg class="mr-2 h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                  <path d="M22 3L9 14"/>
                  <path d="M22 3l-7 18-3-7-7-3 17-8Z"/>
                </svg>
                Enviar
              </button>
            </div>
          </div>
          <div ref="codeMirrorContainer" class="w-full"></div>
        </section>

        <!-- Terminal -->
        <section class="flex flex-col gap-3">
          <label class="text-sm font-medium text-slate-300">Terminal</label>
          <pre :class="[
            'h-[220px] w-full overflow-auto rounded-lg border p-3 text-sm',
            isErrorInTerminal
              ? 'border-rose-700 bg-rose-950 text-rose-200'
              : 'border-slate-700 bg-slate-900 text-slate-100'
          ]">{{ consoleText || '—' }}</pre>
        </section>
      </div>
    </main>

    <!-- Modal de confirmación -->
    <div v-if="showConfirm" class="fixed inset-0 z-50 flex items-center justify-center">
      <div class="absolute inset-0 bg-slate-950/60" @click="cancelEnviar"></div>
      <div class="relative mx-4 w-full max-w-sm rounded-lg border border-slate-700 bg-slate-900 p-5 shadow-lg">
        <h3 class="text-base font-semibold text-slate-100">Enviar evaluación</h3>
        <p class="mt-2 text-sm text-slate-400">
          ¿Confirmas que deseas enviar tu solución para esta evaluación?
        </p>
        <div class="mt-4 flex justify-end gap-2">
          <button class="inline-flex items-center rounded-md bg-slate-700 px-3 py-2 text-slate-100 text-sm hover:bg-slate-600" @click="cancelEnviar">
            Cancelar
          </button>
          <button class="inline-flex items-center rounded-md bg-emerald-600 px-3 py-2 text-white text-sm font-medium hover:bg-emerald-700" @click="confirmEnviar">
            Confirmar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>



