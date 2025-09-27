<template>
  <div class="min-h-screen bg-slate-900 text-white">
    <!-- Topbar mínima -->
    <header class="sticky top-0 z-40 backdrop-blur bg-slate-900/70 border-b border-white/10">
      <nav class="mx-auto max-w-7xl h-14 px-4 sm:px-6 lg:px-8 flex items-center justify-between">
        <router-link to="/" class="flex items-center gap-2 group">
          <div class="h-7 w-7 rounded-lg bg-gradient-to-br from-fuchsia-500 to-indigo-500 shadow-md group-hover:scale-105 transition-transform"></div>
          <span class="text-lg font-semibold">iEssence</span>
        </router-link>
        <router-link to="/login" class="px-3 py-1.5 rounded-lg border border-white/20 hover:bg-white/10">
          Login
        </router-link>
      </nav>
    </header>

    <!-- Body -->
    <main class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
      <div class="mx-auto w-full max-w-md">
        <!-- Card -->
        <div class="rounded-2xl border border-white/10 bg-slate-900/60 backdrop-blur p-6 sm:p-8 shadow-xl">
          <h2 class="text-2xl font-semibold tracking-tight">Registro</h2>
          <p class="mt-1 text-sm text-slate-300">Crea tu cuenta con correo y contraseña.</p>

          <form class="mt-6 space-y-4" @submit.prevent="doRegister" novalidate>
            <!-- Email -->
            <label class="block">
              <span class="sr-only">Dirección de correo</span>
              <input
                v-model="email"
                type="email"
                required
                autocomplete="email"
                placeholder="Dirección de correo"
                class="w-full rounded-xl bg-white/5 border border-white/10 px-4 py-3 outline-none focus:ring-2 focus:ring-white/40"
              />
            </label>

            <!-- Password -->
            <label class="block">
              <span class="sr-only">Crear contraseña</span>
              <input
                v-model="password"
                type="password"
                required
                autocomplete="new-password"
                placeholder="Crear contraseña"
                class="w-full rounded-xl bg-white/5 border border-white/10 px-4 py-3 outline-none focus:ring-2 focus:ring-white/40"
              />
            </label>

            <!-- Confirm -->
            <label class="block">
              <span class="sr-only">Repite contraseña</span>
              <input
                v-model="confirmPassword"
                type="password"
                required
                autocomplete="new-password"
                placeholder="Repite contraseña"
                class="w-full rounded-xl bg-white/5 border border-white/10 px-4 py-3 outline-none focus:ring-2 focus:ring-white/40"
              />
            </label>

            <!-- Error inline -->
            <p v-if="errorMsg" class="text-sm text-red-400 bg-red-400/10 border border-red-400/30 rounded-lg px-3 py-2">
              {{ errorMsg }}
            </p>

            <!-- Social (placeholder) -->
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-2">
              <button type="button" class="rounded-xl px-3 py-2 bg-[#3b5998] hover:opacity-95">Facebook</button>
              <button type="button" class="rounded-xl px-3 py-2 bg-[#db4437] hover:opacity-95">Google</button>
              <button type="button" class="rounded-xl px-3 py-2 bg-black hover:opacity-95">Apple</button>
            </div>

            <!-- CTA -->
            <div class="flex items-center justify-between">
              <router-link to="/login" class="text-sm text-slate-300 hover:text-white underline underline-offset-4">
                Ya tengo cuenta
              </router-link>
              <button
                type="submit"
                :disabled="loading"
                class="inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-fuchsia-500 to-indigo-500 px-5 py-2.5 font-medium hover:opacity-95 focus:outline-none focus:ring-2 focus:ring-white/40 disabled:opacity-60"
              >
                <svg v-if="loading" class="h-4 w-4 animate-spin" viewBox="0 0 24 24" fill="none">
                  <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-opacity="0.25" stroke-width="4"/>
                  <path d="M22 12a10 10 0 0 1-10 10" stroke="currentColor" stroke-width="4"/>
                </svg>
                <span>Continuar</span>
              </button>
            </div>
          </form>
        </div>

        <p class="mt-6 text-center text-sm text-slate-400">
          Al registrarte aceptas nuestros <a href="#" class="underline underline-offset-4 hover:text-white">Términos</a>.
        </p>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuth } from "@/services/auth";

const router = useRouter();
const auth = useAuth();

const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const loading = ref(false);
const errorMsg = ref("");

const doRegister = async () => {
  errorMsg.value = "";

  if (password.value !== confirmPassword.value) {
    errorMsg.value = "Las contraseñas no coinciden";
    return;
  }

  loading.value = true;
  try {
    await auth.register(email.value, password.value);
    router.push({ name: 'perfil', query: { registered: '1' } });
  } catch (err: any) {
    errorMsg.value =
      err?.response?.data?.message ||
      err?.response?.data?.detail ||
      err?.response?.data?.error ||
      err?.message ||
      "Error en el registro";
  } finally {
    loading.value = false;
  }
};
</script>
