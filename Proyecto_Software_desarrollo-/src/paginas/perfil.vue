<template>
  <main class="mx-auto max-w-3xl px-4 sm:px-6 lg:px-8 py-10 space-y-6">
    <!-- Banner de éxito tras registro -->
    <div v-if="registered" class="rounded-xl border border-emerald-400/30 bg-emerald-400/10 px-4 py-3">
      <p class="text-emerald-300">¡Tu cuenta se creó correctamente! Bienvenido/a.</p>
    </div>

    <section class="grid gap-6">
      <!-- Card: Información básica -->
      <div class="rounded-2xl border border-white/10 bg-white/[0.02] p-6">
        <h2 class="text-xl font-semibold mb-4">Información básica</h2>
        <div class="text-sm text-slate-300 space-y-1">
          <p><span class="text-slate-400">Email:</span> {{ user?.email ?? '—' }}</p>
          <p><span class="text-slate-400">Nombre:</span> <span class="font-medium">{{ user?.first_name || '—' }}</span></p>
          <p><span class="text-slate-400">Apellido:</span> <span class="font-medium">{{ user?.last_name || '—' }}</span></p>
        </div>
      </div>

      <!-- Card: Actualizar nombre -->
      <div class="rounded-2xl border border-white/10 bg-white/[0.02] p-6">
        <h2 class="text-xl font-semibold mb-4">Actualizar datos personales</h2>
        <form @submit.prevent="onUpdateNames" class="grid gap-3">
          <div class="grid gap-3 sm:grid-cols-2">
            <div>
              <label class="block text-sm text-slate-300 mb-1">Nombre</label>
              <input
                v-model="firstName"
                type="text"
                required
                class="w-full rounded-xl bg-slate-800 border border-white/10 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-400"
                placeholder="Nombre"
              />
            </div>
            <div>
              <label class="block text-sm text-slate-300 mb-1">Apellido</label>
              <input
                v-model="lastName"
                type="text"
                required
                class="w-full rounded-xl bg-slate-800 border border-white/10 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-400"
                placeholder="Apellido"
              />
            </div>
          </div>
          <div class="flex items-center gap-3">
            <button
              type="submit"
              :disabled="auth.loading"
              class="inline-flex items-center gap-2 rounded-xl px-4 py-2 bg-indigo-500 hover:bg-indigo-600 focus:outline-none focus:ring-2 focus:ring-indigo-300 disabled:opacity-60"
            >
              Guardar
            </button>
            <span v-if="savedOk" class="text-emerald-300 text-sm">Datos actualizados</span>
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

const firstName = ref('')
const lastName = ref('')
const savedOk = ref(false)

onMounted(async () => {
  if (!auth.isAuth) {
    router.replace({ name: 'login', query: { redirect: '/perfil' } })
    return
  }
  await auth.fetchMe()
  firstName.value = auth.user.first_name ?? ''
  lastName.value = auth.user.last_name ?? ''
})

async function onUpdateNames() {
  savedOk.value = false
  await auth.updateNames(firstName.value.trim(), lastName.value.trim())
  savedOk.value = true
}

function signout() {
  auth.signout()
  router.replace({ name: 'login' })
}
</script>
