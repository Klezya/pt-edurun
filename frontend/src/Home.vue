<script setup lang="ts">
import { ref, onMounted } from 'vue'

onMounted(async () => {
  // Crea un objeto para manejar los parámetros de la URL actual
  const urlParams = new URLSearchParams(window.location.search);

  // Obtiene el valor del parámetro 'token'
  const ltik = urlParams.get('ltik');
  
  if (ltik) {
    sessionStorage.setItem('ltik', ltik);
    console.log('ltik guardado en sessionStorage:');
  }
  const url = 'https://dithionous-unautomatically-cheri.ngrok-free.dev'
  const result = await fetch(`${url}/info`, {
    method: 'GET',
    headers: {
      'ngrok-skip-browser-warning': 'any',
      'Authorization': 'Bearer ' + sessionStorage.getItem('ltik'),
    },
  })
  .then(res => res.json())

  console.log(result);

});

</script>

<template>
  <div class="flex min-h-dvh flex-col bg-slate-900 text-slate-100">
    <header class="border-b border-slate-800 bg-slate-950 shadow-sm">
      <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div class="flex h-16 items-center justify-between">
          <div class="flex-shrink-0">
            <span class="text-2xl font-bold text-sky-400">Edurun</span>
          </div>
          <nav class="hidden md:block">
            <div class="ml-10 flex items-baseline space-x-4">
              <RouterLink to="/evaluaciones" class="rounded-md px-3 py-2 text-sm font-medium text-slate-200 hover:bg-slate-800 hover:text-white">Estudiante</RouterLink>
              <a href="#" class="rounded-md px-3 py-2 text-sm font-medium text-slate-200 hover:bg-slate-800 hover:text-white">Docente</a>
              <a href="#" class="rounded-md px-3 py-2 text-sm font-medium text-slate-200 hover:bg-slate-800 hover:text-white">Evaluaciones</a>
            </div>
          </nav>
        </div>
      </div>
    </header>

    <main class="flex flex-grow items-center justify-center">
      <div class="mx-auto max-w-7xl px-4 py-6 text-center sm:px-6 lg:px-8">
        <h1 class="text-4xl font-extrabold text-slate-100 sm:text-5xl lg:text-6xl">
          <span class="block">Bienvenido a</span>
          <span class="block text-sky-400">Edurun</span>
        </h1>
        <p class="mt-6 text-lg text-slate-300">Tu plataforma de evaluaciones en línea.</p>
      </div>
    </main>
    <div></div>
    <footer class="mx-auto w-full max-w-7xl px-4 py-6 text-center text-xs text-slate-400">
      © 2025 Edurun. Todos los derechos reservados.
    </footer>
  </div>
</template>


<style scoped></style>
