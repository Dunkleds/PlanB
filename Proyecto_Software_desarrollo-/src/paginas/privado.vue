<template>
  <div class="min-h-screen bg-slate-900 text-white">
    <header class="sticky top-0 z-40 backdrop-blur bg-slate-900/70 border-b border-white/10">
      <nav class="mx-auto max-w-7xl h-14 px-4 sm:px-6 lg:px-8 flex items-center justify-between">
        <router-link to="/" class="flex items-center gap-2">
          <div class="h-7 w-7 rounded-lg bg-gradient-to-br from-indigo-500 to-sky-500 shadow-md"></div>
          <span class="text-lg font-semibold">Área Privada</span>
        </router-link>
        <div class="flex gap-2">
          <router-link to="/perfil" class="px-3 py-1.5 rounded-lg border border-white/20 hover:bg-white/10">Perfil</router-link>
          <button @click="signout" class="px-3 py-1.5 rounded-lg border border-white/20 hover:bg-white/10">Salir</button>
        </div>
      </nav>
    </header>

    <main class="mx-auto max-w-3xl px-4 sm:px-6 lg:px-8 py-10 space-y-6">
      <h1 class="text-2xl font-semibold">Bienvenido</h1>

      <div class="rounded-2xl border border-white/10 bg-white/[0.02] p-6">
        <p class="text-slate-300">
          Sesión iniciada como
          <span class="font-medium">{{ email ?? '—' }}</span>
        </p>
        <p class="text-slate-400 text-sm">Username: <span class="text-slate-200">{{ username ?? '—' }}</span></p>
      </div>

      <router-link
        to="/perfil"
        class="inline-flex items-center rounded-xl px-4 py-2 bg-indigo-500 hover:bg-indigo-600 focus:outline-none focus:ring-2 focus:ring-indigo-300"
      >
        Ir a mi perfil
      </router-link>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'
import { useAuth } from '@/services/auth'

const router = useRouter()
const auth = useAuth()

// Extrae refs tipadas desde el store (mantiene reactividad)
const { user, isAuth } = storeToRefs(auth)

// Campos derivados seguros para el template
const email = computed(() => user.value.email)
const username = computed(() => user.value.username)

function signout() {
  auth.signout()
  router.replace({ name: 'login' })
}
</script>
