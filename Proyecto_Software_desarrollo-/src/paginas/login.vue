<template>
  <div class="min-h-screen bg-slate-900 text-white">
    <!-- Topbar mínima -->
    <header class="sticky top-0 z-40 backdrop-blur bg-slate-900/70 border-b border-white/10">
      <nav class="mx-auto max-w-7xl h-14 px-4 sm:px-6 lg:px-8 flex items-center justify-between">
        <router-link to="/" class="flex items-center gap-2 group">
          <div class="h-7 w-7 rounded-lg bg-gradient-to-br from-fuchsia-500 to-indigo-500 shadow-md group-hover:scale-105 transition-transform"></div>
          <span class="text-lg font-semibold">iEssence</span>
        </router-link>
        <router-link to="/register" class="px-3 py-1.5 rounded-lg border border-white/20 hover:bg-white/10">
          Registrarse
        </router-link>
      </nav>
    </header>

    <!-- Body -->
    <main class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
      <div class="mx-auto w-full max-w-md">
        <!-- Card -->
        <div class="rounded-2xl border border-white/10 bg-slate-900/60 backdrop-blur p-6 sm:p-8 shadow-xl">
          <h2 class="text-2xl font-semibold tracking-tight">Ingresa</h2>
          <p class="mt-1 text-sm text-slate-300">Usa tu correo y contraseña para continuar.</p>

          <form class="mt-6 space-y-4" @submit.prevent="doLogin" novalidate>
            <!-- Email -->
            <label class="block">
              <span class="sr-only">Correo</span>
              <input
                v-model="email"
                type="email"
                required
                autocomplete="email"
                placeholder="Dirección de correo"
                class="w-full rounded-xl bg-white/5 border border-white/10 px-4 py-3 outline-none focus:ring-2 focus:ring-white/40"
              />
            </label>

            <!-- Password + toggle -->
            <div class="relative">
              <label class="block">
                <span class="sr-only">Contraseña</span>
                <input
                  :type="showPwd ? 'text' : 'password'"
                  v-model="password"
                  required
                  autocomplete="current-password"
                  placeholder="Contraseña"
                  class="w-full rounded-xl bg-white/5 border border-white/10 px-4 py-3 pr-12 outline-none focus:ring-2 focus:ring-white/40"
                />
              </label>
              <button
                type="button"
                @click="showPwd = !showPwd"
                class="absolute inset-y-0 right-0 px-3 grid place-items-center text-slate-300 hover:text-white"
                :aria-pressed="showPwd ? 'true' : 'false'"
              >
                <span class="sr-only">Mostrar/ocultar contraseña</span>
                <svg v-if="!showPwd" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M2.036 12.322a1 1 0 010-.644C3.423 7.51 7.36 5 12 5c4.64 0 8.577 2.51 9.964 6.678.05.161.05.335 0 .496C20.576 16.49 16.639 19 12 19c-4.64 0-8.577-2.51-9.964-6.678z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 3l18 18M10.585 10.585A3 3 0 0013.5 13.5M6.79 6.79C4.95 7.864 3.6 9.47 2.964 11.356a1 1 0 000 .644C4.423 16.49 8.36 19 13 19c1.43 0 2.79-.25 4.037-.708M9.88 4.252A10.9 10.9 0 0113 4c4.64 0 8.577 2.51 9.964 6.678.05.161.05.335 0 .496a11.04 11.04 0 01-2.29 3.57"/></svg>
              </button>
            </div>

            <!-- Error -->
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
              <router-link to="/register" class="text-sm text-slate-300 hover:text-white underline underline-offset-4">
                Crear cuenta
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
                <span>{{ loading ? "Ingresando..." : "Continuar" }}</span>
              </button>
            </div>
          </form>
        </div>

        <!-- Nota -->
        <p class="mt-6 text-center text-sm text-slate-400">
          ¿Olvidaste tu contraseña? <a href="#" class="underline underline-offset-4 hover:text-white">Recupérala</a>
        </p>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuth } from "@/services/auth";

const router = useRouter();
const route = useRoute();
const auth = useAuth();

const email = ref("");
const password = ref("");
const loading = ref(false);
const errorMsg = ref("");
const showPwd = ref(false);

const doLogin = async () => {
  errorMsg.value = "";
  loading.value = true;
  try {
    await auth.login(email.value, password.value);
    const redirect = typeof route.query.redirect === "string" ? route.query.redirect : '/perfil';
    router.replace(redirect || '/perfil');
  } catch (err: any) {
    errorMsg.value =
      err?.response?.data?.message ||
      err?.response?.data?.detail ||
      err?.response?.data?.error ||
      err?.message ||
      "Error de login";
  } finally {
    loading.value = false;
  }
};
</script>
