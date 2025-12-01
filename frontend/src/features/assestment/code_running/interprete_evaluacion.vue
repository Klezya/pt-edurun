<script setup lang="ts">
// Core Vue imports
import { onMounted, onBeforeUnmount, ref} from 'vue'
import { useRoute } from 'vue-router'

// Servicios y tipos
import { getEvaluacion } from '../shared'
import type { Actividad } from '../shared/activity.types'
import { runCode, sendCode, sendGrade, runEvaluacionTests, submitEvaluacion } from './code.service'
import { getUserInfo } from '@/features/lti_protocol'

// CodeMirror imports
import { EditorState } from '@codemirror/state'
import { EditorView, keymap, lineNumbers, highlightActiveLineGutter, ViewUpdate } from '@codemirror/view'
import { defaultKeymap, history, historyKeymap, indentMore } from '@codemirror/commands'
import { indentOnInput, bracketMatching } from '@codemirror/language'
import { python } from '@codemirror/lang-python'
import { oneDark } from '@codemirror/theme-one-dark'


const route = useRoute()

const evaluacion = ref<Actividad | null>(null)
const loadingEvaluacion = ref(true)

const isCodeRunning = ref(false)
const textCode = ref(`
print("Hola mundo")\n
`)

const consoleText = ref('')
const isErrorInTerminal = ref(false)

const codeMirrorContainer = ref<HTMLDivElement | null>(null)
let view: EditorView | null = null

const copyAttempts = ref(0)
const pasteAttempts = ref(0)
const cutAttempts = ref(0)

// Métricas de ejecución
const codeExecutionCount = ref(0)
const testExecutionCount = ref(0)

// Tiempo total de desarrollo
const startTime = ref<number | null>(null)

// Rastreo de pantalla completa
const exitedFullscreen = ref(false)

// Contador de cambios de ventana/pestaña
const windowSwitchCount = ref(0)
const lastBlurTime = ref<number | null>(null)
const totalInactivityTime = ref(0) // en segundos

// Estado del modal de inicio de evaluación
const showStartModal = ref(false)
const evaluacionIniciada = ref(false)

// Estado del modal de confirmación de envío
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

// Funciones para manejar pantalla completa
async function requestFullscreen() {
  const elem = document.documentElement
  elem.requestFullscreen()
}

async function exitFullscreen() {
  try {
    if (document.fullscreenElement) {
      await document.exitFullscreen()
    }
  } catch (err) {
    console.error('Error al salir de pantalla completa:', err)
  }
}

function handleFullscreenChange() {
  if (!document.fullscreenElement && evaluacionIniciada.value) {
    exitedFullscreen.value = true
    console.warn('Usuario salió de pantalla completa')
  }
}

// Funciones del modal de inicio
async function iniciarEvaluacion() {
  showStartModal.value = false
  evaluacionIniciada.value = true
  startTime.value = Date.now()
  console.log('Evaluación iniciada')
  // Activar pantalla completa
  await requestFullscreen()
}

function cancelarInicio() {
  // Opcional: redirigir a otra página o cerrar la vista
  console.log('Inicio de evaluación cancelado')
  window.history.back()
}

// Manejador de cambio de ventana/pestaña
function handleWindowBlur() {
  windowSwitchCount.value++
  lastBlurTime.value = Date.now()
  console.log(`Cambio de ventana detectado. Total: ${windowSwitchCount.value}`)
}

function handleWindowFocus() {
  if (lastBlurTime.value) {
    const timeAway = Math.round((Date.now() - lastBlurTime.value) / 1000)
    totalInactivityTime.value += timeAway
    console.log(`Usuario regresó después de ${timeAway} segundos. Tiempo total de inactividad: ${totalInactivityTime.value}s`)
    lastBlurTime.value = null
  }
}

async function cargarEvaluacion() {
  loadingEvaluacion.value = true
  evaluacion.value = null

  const id = Number(route.params.id)

  try {
    evaluacion.value = await getEvaluacion(id) as Actividad
    // Mostrar modal de inicio después de cargar la evaluación
    showStartModal.value = true
  } catch (e: any) {
    console.log('Error al cargar la evaluación:', e)
  } finally {
    loadingEvaluacion.value = false
  }
}

async function run() {
  if (isCodeRunning.value || !evaluacionIniciada.value) return
  isCodeRunning.value = true
  try {
    codeExecutionCount.value++
    
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


async function correrTests() {
  if (isCodeRunning.value || !evaluacionIniciada.value) return
  isCodeRunning.value = true
  try {
    testExecutionCount.value++
    
    const res = await runEvaluacionTests(textCode.value, evaluacion.value?.id as number)

    if (!res.ok) {
      console.log('Error en la respuesta de /run-evaluacion-test/:', res.statusText)
      return
    }

    const data = await res.json()
    console.log('Respuesta de /run-evaluacion-test/:', data)
    if (data.stderr) {
      consoleText.value = data.stderr
      isErrorInTerminal.value = true
    } else {
      consoleText.value = data.stdout
      isErrorInTerminal.value = false
    }
  } catch (e) {
    console.log('Error al correr los tests:', e)
  } finally {
    isCodeRunning.value = false
  }
}


async function enviar() {
  const assessment_id = Number(route.params.id)

  if (isCodeRunning.value || !evaluacionIniciada.value) return
  isCodeRunning.value = true
  
  try {
    const res = await sendCode(textCode.value, evaluacion.value?.id as number)

    if (!res.ok) {
      console.log('Error en la respuesta de /send-code/:', res.statusText)
      consoleText.value = 'Error al enviar el código'
      isErrorInTerminal.value = true
      return
    }

    const data = await res.json()
    console.log('Respuesta de /send-code/:', data)

    if (data.return_code === 0 && data.score !== undefined) {
      
      try {
        const userInfo = await getUserInfo()
        const tiempoTotalSegundos = startTime.value 
          ? Math.round((Date.now() - startTime.value) / 1000)
          : 0
        
        const entregaData = {
          id_evaluacion: evaluacion.value?.id as number,
          id_alumno: userInfo.userId,
          nota: data.score,
          codigo: textCode.value,
          detalles: {
            intentos_copiar: copyAttempts.value,
            intentos_pegar: pasteAttempts.value,
            intentos_cortar: cutAttempts.value,
            salio_pantalla_completa: exitedFullscreen.value,
            cambios_ventana: windowSwitchCount.value,
            tiempo_inactividad_segundos: totalInactivityTime.value,
            ejecuciones_codigo: codeExecutionCount.value,
            ejecuciones_tests: testExecutionCount.value,
            tiempo_total_segundos: tiempoTotalSegundos,
            timestamp: new Date().toISOString(),
          }
        }
        
        await submitEvaluacion(entregaData)
        console.log('Entrega registrada en la base de datos')
        
      } catch (e) {
        console.error('Error al registrar la entrega:', e)
      }

      if (exitedFullscreen.value) {
        data.score = 0
      }
      const gradeRes = await sendGrade(data.score, assessment_id)
      if (gradeRes.ok) {
        console.log('Nota enviada al LMS:', data.score)
      } else {
        console.error('Error al enviar la nota al LMS:', gradeRes.statusText)
      }
    }
    
    if (data.stderr) {
      consoleText.value = data.stderr
      isErrorInTerminal.value = true
    } else {
      consoleText.value = data.stdout
      isErrorInTerminal.value = false
    }

    // Salir de pantalla completa y cerrar la ventana después de enviar
    await exitFullscreen()
    
    // Pequeño delay para asegurar que se procesó todo antes de cerrar
    setTimeout(() => {
      window.close()
    }, 1000)

  } catch (e) {
    console.log('Error al enviar el código:', e)
    consoleText.value = 'Error al conectar con el servidor'
    isErrorInTerminal.value = true
  } finally {
    isCodeRunning.value = false
  }
}

onMounted(() => {
  const urlParams = new URLSearchParams(window.location.search)
  const ltik = urlParams.get('ltik')
  if (ltik) {
    sessionStorage.setItem('ltik', ltik)
  }
  
  cargarEvaluacion()

  // Agregar listeners para detectar cambios de ventana
  window.addEventListener('blur', handleWindowBlur)
  window.addEventListener('focus', handleWindowFocus)

  // Agregar listener para detectar cambios en pantalla completa
  document.addEventListener('fullscreenchange', handleFullscreenChange)

  if (codeMirrorContainer.value && !view) {
    const blockCopyPaste = EditorView.domEventHandlers({
      paste: (event) => {
        event.preventDefault()
        pasteAttempts.value++
        return true
      },
      copy: (event) => {
        event.preventDefault()
        copyAttempts.value++
        return true
      },
      cut: (event) => {
        event.preventDefault()
        cutAttempts.value++
        return true
      },
    })

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
        blockCopyPaste,
        EditorView.updateListener.of((vu: ViewUpdate) => {
          if (vu.docChanged) {
            textCode.value = vu.state.doc.toString()
          }
        }),
        EditorView.theme({
          '&': {
            height: '35vh',
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
  
  // Limpiar listeners de ventana
  window.removeEventListener('blur', handleWindowBlur)
  window.removeEventListener('focus', handleWindowFocus)
  
  // Limpiar listener de pantalla completa
  document.removeEventListener('fullscreenchange', handleFullscreenChange)
  
  // Asegurarse de salir de pantalla completa al desmontar
  if (document.fullscreenElement) {
    exitFullscreen()
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
            <div class="rounded-2xl border border-white/10 bg-slate-950/40 backdrop-blur-md shadow-2xl p-6 relative">
              <!-- Overlay cuando no se ha iniciado -->
              <div v-if="!evaluacionIniciada" class="absolute inset-0 bg-slate-950/70 backdrop-blur-sm rounded-2xl z-10 flex items-center justify-center">
                <div class="text-center">
                  <svg class="w-16 h-16 text-slate-400 mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
                  </svg>
                  <p class="text-slate-300 font-medium">Debes iniciar la evaluación para comenzar</p>
                </div>
              </div>
              
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
                    :disabled="isCodeRunning || !evaluacionIniciada"
                    @click="run"
                  >
                    <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <polygon points="8,5 19,12 8,19"></polygon>
                    </svg>
                    <span>{{ isCodeRunning ? 'Ejecutando…' : 'Ejecutar' }}</span>
                  </button>

                  <button
                    class="inline-flex items-center gap-2 rounded-lg bg-gradient-to-r from-purple-600 to-indigo-700 px-4 py-2.5 text-white text-sm font-medium hover:from-purple-500 hover:to-indigo-600 transition-all duration-200 hover:scale-105 shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
                    :disabled="isCodeRunning || !evaluacionIniciada"
                    @click="correrTests"
                  >
                    <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M9 11l3 3L22 4"/>
                      <path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11"/>
                    </svg>
                    <span>Correr Tests</span>
                  </button>

                  <button
                    class="inline-flex items-center gap-2 rounded-lg bg-gradient-to-r from-emerald-600 to-teal-700 px-4 py-2.5 text-white text-sm font-medium hover:from-emerald-500 hover:to-teal-600 transition-all duration-200 hover:scale-105 shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
                    :disabled="isCodeRunning || !evaluacionIniciada"
                    @click="onEnviarClick"
                  >
                    <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M22 3L9 14"/>
                      <path d="M22 3l-7 18-3-7-7-3 17-8Z"/>
                    </svg>
                    <span>{{ isCodeRunning ? 'Enviando...' : 'Enviar' }}</span>
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

    <!-- Modal de inicio de evaluación -->
    <div v-if="showStartModal && !loadingEvaluacion" class="fixed inset-0 z-50 flex items-center justify-center">
      <div class="absolute inset-0 bg-slate-950/90 backdrop-blur-md"></div>
      <div class="relative mx-4 w-full max-w-2xl rounded-2xl border border-white/10 bg-slate-950/95 backdrop-blur-md shadow-2xl p-8">
        <div class="flex items-center gap-3 mb-6">
          <div class="bg-gradient-to-br from-blue-400 to-indigo-600 p-3 rounded-xl shadow-lg">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          <h3 class="text-2xl font-bold text-white">Comenzar Evaluación</h3>
        </div>
        
        <div class="mb-6 space-y-4">
          
          <div class="p-5 rounded-xl bg-amber-500/10 border border-amber-500/30">
            <div class="flex items-start gap-3">
              <svg class="w-6 h-6 text-amber-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
              </svg>
              <div class="flex-1">
                <h5 class="text-base font-semibold text-amber-300 mb-2">Instrucciones importantes:</h5>
                <ul class="space-y-2 text-sm text-amber-200/90">
                  <li class="flex items-start gap-2">
                    <span class="text-amber-400 font-bold">•</span>
                    <span>La pantalla se pondrá en modo pantalla completa automáticamente</span>
                  </li>
                  <li class="flex items-start gap-2">
                    <span class="text-red-400 font-bold">⚠️</span>
                    <span class="font-semibold text-red-300">Si sales de pantalla completa, la prueba será INVALIDADA</span>
                  </li>
                  <li class="flex items-start gap-2">
                    <span class="text-amber-400 font-bold">•</span>
                    <span>No podrás copiar ni pegar código en el editor</span>
                  </li>
                  <li class="flex items-start gap-2">
                    <span class="text-amber-400 font-bold">•</span>
                    <span>Se registrarán los cambios de ventana o pestaña y el tiempo fuera de la ventana</span>
                  </li>
                  <li class="flex items-start gap-2">
                    <span class="text-amber-400 font-bold">•</span>
                    <span>Una vez iniciada, todas tus acciones serán monitoreadas</span>
                  </li>
                  <li class="flex items-start gap-2">
                    <span class="text-amber-400 font-bold">•</span>
                    <span>Asegúrate de estar listo antes de continuar</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
        
        <div class="flex justify-end gap-3">
          <button 
            class="inline-flex items-center gap-2 rounded-lg px-5 py-3 text-sm font-medium text-slate-200 hover:bg-white/10 hover:text-white transition-all duration-200 border border-slate-700 hover:border-slate-500" 
            @click="cancelarInicio"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
            <span>Cancelar</span>
          </button>
          <button 
            class="inline-flex items-center gap-2 rounded-lg bg-gradient-to-r from-blue-600 to-indigo-700 px-5 py-3 text-white text-sm font-medium hover:from-blue-500 hover:to-indigo-600 transition-all duration-200 hover:scale-105 shadow-lg" 
            @click="iniciarEvaluacion"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <span>Estoy listo, comenzar</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Modal de confirmación de envío -->
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


