<template>
  <div class="min-h-screen bg-slate-900 text-white">
    <main class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
      <div class="mx-auto w-full max-w-md">
        <!-- Card -->
        <div class="rounded-2xl border border-white/10 bg-slate-900/60 backdrop-blur p-6 sm:p-8 shadow-xl">
          <h2 class="text-2xl font-semibold tracking-tight">Registro</h2>
          <p class="mt-1 text-sm text-slate-300">Crea tu cuenta con correo y contraseña.</p>

          <form class="mt-6 space-y-4" @submit.prevent="doRegister" novalidate>
            <label class="block">
              <span class="sr-only">Nombre</span>
              <input
                v-model="firstName"
                type="text"
                required
                autocomplete="given-name"
                placeholder="Nombre"
                class="w-full rounded-xl bg-white/5 border border-white/10 px-4 py-3 outline-none focus:ring-2 focus:ring-white/40"
              />
            </label>

            <label class="block">
              <span class="sr-only">Apellido</span>
              <input
                v-model="lastName"
                type="text"
                required
                autocomplete="family-name"
                placeholder="Apellido"
                class="w-full rounded-xl bg-white/5 border border-white/10 px-4 py-3 outline-none focus:ring-2 focus:ring-white/40"
              />
            </label>

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

            <!-- Password (con mostrar/ocultar) -->
            <div class="relative">
              <label class="block">
                <span class="sr-only">Crear contraseña</span>
                <input
                  :type="showPwd ? 'text' : 'password'"
                  v-model="password"
                  required
                  autocomplete="new-password"
                  placeholder="Crear contraseña"
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
                <!-- ojo abierto/cerrado -->
                <svg v-if="!showPwd" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5"
                     viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                        d="M2.036 12.322a1 1 0 010-.644C3.423 7.51 7.36 5 12 5c4.64 0 8.577 2.51 9.964 6.678.05.161.05.335 0 .496C20.576 16.49 16.639 19 12 19c-4.64 0-8.577-2.51-9.964-6.678z"/>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                        d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5"
                     viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                        d="M3 3l18 18M10.585 10.585A3 3 0 0013.5 13.5M6.79 6.79C4.95 7.864 3.6 9.47 2.964 11.356a1 1 0 000 .644C4.423 16.49 8.36 19 13 19c1.43 0 2.79-.25 4.037-.708M9.88 4.252A10.9 10.9 0 0113 4c4.64 0 8.577 2.51 9.964 6.678.05.161.05.335 0 .496a11.04 11.04 0 01-2.29 3.57"/>
                </svg>
              </button>
            </div>

            <!-- Confirm Password (con mostrar/ocultar) -->
            <div class="relative">
              <label class="block">
                <span class="sr-only">Repite contraseña</span>
                <input
                  :type="showPwd2 ? 'text' : 'password'"
                  v-model="confirmPassword"
                  required
                  autocomplete="new-password"
                  placeholder="Repite contraseña"
                  class="w-full rounded-xl bg-white/5 border border-white/10 px-4 py-3 pr-12 outline-none focus:ring-2 focus:ring-white/40"
                />
              </label>
              <button
                type="button"
                @click="showPwd2 = !showPwd2"
                class="absolute inset-y-0 right-0 px-3 grid place-items-center text-slate-300 hover:text-white"
                :aria-pressed="showPwd2 ? 'true' : 'false'"
              >
                <span class="sr-only">Mostrar/ocultar contraseña</span>
                <svg v-if="!showPwd2" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5"
                     viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                        d="M2.036 12.322a1 1 0 010-.644C3.423 7.51 7.36 5 12 5c4.64 0 8.577 2.51 9.964 6.678.05.161.05.335 0 .496C20.576 16.49 16.639 19 12 19c-4.64 0-8.577-2.51-9.964-6.678z"/>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                        d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5"
                     viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                        d="M3 3l18 18M10.585 10.585A3 3 0 0013.5 13.5M6.79 6.79C4.95 7.864 3.6 9.47 2.964 11.356a1 1 0 000 .644C4.423 16.49 8.36 19 13 19c1.43 0 2.79-.25 4.037-.708M9.88 4.252A10.9 10.9 0 0113 4c4.64 0 8.577 2.51 9.964 6.678.05.161.05.335 0 .496a11.04 11.04 0 01-2.29 3.57"/>
                </svg>
              </button>
            </div>

            <!-- Error inline -->
            <p
              v-if="errorMsg"
              class="text-sm text-red-400 bg-red-400/10 border border-red-400/30 rounded-lg px-3 py-2 whitespace-pre-line"
            >
              {{ errorMsg }}
            </p>

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
          Al registrarte aceptas nuestros
          <router-link
            to="/terminos"
            class="underline underline-offset-4 hover:text-white"
          > Términos y Condiciones</router-link>
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

const firstName = ref("");
const lastName = ref("");
const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const loading = ref(false);
const errorMsg = ref("");

// toggles de visibilidad
const showPwd = ref(false);
const showPwd2 = ref(false);

const doRegister = async () => {
  errorMsg.value = "";

  if (!firstName.value.trim() || !lastName.value.trim()) {
    errorMsg.value = "Ingresa tu nombre y apellido";
    return;
  }

  if (password.value !== confirmPassword.value) {
    errorMsg.value = "Las contraseñas no coinciden";
    return;
  }

  loading.value = true;
  try {
    await auth.register(email.value, password.value, firstName.value.trim(), lastName.value.trim());
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
