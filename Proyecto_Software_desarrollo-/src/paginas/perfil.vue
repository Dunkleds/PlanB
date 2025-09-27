<template>
  <div class="min-h-screen bg-slate-900 text-white">
    <!-- Topbar -->
    <header class="sticky top-0 z-40 backdrop-blur bg-slate-900/70 border-b border-white/10">
      <nav class="mx-auto max-w-7xl h-14 px-4 sm:px-6 lg:px-8 flex items-center justify-between">
        <router-link to="/" class="flex items-center gap-2 group">
          <div class="h-7 w-7 rounded-lg bg-gradient-to-br from-indigo-500 to-sky-500 shadow-md group-hover:scale-105 transition-transform"></div>
          <span class="text-lg font-semibold">iEssence</span>
        </router-link>

        <div class="flex gap-2">
          <router-link to="/" class="px-3 py-1.5 rounded-lg border border-white/20 hover:bg-white/10">Inicio</router-link>
          <button @click="signout" class="px-3 py-1.5 rounded-lg border border-white/20 hover:bg-white/10">Salir</button>
        </div>
      </nav>
    </header>

    <main class="mx-auto max-w-3xl px-4 sm:px-6 lg:px-8 py-10 space-y-6">
      <!-- Banner de éxito tras registro -->
      <div v-if="registered" class="rounded-xl border border-emerald-400/30 bg-emerald-400/10 px-4 py-3">
        <p class="text-emerald-300">¡Tu cuenta se creó correctamente! Bienvenido/a.</p>
      </div>

      <section class="grid gap-6">
        <!-- Card: Información básica -->
        <div class="rounded-2xl border border-white/10 bg-white/[0.02] p-6">
          <h2 class="text-xl font-semibold mb-4">Perfil</h2>
          <div class="text-sm text-slate-300 space-y-1">
            <p><span class="text-slate-400">ID:</span> {{ user?.id ?? '—' }}</p>
            <p><span class="text-slate-400">Email:</span> {{ user?.email ?? '—' }}</p>
            <p><span class="text-slate-400">Username actual:</span> <span class="font-medium">{{ user?.username ?? '—' }}</span></p>
          </div>
        </div>

        <!-- Card: Cambiar username -->
        <div class="rounded-2xl border border-white/10 bg-white/[0.02] p-6">
          <h2 class="text-xl font-semibold mb-4">Editar username</h2>
          <form @submit.prevent="onChangeUsername" class="grid gap-3">
            <div>
              <label class="block text-sm text-slate-300 mb-1">Nuevo username</label>
              <input
                v-model="newUsername"
                type="text"
                required
                minlength="3"
                class="w-full rounded-xl bg-slate-800 border border-white/10 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-400"
                placeholder="tu_nuevo_username"
              />
            </div>
            <div class="flex items-center gap-3">
              <button
                type="submit"
                :disabled="auth.loading"
                class="inline-flex items-center gap-2 rounded-xl px-4 py-2 bg-indigo-500 hover:bg-indigo-600 focus:outline-none focus:ring-2 focus:ring-indigo-300 disabled:opacity-60"
              >
                Guardar
              </button>
              <span v-if="savedOk" class="text-emerald-300 text-sm">Guardado correctamente</span>
            </div>
            <p v-if="auth.error" class="text-red-400 text-sm">{{ auth.error }}</p>
          </form>
        </div>

        <!-- Card: Opciones varias -->
        <div class="rounded-2xl border border-white/10 bg-white/[0.02] p-6">
          <h2 class="text-xl font-semibold mb-4">Opciones</h2>
          <ul class="grid gap-2 text-sm">
            <li class="flex items-center justify-between">
              <span class="text-slate-300">Cambiar contraseña (próximamente)</span>
              <button disabled class="px-3 py-1.5 rounded-lg border border-white/10 text-slate-400">En desarrollo</button>
            </li>
            <li class="flex items-center justify-between">
              <span class="text-slate-300">Cerrar sesión</span>
              <button @click="signout" class="px-3 py-1.5 rounded-lg border border-white/20 hover:bg-white/10">Salir</button>
            </li>
          </ul>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuth } from '@/services/auth'

const route = useRoute()
const router = useRouter()
const auth = useAuth()

const registered = computed(() => route.query.registered === '1')
const user = computed(() => auth.user)

const newUsername = ref('')
const savedOk = ref(false)

onMounted(async () => {
  if (!auth.isAuth) {
    router.replace({ name: 'login', query: { redirect: '/perfil' } })
    return
  }
  await auth.fetchMe()
  newUsername.value = auth.user.username ?? ''
})

async function onChangeUsername() {
  savedOk.value = false
  await auth.changeUsername(newUsername.value.trim())
  savedOk.value = true
}

function signout() {
  auth.signout()
  router.replace({ name: 'login' })
}
</script>
