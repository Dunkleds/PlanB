<template>
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
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useAuth } from '@/services/auth'

const auth = useAuth()

// Extrae refs tipadas desde el store (mantiene reactividad)
const { user } = storeToRefs(auth)

// Campos derivados seguros para el template
const email = computed(() => user.value.email)
const username = computed(() => user.value.username)
</script>
