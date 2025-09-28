<template>
  <div class="min-h-screen bg-slate-900 text-white">
    <main class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
      <div class="mx-auto w-full max-w-md">
        <div class="rounded-2xl border border-white/10 bg-slate-900/60 backdrop-blur p-6 sm:p-8 shadow-xl">
          <h2 class="text-2xl font-semibold tracking-tight">
            {{ isConfirm ? 'Define tu nueva contraseña' : 'Recuperar contraseña' }}
          </h2>
          <p class="mt-1 text-sm text-slate-300">
            {{ isConfirm
              ? 'Ingresa tu nueva contraseña para finalizar el proceso.'
              : 'Escribe tu correo y te enviaremos un enlace para restablecerla.' }}
          </p>

          <!-- Paso 1: pedir correo -->
          <form v-if="!isConfirm" class="mt-6 space-y-4" @submit.prevent="sendEmail">
            <label class="block">
              <span class="sr-only">Correo</span>
              <input
                v-model="email"
                type="email"
                required
                autocomplete="email"
                placeholder="tu@correo.com"
                class="w-full rounded-xl bg-white/5 border border-white/10 px-4 py-3 outline-none focus:ring-2 focus:ring-white/40"
              />
            </label>

            <p v-if="msg" class="text-sm text-emerald-400 bg-emerald-400/10 border border-emerald-400/30 rounded-lg px-3 py-2">{{ msg }}</p>
            <p v-if="errorMsg" class="text-sm text-red-400 bg-red-400/10 border border-red-400/30 rounded-lg px-3 py-2">{{ errorMsg }}</p>

            <div class="flex items-center justify-between">
              <router-link to="/login" class="text-sm text-slate-300 hover:text-white underline underline-offset-4">
                Volver a login
              </router-link>
              <button
                type="submit"
                :disabled="loading"
                class="inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-fuchsia-500 to-indigo-500 px-5 py-2.5 font-medium hover:opacity-95 disabled:opacity-60"
              >
                <svg v-if="loading" class="h-4 w-4 animate-spin" viewBox="0 0 24 24" fill="none">
                  <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-opacity="0.25" stroke-width="4"/>
                  <path d="M22 12a10 10 0 0 1-10 10" stroke="currentColor" stroke-width="4"/>
                </svg>
                <span>{{ loading ? "Enviando..." : "Enviar enlace" }}</span>
              </button>
            </div>
          </form>

          <!-- Paso 2: confirmar y cambiar contraseña -->
          <form v-else class="mt-6 space-y-4" @submit.prevent="setNewPassword">
            <label class="block">
              <span class="sr-only">Nueva contraseña</span>
              <input
                :type="showPwd ? 'text' : 'password'"
                v-model="newPassword"
                required
                placeholder="Nueva contraseña"
                class="w-full rounded-xl bg-white/5 border border-white/10 px-4 py-3 pr-12 outline-none focus:ring-2 focus:ring-white/40"
              />
            </label>

            <label class="block">
              <span class="sr-only">Repite contraseña</span>
              <input
                :type="showPwd ? 'text' : 'password'"
                v-model="confirm"
                required
                placeholder="Repite contraseña"
                class="w-full rounded-xl bg-white/5 border border-white/10 px-4 py-3 pr-12 outline-none focus:ring-2 focus:ring-white/40"
              />
            </label>

            <button
              type="button"
              class="text-sm text-slate-300 hover:text-white underline underline-offset-4"
              @click="showPwd = !showPwd"
            >
              {{ showPwd ? 'Ocultar' : 'Mostrar' }} contraseñas
            </button>

            <p v-if="msg" class="text-sm text-emerald-400 bg-emerald-400/10 border border-emerald-400/30 rounded-lg px-3 py-2">{{ msg }}</p>
            <p v-if="errorMsg" class="text-sm text-red-400 bg-red-400/10 border border-red-400/30 rounded-lg px-3 py-2">{{ errorMsg }}</p>

            <div class="flex items-center justify-between">
              <router-link to="/login" class="text-sm text-slate-300 hover:text-white underline underline-offset-4">
                Volver a login
              </router-link>
              <button
                type="submit"
                :disabled="loading"
                class="inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-fuchsia-500 to-indigo-500 px-5 py-2.5 font-medium hover:opacity-95 disabled:opacity-60"
              >
                <svg v-if="loading" class="h-4 w-4 animate-spin" viewBox="0 0 24 24" fill="none">
                  <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-opacity="0.25" stroke-width="4"/>
                  <path d="M22 12a10 10 0 0 1-10 10" stroke="currentColor" stroke-width="4"/>
                </svg>
                <span>{{ loading ? "Guardando..." : "Cambiar contraseña" }}</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { requestPasswordReset, confirmPasswordReset } from "@/services/auth";

const route = useRoute();
const router = useRouter();

const email = ref("");
const newPassword = ref("");
const confirm = ref("");
const loading = ref(false);
const errorMsg = ref("");
const msg = ref("");
const showPwd = ref(false);


const uid = computed(() => String(route.query.uid || ""));
const token = computed(() => String(route.query.token || ""));
const isConfirm = computed(() => !!uid.value && !!token.value);


const sendEmail = async () => {
  errorMsg.value = ""; msg.value = ""; loading.value = true;
  try {
    await requestPasswordReset(email.value);
    msg.value = "Si el correo existe, te enviamos un enlace para restablecer la contraseña.";
  } catch (e: any) {
    errorMsg.value = e?.response?.data?.detail || e?.message || "Error al enviar el correo";
  } finally {
    loading.value = false;
  }
};

const setNewPassword = async () => {
  errorMsg.value = ""; msg.value = "";
  if (newPassword.value !== confirm.value) {
    errorMsg.value = "Las contraseñas no coinciden."; return;
  }
  loading.value = true;
  try {
    await confirmPasswordReset({ uid: uid.value, token: token.value, new_password: newPassword.value });
    msg.value = "Contraseña actualizada. Redirigiendo al login…";
    setTimeout(() => router.replace("/login"), 1200);
  } catch (e: any) {
    errorMsg.value = e?.response?.data?.detail || e?.message || "No se pudo actualizar la contraseña.";
  } finally {
    loading.value = false;
  }
};
</script>
