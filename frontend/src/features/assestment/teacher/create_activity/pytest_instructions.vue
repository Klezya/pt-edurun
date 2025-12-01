<script setup lang="ts">
import { ref } from 'vue'

const isOpen = ref(false)

const open = () => {
  isOpen.value = true
}

const close = () => {
  isOpen.value = false
}

// Exponer el método open para que el componente padre pueda llamarlo
defineExpose({
  open
})
</script>

<template>
  <!-- Modal de instructivo -->
  <Teleport to="body">
    <Transition
      enter-active-class="transition-opacity duration-200"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition-opacity duration-200"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="isOpen"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4"
        @click.self="close"
      >
        <Transition
          enter-active-class="transition-all duration-300"
          enter-from-class="opacity-0 scale-95"
          enter-to-class="opacity-100 scale-100"
          leave-active-class="transition-all duration-200"
          leave-from-class="opacity-100 scale-100"
          leave-to-class="opacity-0 scale-95"
        >
          <div
            v-if="isOpen"
            class="relative w-full max-w-3xl max-h-[90vh] overflow-hidden rounded-2xl border border-white/10 bg-slate-950 shadow-2xl"
          >
            <!-- Header -->
            <div class="flex items-center justify-between border-b border-white/10 bg-gradient-to-r from-sky-900/30 to-blue-900/30 px-6 py-4">
              <div class="flex items-center gap-3">
                <div class="rounded-lg bg-sky-500/20 p-2">
                  <svg class="h-6 w-6 text-sky-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                </div>
                <h2 class="text-xl font-bold text-slate-100">
                  Instructivo de Uso - Pytest
                </h2>
              </div>
              <button
                @click="close"
                class="rounded-lg p-2 text-slate-400 transition-all hover:bg-white/10 hover:text-slate-100"
                aria-label="Cerrar"
              >
                <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
              </button>
            </div>

            <!-- Content -->
            <div class="overflow-y-auto px-6 py-6 max-h-[calc(90vh-140px)]">
              <div class="space-y-6 text-slate-300">
                <!-- Introducción -->
                <section>
                  <h3 class="mb-3 text-lg font-semibold text-sky-400">
                    ¿Qué es Pytest?
                  </h3>
                  <p class="leading-relaxed text-slate-300">
                    Pytest es un framework de pruebas para Python que permite escribir tests automatizados para validar el código de los estudiantes. 
                    El código que escribas aquí se ejecutará contra las entregas de los estudiantes para evaluar automáticamente si cumplen con los requisitos.
                  </p>
                </section>

                <!-- Conceptos básicos -->
                <section>
                  <h3 class="mb-3 text-lg font-semibold text-sky-400">
                    📚 Conceptos Básicos
                  </h3>
                  <div class="space-y-4">
                    <!-- Función de test -->
                    <div class="rounded-lg border border-cyan-500/30 bg-cyan-950/20 p-4">
                      <div class="flex items-start gap-3">
                        <div class="rounded bg-cyan-500/20 p-2">
                          <svg class="h-5 w-5 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path>
                          </svg>
                        </div>
                        <div class="flex-1">
                          <h4 class="mb-2 font-semibold text-cyan-300">¿Qué es una función test?</h4>
                          <p class="text-sm text-slate-300 mb-2">
                            Una <strong>función test</strong> es una función de Python que comienza con <code class="rounded bg-slate-800 px-2 py-0.5 text-sky-400">test_</code> 
                            y contiene uno o más asserts para verificar que el código del estudiante funcione correctamente.
                          </p>
                          <div class="rounded bg-slate-950 p-3">
                            <code class="text-xs"><span class="text-purple-400">def</span> <span class="text-blue-400">test_suma</span>():<br/>
                            &nbsp;&nbsp;&nbsp;&nbsp;<span class="text-gray-500"># Esta es una función test</span><br/>
                            &nbsp;&nbsp;&nbsp;&nbsp;resultado = <span class="text-yellow-400">suma</span>(<span class="text-orange-400">2</span>, <span class="text-orange-400">3</span>)<br/>
                            &nbsp;&nbsp;&nbsp;&nbsp;<span class="text-purple-400">assert</span> resultado == <span class="text-orange-400">5</span></code>
                          </div>
                          <p class="text-xs text-slate-400 mt-2">
                            Cada función test representa <strong>una prueba completa e independiente</strong>.
                          </p>
                        </div>
                      </div>
                    </div>

                    <!-- Assert -->
                    <div class="rounded-lg border border-teal-500/30 bg-teal-950/20 p-4">
                      <div class="flex items-start gap-3">
                        <div class="rounded bg-teal-500/20 p-2">
                          <svg class="h-5 w-5 text-teal-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                          </svg>
                        </div>
                        <div class="flex-1">
                          <h4 class="mb-2 font-semibold text-teal-300">¿Qué es un assert?</h4>
                          <p class="text-sm text-slate-300 mb-2">
                            Un <strong>assert</strong> es una verificación que comprueba si una condición es verdadera. 
                            Si la condición es <span class="text-green-400">verdadera</span>, el assert pasa. 
                            Si es <span class="text-red-400">falsa</span>, el assert falla y detiene la función test inmediatamente.
                          </p>
                          <div class="rounded bg-slate-950 p-3 space-y-2">
                            <div>
                              <code class="text-xs"><span class="text-purple-400">assert</span> <span class="text-yellow-400">suma</span>(<span class="text-orange-400">2</span>, <span class="text-orange-400">3</span>) == <span class="text-orange-400">5</span>  <span class="text-gray-500"># ✅ Pasa (2+3 es 5)</span></code>
                            </div>
                            <div>
                              <code class="text-xs"><span class="text-purple-400">assert</span> <span class="text-yellow-400">suma</span>(<span class="text-orange-400">2</span>, <span class="text-orange-400">3</span>) == <span class="text-orange-400">10</span> <span class="text-gray-500"># ❌ Falla (2+3 NO es 10)</span></code>
                            </div>
                          </div>
                          <p class="text-xs text-slate-400 mt-2">
                            Los asserts son las verificaciones individuales dentro de cada función test.
                          </p>
                        </div>
                      </div>
                    </div>

                    <!-- Cómo funciona -->
                    <div class="rounded-lg border border-violet-500/30 bg-violet-950/20 p-4">
                      <div class="flex items-start gap-3">
                        <div class="rounded bg-violet-500/20 p-2">
                          <svg class="h-5 w-5 text-violet-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                          </svg>
                        </div>
                        <div class="flex-1">
                          <h4 class="mb-2 font-semibold text-violet-300">¿Cómo funciona el proceso?</h4>
                          <ol class="text-sm text-slate-300 space-y-2 list-decimal ml-4">
                            <li>Pytest ejecuta cada <strong>función test_*</strong> una por una</li>
                            <li>Dentro de cada función, ejecuta los <strong>asserts</strong> en orden</li>
                            <li>Si <strong>todos los asserts</strong> de una función pasan → el test pasa ✅</li>
                            <li>Si <strong>cualquier assert</strong> falla → el test falla ❌ y se detiene</li>
                            <li>Al final, calcula el puntaje: <code class="rounded bg-slate-800 px-2 py-0.5 text-sky-400">(tests_pasados / tests_totales) × 100</code></li>
                          </ol>
                        </div>
                      </div>
                    </div>
                  </div>
                </section>

                <!-- Reglas importantes del sistema -->
                <section>
                  <h3 class="mb-3 text-lg font-semibold text-sky-400">
                    🎯 Reglas Importantes del Sistema
                  </h3>
                  <div class="space-y-3">
                    <div class="rounded-lg border border-amber-500/30 bg-amber-950/20 p-4">
                      <div class="flex items-start gap-3">
                        <svg class="mt-0.5 h-5 w-5 flex-shrink-0 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                        <div class="space-y-2 text-sm">
                          <p class="font-semibold text-amber-300">1. El código del estudiante siempre se llama "app"</p>
                          <p class="text-slate-300">Todas las importaciones deben ser desde <code class="rounded bg-slate-800 px-2 py-0.5 text-sky-400">app</code>, no uses otros nombres.</p>
                        </div>
                      </div>
                    </div>

                    <div class="rounded-lg border border-purple-500/30 bg-purple-950/20 p-4">
                      <div class="flex items-start gap-3">
                        <svg class="mt-0.5 h-5 w-5 flex-shrink-0 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
                        </svg>
                        <div class="space-y-2 text-sm">
                          <p class="font-semibold text-purple-300">2. Cada función "test_*" cuenta como 1 test completo</p>
                          <p class="text-slate-300">No importa cuántos <code class="rounded bg-slate-800 px-2 py-0.5 text-sky-400">assert</code> tenga dentro, cada función <code class="rounded bg-slate-800 px-2 py-0.5 text-sky-400">test_*()</code> es considerada como una unidad de test.</p>
                        </div>
                      </div>
                    </div>

                    <div class="rounded-lg border border-red-500/30 bg-red-950/20 p-4">
                      <div class="flex items-start gap-3">
                        <svg class="mt-0.5 h-5 w-5 flex-shrink-0 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
                        </svg>
                        <div class="space-y-2 text-sm">
                          <p class="font-semibold text-red-300">⚠️ IMPORTANTE: Si un assert falla, todo el test falla</p>
                          <p class="text-slate-300">Cuando un <code class="rounded bg-slate-800 px-2 py-0.5 text-sky-400">assert</code> falla dentro de una función, <strong>la función se detiene inmediatamente</strong> y el test completo se marca como fallido (0 puntos).</p>
                          <div class="mt-2 rounded bg-slate-950 p-2">
                            <code class="text-xs"><span class="text-purple-400">def</span> <span class="text-blue-400">test_ejemplo</span>():<br/>
                            &nbsp;&nbsp;<span class="text-purple-400">assert</span> <span class="text-yellow-400">suma</span>(<span class="text-orange-400">2</span>,<span class="text-orange-400">3</span>) == <span class="text-orange-400">5</span>  <span class="text-green-400"># ✅ Pasa</span><br/>
                            &nbsp;&nbsp;<span class="text-purple-400">assert</span> <span class="text-yellow-400">suma</span>(<span class="text-orange-400">2</span>,<span class="text-orange-400">2</span>) == <span class="text-orange-400">100</span> <span class="text-red-400"># ❌ Falla aquí</span><br/>
                            &nbsp;&nbsp;<span class="text-purple-400">assert</span> <span class="text-yellow-400">suma</span>(<span class="text-orange-400">1</span>,<span class="text-orange-400">1</span>) == <span class="text-orange-400">2</span>  <span class="text-gray-500"># ⏭️ Nunca se ejecuta</span><br/>
                            <span class="text-gray-500"># Resultado: Test FALLIDO = 0 puntos</span></code>
                          </div>
                          <p class="text-amber-300 font-medium mt-2">💡 Por eso es mejor crear múltiples funciones test_* independientes en lugar de una funcion con muchos asserts.</p>
                        </div>
                      </div>
                    </div>

                    <div class="rounded-lg border border-green-500/30 bg-green-950/20 p-4">
                      <div class="flex items-start gap-3">
                        <svg class="mt-0.5 h-5 w-5 flex-shrink-0 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
                        </svg>
                        <div class="space-y-2 text-sm">
                          <p class="font-semibold text-green-300">3. Cálculo automático del puntaje</p>
                          <p class="text-slate-300">El sistema calcula el porcentaje automáticamente basado en la cantidad de tests: <strong>Puntaje = (tests_pasados / tests_totales) × 100</strong></p>
                          <p class="text-slate-400 italic">Ejemplo: 5 tests = 20 puntos cada uno. No puedes cambiar el valor individual.</p>
                        </div>
                      </div>
                    </div>

                    <div class="rounded-lg border border-blue-500/30 bg-blue-950/20 p-4">
                      <div class="flex items-start gap-3">
                        <svg class="mt-0.5 h-5 w-5 flex-shrink-0 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                        </svg>
                        <div class="space-y-2 text-sm">
                          <p class="font-semibold text-blue-300">4. Visibilidad de los nombres de tests</p>
                          <p class="text-slate-300">Los estudiantes <strong>solo ven el nombre del test si NO lo pasan</strong>. Elige tu estrategia:</p>
                          <ul class="ml-4 mt-2 space-y-1 list-disc text-slate-400">
                            <li>Nombres genéricos (<code class="text-sky-400">test1, test2</code>) para no dar pistas</li>
                            <li>Nombres descriptivos (<code class="text-sky-400">test_suma_positivos</code>) para guiar al estudiante</li>
                          </ul>
                        </div>
                      </div>
                    </div>
                  </div>
                </section>

                <!-- Estructura básica -->
                <section>
                  <h3 class="mb-3 text-lg font-semibold text-sky-400">
                    Estructura Básica
                  </h3>
                  <div class="space-y-3">
                    <div class="rounded-lg border border-white/10 bg-slate-900/50 p-4">
                      <p class="mb-2 text-sm font-medium text-slate-400">Ejemplo básico:</p>
                      <pre class="overflow-x-auto rounded bg-slate-950 p-3 text-sm"><code><span class="text-gray-500"># Siempre importar desde 'app'</span>
<span class="text-purple-400">from</span> <span class="text-cyan-400">app</span> <span class="text-purple-400">import</span> <span class="text-yellow-400">suma</span>

<span class="text-purple-400">def</span> <span class="text-blue-400">test_suma_basica</span>():
    <span class="text-emerald-400">"""Descripción del test"""</span>
    <span class="text-purple-400">assert</span> <span class="text-yellow-400">suma</span>(<span class="text-orange-400">2</span>, <span class="text-orange-400">3</span>) == <span class="text-orange-400">5</span>
    <span class="text-purple-400">assert</span> <span class="text-yellow-400">suma</span>(<span class="text-orange-400">10</span>, <span class="text-orange-400">5</span>) == <span class="text-orange-400">15</span>
    <span class="text-gray-500"># Todos estos asserts cuentan como 1 solo test</span></code></pre>
                    </div>
                    <ul class="ml-6 space-y-2 list-disc text-slate-300">
                      <li>Las funciones de test <strong>deben comenzar con</strong> <code class="rounded bg-slate-800 px-2 py-0.5 text-sky-400">test_</code></li>
                      <li>Usa <code class="rounded bg-slate-800 px-2 py-0.5 text-sky-400">assert</code> para verificar condiciones</li>
                      <li><strong>Siempre importa desde</strong> <code class="rounded bg-slate-800 px-2 py-0.5 text-sky-400">app</code> (el archivo del estudiante)</li>
                      <li>Cada función test_* = 1 test completo (sin importar cuántos asserts tenga)</li>
                    </ul>
                  </div>
                </section>

                <!-- Estrategia de ponderación -->
                <section>
                  <h3 class="mb-3 text-lg font-semibold text-sky-400">
                    ⚖️ Estrategia de Ponderación
                  </h3>
                  <div class="rounded-lg border border-indigo-500/30 bg-indigo-950/20 p-4">
                    <p class="mb-3 text-slate-300">
                      Si quieres dar más peso a ciertos criterios, <strong>crea más funciones de test</strong> para ese criterio:
                    </p>
                    <pre class="overflow-x-auto rounded bg-slate-950 p-3 text-sm"><code><span class="text-gray-500"># Dar más peso a la suma (60%) que a la resta (20%) y multiplicación (20%)</span>
<span class="text-purple-400">from</span> <span class="text-cyan-400">app</span> <span class="text-purple-400">import</span> <span class="text-yellow-400">suma</span>, <span class="text-yellow-400">resta</span>, <span class="text-yellow-400">multiplicar</span>

<span class="text-gray-500"># 3 tests para suma = 60% del total</span>
<span class="text-purple-400">def</span> <span class="text-blue-400">test_suma_positivos</span>():
    <span class="text-purple-400">assert</span> <span class="text-yellow-400">suma</span>(<span class="text-orange-400">2</span>, <span class="text-orange-400">3</span>) == <span class="text-orange-400">5</span>

<span class="text-purple-400">def</span> <span class="text-blue-400">test_suma_negativos</span>():
    <span class="text-purple-400">assert</span> <span class="text-yellow-400">suma</span>(-<span class="text-orange-400">2</span>, -<span class="text-orange-400">3</span>) == -<span class="text-orange-400">5</span>

<span class="text-purple-400">def</span> <span class="text-blue-400">test_suma_con_cero</span>():
    <span class="text-purple-400">assert</span> <span class="text-yellow-400">suma</span>(<span class="text-orange-400">5</span>, <span class="text-orange-400">0</span>) == <span class="text-orange-400">5</span>

<span class="text-gray-500"># 1 test para resta = 20% del total</span>
<span class="text-purple-400">def</span> <span class="text-blue-400">test_resta_basica</span>():
    <span class="text-purple-400">assert</span> <span class="text-yellow-400">resta</span>(<span class="text-orange-400">5</span>, <span class="text-orange-400">3</span>) == <span class="text-orange-400">2</span>

<span class="text-gray-500"># 1 test para multiplicación = 20% del total</span>
<span class="text-purple-400">def</span> <span class="text-blue-400">test_multiplicar_basica</span>():
    <span class="text-purple-400">assert</span> <span class="text-yellow-400">multiplicar</span>(<span class="text-orange-400">3</span>, <span class="text-orange-400">4</span>) == <span class="text-orange-400">12</span>

<span class="text-gray-500"># Total: 5 tests = 100 puntos (cada test vale 20 pts)</span></code></pre>
                  </div>
                </section>

                <!-- Casos de prueba -->
                <section>
                  <h3 class="mb-3 text-lg font-semibold text-sky-400">
                    Ejemplos de Tests
                  </h3>
                  <div class="space-y-4">
                    <!-- Casos positivos -->
                    <div class="rounded-lg border border-emerald-500/20 bg-emerald-950/20 p-4">
                      <h4 class="mb-2 font-semibold text-emerald-400">✓ Casos Positivos (Nombres Descriptivos)</h4>
                      <p class="mb-2 text-xs text-slate-400">Los estudiantes verán estos nombres si fallan</p>
                      <pre class="overflow-x-auto rounded bg-slate-950 p-3 text-sm"><code><span class="text-purple-400">from</span> <span class="text-cyan-400">app</span> <span class="text-purple-400">import</span> <span class="text-yellow-400">calcular_promedio</span>

<span class="text-purple-400">def</span> <span class="text-blue-400">test_promedio_numeros_enteros</span>():
    <span class="text-purple-400">assert</span> <span class="text-yellow-400">calcular_promedio</span>([<span class="text-orange-400">5</span>, <span class="text-orange-400">5</span>, <span class="text-orange-400">5</span>]) == <span class="text-orange-400">5</span>
    <span class="text-purple-400">assert</span> <span class="text-yellow-400">calcular_promedio</span>([<span class="text-orange-400">10</span>, <span class="text-orange-400">8</span>, <span class="text-orange-400">9</span>]) == <span class="text-orange-400">9</span>

<span class="text-purple-400">def</span> <span class="text-blue-400">test_promedio_con_decimales</span>():
    <span class="text-purple-400">assert</span> <span class="text-yellow-400">calcular_promedio</span>([<span class="text-orange-400">7.5</span>, <span class="text-orange-400">8.5</span>]) == <span class="text-orange-400">8.0</span></code></pre>
                    </div>

                    <!-- Casos límite -->
                    <div class="rounded-lg border border-yellow-500/20 bg-yellow-950/20 p-4">
                      <h4 class="mb-2 font-semibold text-yellow-400">⚠ Casos Límite (Nombres Genéricos)</h4>
                      <p class="mb-2 text-xs text-slate-400">Nombres genéricos para no dar pistas</p>
                      <pre class="overflow-x-auto rounded bg-slate-950 p-3 text-sm"><code><span class="text-purple-400">from</span> <span class="text-cyan-400">app</span> <span class="text-purple-400">import</span> <span class="text-yellow-400">calcular_promedio</span>

<span class="text-purple-400">def</span> <span class="text-blue-400">test1</span>():
    <span class="text-emerald-400">"""Evalúa el caso de un solo elemento"""</span>
    <span class="text-purple-400">assert</span> <span class="text-yellow-400">calcular_promedio</span>([<span class="text-orange-400">100</span>]) == <span class="text-orange-400">100</span>

<span class="text-purple-400">def</span> <span class="text-blue-400">test2</span>():
    <span class="text-emerald-400">"""Evalúa el caso con cero"""</span>
    <span class="text-purple-400">assert</span> <span class="text-yellow-400">calcular_promedio</span>([<span class="text-orange-400">0</span>]) == <span class="text-orange-400">0</span></code></pre>
                    </div>

                    <!-- Casos de error -->
                    <div class="rounded-lg border border-red-500/20 bg-red-950/20 p-4">
                      <h4 class="mb-2 font-semibold text-red-400">✗ Manejo de Errores</h4>
                      <pre class="overflow-x-auto rounded bg-slate-950 p-3 text-sm"><code><span class="text-purple-400">from</span> <span class="text-cyan-400">app</span> <span class="text-purple-400">import</span> <span class="text-yellow-400">calcular_promedio</span>
<span class="text-purple-400">import</span> <span class="text-cyan-400">pytest</span>

<span class="text-purple-400">def</span> <span class="text-blue-400">test_error_lista_vacia</span>():
    <span class="text-emerald-400">"""Debe lanzar ValueError con lista vacía"""</span>
    <span class="text-purple-400">with</span> pytest.<span class="text-yellow-400">raises</span>(<span class="text-cyan-400">ValueError</span>):
        <span class="text-yellow-400">calcular_promedio</span>([])

<span class="text-purple-400">def</span> <span class="text-blue-400">test_error_tipo_incorrecto</span>():
    <span class="text-emerald-400">"""Debe lanzar TypeError con entrada no válida"""</span>
    <span class="text-purple-400">with</span> pytest.<span class="text-yellow-400">raises</span>(<span class="text-cyan-400">TypeError</span>):
        <span class="text-yellow-400">calcular_promedio</span>(<span class="text-purple-400">None</span>)</code></pre>
                    </div>
                  </div>
                </section>

                <!-- Assertions comunes -->
                <section>
                  <h3 class="mb-3 text-lg font-semibold text-sky-400">
                    Assertions Comunes
                  </h3>
                  <div class="space-y-2 rounded-lg border border-white/10 bg-slate-900/50 p-4">
                    <div class="grid grid-cols-1 gap-3 md:grid-cols-2">
                      <div>
                        <code class="text-sm text-sky-400">assert x == y</code>
                        <p class="mt-1 text-xs text-slate-400">Verifica igualdad</p>
                      </div>
                      <div>
                        <code class="text-sm text-sky-400">assert x != y</code>
                        <p class="mt-1 text-xs text-slate-400">Verifica desigualdad</p>
                      </div>
                      <div>
                        <code class="text-sm text-sky-400">assert x &gt; y</code>
                        <p class="mt-1 text-xs text-slate-400">Mayor que</p>
                      </div>
                      <div>
                        <code class="text-sm text-sky-400">assert x in lista</code>
                        <p class="mt-1 text-xs text-slate-400">Pertenencia</p>
                      </div>
                      <div>
                        <code class="text-sm text-sky-400">assert isinstance(x, tipo)</code>
                        <p class="mt-1 text-xs text-slate-400">Verifica tipo</p>
                      </div>
                      <div>
                        <code class="text-sm text-sky-400">assert len(lista) == n</code>
                        <p class="mt-1 text-xs text-slate-400">Verifica longitud</p>
                      </div>
                    </div>
                  </div>
                </section>

                <!-- Mejores prácticas -->
                <section>
                  <h3 class="mb-3 text-lg font-semibold text-sky-400">
                    Mejores Prácticas
                  </h3>
                  <div class="space-y-3">
                    <div class="flex items-start gap-3 rounded-lg border border-white/10 bg-slate-900/50 p-4">
                      <svg class="mt-0.5 h-5 w-5 flex-shrink-0 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                      </svg>
                      <div>
                        <p class="font-medium text-slate-200">Siempre importar desde "app"</p>
                        <p class="mt-1 text-sm text-slate-400">
                          El código del estudiante siempre se guardará como <code class="rounded bg-slate-800 px-1 text-sky-400">app.py</code>
                        </p>
                      </div>
                    </div>

                    <div class="flex items-start gap-3 rounded-lg border border-white/10 bg-slate-900/50 p-4">
                      <svg class="mt-0.5 h-5 w-5 flex-shrink-0 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                      </svg>
                      <div>
                        <p class="font-medium text-slate-200">Estrategia de nombres de tests</p>
                        <p class="mt-1 text-sm text-slate-400">
                          Decide si usar nombres descriptivos (para guiar) o genéricos (para no dar pistas). Los estudiantes solo ven los nombres de tests fallidos.
                        </p>
                      </div>
                    </div>

                    <div class="flex items-start gap-3 rounded-lg border border-white/10 bg-slate-900/50 p-4">
                      <svg class="mt-0.5 h-5 w-5 flex-shrink-0 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                      </svg>
                      <div>
                        <p class="font-medium text-slate-200">Usa múltiples funciones para ponderación</p>
                        <p class="mt-1 text-sm text-slate-400">
                          Si un criterio es más importante, crea más funciones test_* para ese criterio. Cada función test_* vale lo mismo.
                        </p>
                      </div>
                    </div>

                    <div class="flex items-start gap-3 rounded-lg border border-white/10 bg-slate-900/50 p-4">
                      <svg class="mt-0.5 h-5 w-5 flex-shrink-0 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                      </svg>
                      <div>
                        <p class="font-medium text-slate-200">Documenta tus tests</p>
                        <p class="mt-1 text-sm text-slate-400">
                          Usa docstrings para recordar qué valida cada test (esto no lo ven los estudiantes)
                        </p>
                      </div>
                    </div>

                    <div class="flex items-start gap-3 rounded-lg border border-white/10 bg-slate-900/50 p-4">
                      <svg class="mt-0.5 h-5 w-5 flex-shrink-0 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                      </svg>
                      <div>
                        <p class="font-medium text-slate-200">Cubre múltiples casos</p>
                        <p class="mt-1 text-sm text-slate-400">
                          Incluye casos positivos, negativos, límites y errores en diferentes funciones test_*
                        </p>
                      </div>
                    </div>

                    <div class="flex items-start gap-3 rounded-lg border border-white/10 bg-slate-900/50 p-4">
                      <svg class="mt-0.5 h-5 w-5 flex-shrink-0 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                      </svg>
                      <div>
                        <p class="font-medium text-slate-200">Tests independientes</p>
                        <p class="mt-1 text-sm text-slate-400">
                          Cada test debe funcionar independientemente de los demás
                        </p>
                      </div>
                    </div>
                  </div>
                </section>

                <!-- Ejemplo completo -->
                <section>
                  <h3 class="mb-3 text-lg font-semibold text-sky-400">
                    Ejemplo Completo
                  </h3>
                  <div class="rounded-lg border border-white/10 bg-slate-900/50 p-4">
                    <p class="mb-3 text-sm text-slate-300">Test completo para una función que calcula el factorial:</p>
                    <pre class="overflow-x-auto rounded bg-slate-950 p-4 text-sm"><code><span class="text-gray-500"># Siempre importar desde app</span>
<span class="text-purple-400">from</span> <span class="text-cyan-400">app</span> <span class="text-purple-400">import</span> <span class="text-yellow-400">factorial</span>
<span class="text-purple-400">import</span> <span class="text-cyan-400">pytest</span>

<span class="text-gray-500"># Test 1: Casos positivos básicos (20 puntos)</span>
<span class="text-purple-400">def</span> <span class="text-blue-400">test_factorial_casos_basicos</span>():
    <span class="text-emerald-400">"""Prueba casos básicos de factorial"""</span>
    <span class="text-purple-400">assert</span> <span class="text-yellow-400">factorial</span>(<span class="text-orange-400">0</span>) == <span class="text-orange-400">1</span>
    <span class="text-purple-400">assert</span> <span class="text-yellow-400">factorial</span>(<span class="text-orange-400">1</span>) == <span class="text-orange-400">1</span>
    <span class="text-purple-400">assert</span> <span class="text-yellow-400">factorial</span>(<span class="text-orange-400">5</span>) == <span class="text-orange-400">120</span>

<span class="text-gray-500"># Test 2: Caso más complejo (20 puntos)</span>
<span class="text-purple-400">def</span> <span class="text-blue-400">test_factorial_numero_grande</span>():
    <span class="text-emerald-400">"""Prueba factorial con número grande"""</span>
    <span class="text-purple-400">assert</span> <span class="text-yellow-400">factorial</span>(<span class="text-orange-400">10</span>) == <span class="text-orange-400">3628800</span>

<span class="text-gray-500"># Test 3: Manejo de errores - negativos (20 puntos)</span>
<span class="text-purple-400">def</span> <span class="text-blue-400">test_factorial_numero_negativo</span>():
    <span class="text-emerald-400">"""Debe lanzar error con números negativos"""</span>
    <span class="text-purple-400">with</span> pytest.<span class="text-yellow-400">raises</span>(<span class="text-cyan-400">ValueError</span>):
        <span class="text-yellow-400">factorial</span>(-<span class="text-orange-400">1</span>)
    <span class="text-purple-400">with</span> pytest.<span class="text-yellow-400">raises</span>(<span class="text-cyan-400">ValueError</span>):
        <span class="text-yellow-400">factorial</span>(-<span class="text-orange-400">10</span>)

<span class="text-gray-500"># Test 4: Manejo de errores - tipo string (20 puntos)</span>
<span class="text-purple-400">def</span> <span class="text-blue-400">test_factorial_tipo_string</span>():
    <span class="text-emerald-400">"""Debe lanzar error con strings"""</span>
    <span class="text-purple-400">with</span> pytest.<span class="text-yellow-400">raises</span>(<span class="text-cyan-400">TypeError</span>):
        <span class="text-yellow-400">factorial</span>(<span class="text-emerald-400">"5"</span>)

<span class="text-gray-500"># Test 5: Manejo de errores - tipo float (20 puntos)</span>
<span class="text-purple-400">def</span> <span class="text-blue-400">test_factorial_tipo_float</span>():
    <span class="text-emerald-400">"""Debe lanzar error con decimales"""</span>
    <span class="text-purple-400">with</span> pytest.<span class="text-yellow-400">raises</span>(<span class="text-cyan-400">TypeError</span>):
        <span class="text-yellow-400">factorial</span>(<span class="text-orange-400">5.5</span>)

<span class="text-gray-500"># Total: 5 tests = 100 puntos</span>
<span class="text-gray-500"># Cada test (función test_*) vale 20 puntos</span></code></pre>
                    <div class="mt-3 rounded-lg border border-sky-500/30 bg-sky-950/20 p-3">
                      <p class="text-sm text-sky-200">
                        <strong>Nota:</strong> Este ejemplo tiene 5 funciones test_*, por lo tanto cada una vale 20 puntos. 
                        Si el estudiante pasa 4 de 5 tests, obtiene 80%.
                      </p>
                    </div>
                  </div>
                </section>

                <!-- Qué verán los estudiantes -->
                <section>
                  <h3 class="mb-3 text-lg font-semibold text-sky-400">
                    👁️ ¿Qué Verán los Estudiantes?
                  </h3>
                  <div class="space-y-3">
                    <div class="rounded-lg border border-green-500/30 bg-green-950/20 p-4">
                      <h4 class="mb-2 font-semibold text-green-300">Si pasan todos los tests:</h4>
                      <pre class="overflow-x-auto rounded bg-slate-950 p-3 text-sm text-green-400">Tests Superados: 5
Tests no superados: 0
Tests Totales: 5

Puntaje obtenido: 100%</pre>
                    </div>

                    <div class="rounded-lg border border-red-500/30 bg-red-950/20 p-4">
                      <h4 class="mb-2 font-semibold text-red-300">Si fallan algunos tests:</h4>
                      <pre class="overflow-x-auto rounded bg-slate-950 p-3 text-sm text-red-400">Tests Superados: 3
Tests no superados: 2
Tests Totales: 5

Tests que no pasaron:
  - test_factorial_numero_negativo
  - test_factorial_tipo_float

Puntaje obtenido: 60%</pre>
                      <p class="mt-2 text-sm text-slate-300">
                        ⚠️ Los estudiantes <strong>solo ven los nombres de los tests que fallaron</strong>
                      </p>
                    </div>

                    <div class="rounded-lg border border-amber-500/30 bg-amber-950/20 p-4">
                      <h4 class="mb-2 font-semibold text-amber-300">Si hay errores en el código:</h4>
                      <pre class="overflow-x-auto rounded bg-slate-950 p-3 text-sm text-amber-400">[Errores encontrados al verificar el código]
  > No se encuentra la función 'factorial' en el código</pre>
                      <p class="mt-2 text-sm text-slate-300">
                        Esto ocurre cuando el estudiante no ha definido la función que se intenta importar
                      </p>
                    </div>
                  </div>
                </section>

                <!-- Nota importante -->
                <div class="rounded-lg border border-blue-500/20 bg-blue-950/20 p-4">
                  <div class="flex items-start gap-3">
                    <svg class="mt-0.5 h-5 w-5 flex-shrink-0 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    <div class="text-sm">
                      <p class="font-medium text-blue-300">Resumen:</p>
                      <ul class="mt-2 space-y-1 text-blue-200 list-disc ml-4">
                        <li>Siempre importa desde <strong>app</strong></li>
                        <li>Cada función <strong>test_*()</strong> = 1 test completo</li>
                        <li>El puntaje es automático: <strong>(tests_pasados / tests_totales) × 100</strong></li>
                        <li>Los estudiantes solo ven los nombres de <strong>tests fallidos</strong></li>
                        <li>Para dar más peso a algo, crea <strong>más funciones test_*</strong> para ese criterio</li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Footer -->
            <div class="flex justify-end border-t border-white/10 bg-slate-900/50 px-6 py-4">
              <button
                @click="close"
                class="rounded-lg bg-gradient-to-r from-sky-500 to-blue-600 px-6 py-2.5 text-sm font-medium text-white shadow-lg shadow-sky-500/30 transition-all duration-200 hover:scale-105 hover:shadow-sky-500/50"
              >
                Entendido
              </button>
            </div>
          </div>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
code {
  font-family: 'Fira Code', 'Consolas', 'Monaco', 'Courier New', monospace;
}
</style>
