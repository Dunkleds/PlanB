<!-- src/paginas/Terminos.vue -->
<template>
  <div class="min-h-screen bg-slate-900 text-white">
    <main class="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8 py-12">
      <h1 class="text-3xl font-bold">Términos y Condiciones</h1>
      <p class="mt-2 text-slate-300">Última actualización: {{ today }}</p>

      <section class="mt-8 space-y-6">
        <div class="rounded-2xl border border-white/10 bg-slate-900/60 backdrop-blur p-6 shadow">
          <h2 class="text-xl font-semibold">1. Aceptación</h2>
          <p class="mt-2 text-slate-300">
            Al registrarte y usar este sitio, aceptas estos términos y cualquier política adicional
            publicada en la plataforma. Si no estás de acuerdo, por favor no utilices el servicio.
          </p>
        </div>

        <div class="rounded-2xl border border-white/10 bg-slate-900/60 backdrop-blur p-6 shadow">
          <h2 class="text-xl font-semibold">2. Cuentas de usuario</h2>
          <ul class="mt-2 list-disc list-inside text-slate-300 space-y-1">
            <li>Debes proporcionar información verídica.</li>
            <li>Eres responsable de mantener la confidencialidad de tus credenciales.</li>
            <li>Podremos suspender cuentas por incumplimiento de estos términos.</li>
          </ul>
        </div>

        <div class="rounded-2xl border border-white/10 bg-slate-900/60 backdrop-blur p-6 shadow">
          <h2 class="text-xl font-semibold">3. Uso permitido</h2>
          <p class="mt-2 text-slate-300">
            No se permite el uso del servicio para actividades ilegales, spam o ingeniería inversa.
          </p>
        </div>

        <div class="rounded-2xl border border-white/10 bg-slate-900/60 backdrop-blur p-6 shadow">
          <h2 class="text-xl font-semibold">4. Privacidad</h2>
          <p class="mt-2 text-slate-300">
            Tratamos tus datos conforme a nuestra Política de Privacidad. Si requieres una página
            separada de privacidad, podemos crearla y enlazarla aquí.
          </p>
        </div>

        <div class="rounded-2xl border border-white/10 bg-slate-900/60 backdrop-blur p-6 shadow">
          <h2 class="text-xl font-semibold">5. Modificaciones</h2>
          <p class="mt-2 text-slate-300">
            Podemos actualizar estos términos en cualquier momento. Te avisaremos cuando haya cambios
            importantes.
          </p>
        </div>
      </section>

      <div class="mt-10">
        <router-link
          to="/register"
          class="underline underline-offset-4 text-slate-300 hover:text-white"
        >
          Volver al registro
        </router-link>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
const today = new Date().toLocaleDateString();
</script>
