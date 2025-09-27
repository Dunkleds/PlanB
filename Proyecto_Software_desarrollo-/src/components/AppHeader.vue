<template>
  <header class="sticky top-0 z-40 backdrop-blur bg-slate-900/70 border-b border-white/10">
    <nav class="mx-auto max-w-7xl h-14 px-4 sm:px-6 lg:px-8 flex items-center justify-between">
      <!-- Logo / Home -->
      <router-link to="/" class="flex items-center gap-2 group">
        <div class="h-7 w-7 rounded-lg bg-gradient-to-br from-indigo-500 to-sky-500 shadow-md group-hover:scale-105 transition-transform"></div>
        <span class="text-lg font-semibold text-white">iEssence</span>
      </router-link>

      <!-- Right side -->
      <div class="flex items-center gap-2">
        <!-- NO autenticado: mostrar Login / Registrarse / Privado (si quieres mantenerlo) -->
        <template v-if="!isAuth">
          <router-link
            to="/login"
            class="px-3 py-1.5 rounded-lg border border-white/20 text-white hover:bg-white/10"
          >
            Login
          </router-link>
          <router-link
            to="/register"
            class="px-3 py-1.5 rounded-lg border border-white/20 text-white hover:bg-white/10"
          >
            Registrarse
          </router-link>
          <router-link
            to="/privado"
            class="px-3 py-1.5 rounded-lg border border-white/20 text-white hover:bg-white/10"
          >
            Privado
          </router-link>
        </template>

        <!-- Autenticado: reemplazar por “Hola, username” -->
        <template v-else>
          <router-link
            to="/perfil"
            class="px-3 py-1.5 rounded-xl border border-white/20 text-white hover:bg-white/10"
            :title="`Ir a perfil de ${displayName}`"
          >
            Hola, <span class="font-semibold">{{ displayName }}</span>
          </router-link>
          <button
            @click="signout"
            class="px-3 py-1.5 rounded-xl border border-white/20 text-white hover:bg-white/10"
          >
            Salir
          </button>
        </template>
      </div>
    </nav>
  </header>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'
import { useAuth } from '@/services/auth'

const router = useRouter()
const auth = useAuth()
const { isAuth, user } = storeToRefs(auth)

// Si está autenticado pero aún no tenemos user en memoria, lo traemos
onMounted(async () => {
  if (isAuth.value && !user.value?.email) {
    await auth.fetchMe()
  }
})

// Nombre a mostrar: username o, si no hay, la parte local del email
const displayName = computed(() => {
  if (user.value?.username && user.value.username.trim().length > 0) {
    return user.value.username
  }
  const email = user.value?.email ?? ''
  const local = email.split('@')[0] || 'usuario'
  return local
})

function signout() {
  auth.signout()
  router.replace({ name: 'login' })
}
</script>
