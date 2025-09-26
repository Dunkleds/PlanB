<template>
  <div class="home min-h-screen bg-slate-900 text-white">
    <!-- Header -->
    <header
      class="sticky top-0 z-50 backdrop-blur bg-slate-900/70 border-b border-white/10"
      @keydown.esc="closeAll"
    >
      <nav class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <!-- Izquierda: botón menú + logo -->
        <div class="flex items-center gap-3">
          <!-- Botón menú móvil -->
          <button
            class="inline-flex items-center justify-center p-2 rounded-xl hover:bg-white/10 focus:outline-none focus:ring-2 focus:ring-white/40 lg:hidden"
            :aria-expanded="menuOpen ? 'true' : 'false'"
            aria-controls="mobile-menu"
            @click="toggleMenu"
          >
            <span class="sr-only">Abrir menú</span>
            <svg v-if="!menuOpen" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 6h16M4 12h16M4 18h16"/>
            </svg>
            <svg v-else class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>

          <!-- Logo -->
          <router-link to="/" class="flex items-center gap-2 group">
            <div class="h-8 w-8 rounded-xl bg-gradient-to-br from-fuchsia-500 to-indigo-500 shadow-md group-hover:scale-105 transition-transform"></div>
            <h1 class="text-xl font-semibold tracking-tight">iEssence</h1>
          </router-link>

          <!-- Navegación desktop -->
          <ul class="hidden lg:flex items-center gap-1 ml-6">
            <li>
              <router-link
                to="/"
                class="px-3 py-2 rounded-lg hover:bg-white/10 focus:outline-none focus:ring-2 focus:ring-white/40"
                :class="isActive('/')"
              >Inicio</router-link>
            </li>
            <li>
              <router-link
                to="/acerca"
                class="px-3 py-2 rounded-lg hover:bg-white/10 focus:outline-none focus:ring-2 focus:ring-white/40"
                :class="isActive('/acerca')"
              >Acerca</router-link>
            </li>
            <li>
              <router-link
                to="/carrito"
                class="px-3 py-2 rounded-lg hover:bg-white/10 focus:outline-none focus:ring-2 focus:ring-white/40 relative"
                :class="isActive('/carrito')"
              >
                Carro
                <span
                  v-if="cartCount>0"
                  class="absolute -top-1 -right-2 text-[10px] leading-none rounded-full bg-fuchsia-500 px-1.5 py-0.5"
                >{{ cartCount }}</span>
              </router-link>
            </li>
          </ul>
        </div>

        <!-- Derecha: acciones usuario -->
        <div class="flex items-center gap-2">
          <!-- Links auth (ajusta según tu estado real de sesión) -->
          <router-link
            to="/login"
            class="hidden sm:inline-flex items-center px-3 py-2 rounded-lg border border-white/20 hover:border-white/40 hover:bg-white/10 focus:outline-none focus:ring-2 focus:ring-white/40"
          >Login</router-link>

          <router-link
            to="/register"
            class="hidden sm:inline-flex items-center px-3 py-2 rounded-lg bg-gradient-to-r from-fuchsia-500 to-indigo-500 hover:opacity-95 focus:outline-none focus:ring-2 focus:ring-white/40"
          >Registrarse</router-link>

          <router-link
            to="/privado"
            class="hidden md:inline-flex items-center px-3 py-2 rounded-lg hover:bg-white/10 focus:outline-none focus:ring-2 focus:ring-white/40"
          >Privado</router-link>

          <!-- Dropdown usuario -->
          <div class="relative">
            <button
              ref="userBtn"
              @click="toggleUserMenu"
              class="inline-flex items-center gap-2 px-2 py-1.5 rounded-full hover:bg-white/10 focus:outline-none focus:ring-2 focus:ring-white/40"
              :aria-expanded="userMenuOpen ? 'true' : 'false'"
              aria-haspopup="menu"
            >
              <span class="sr-only">Abrir menú de usuario</span>
              <span class="h-8 w-8 rounded-full bg-white/15 grid place-items-center text-sm">👤</span>
              <svg class="h-4 w-4 opacity-70" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 11.17l3.71-3.94a.75.75 0 111.08 1.04l-4.24 4.5a.75.75 0 01-1.08 0L5.21 8.27a.75.75 0 01.02-1.06z" clip-rule="evenodd"/>
              </svg>
            </button>

            <!-- Panel dropdown -->
            <transition
              enter-active-class="transition ease-out duration-150"
              enter-from-class="opacity-0 translate-y-1"
              enter-to-class="opacity-100 translate-y-0"
              leave-active-class="transition ease-in duration-100"
              leave-from-class="opacity-100 translate-y-0"
              leave-to-class="opacity-0 translate-y-1"
            >
              <div
                v-if="userMenuOpen"
                ref="userMenu"
                class="absolute right-0 mt-2 w-56 rounded-xl border border-white/10 bg-slate-900/95 backdrop-blur shadow-xl p-1"
                role="menu"
                @keydown.esc.stop="userMenuOpen=false"
              >
                <router-link to="/perfil" class="block px-3 py-2 rounded-lg hover:bg-white/10" role="menuitem">Perfil</router-link>
                <router-link to="/privado" class="block px-3 py-2 rounded-lg hover:bg-white/10" role="menuitem">Panel privado</router-link>
                <hr class="my-1 border-white/10">
                <button class="w-full text-left px-3 py-2 rounded-lg hover:bg-white/10" role="menuitem">Cerrar sesión</button>
              </div>
            </transition>
          </div>
        </div>
      </nav>

      <!-- Menú móvil -->
      <transition
        enter-active-class="transition duration-150 ease-out"
        enter-from-class="opacity-0 -translate-y-2"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition duration-100 ease-in"
        leave-from-class="opacity-100 translate-y-0"
        leave-to-class="opacity-0 -translate-y-2"
      >
        <div
          v-if="menuOpen"
          id="mobile-menu"
          class="lg:hidden border-t border-white/10 bg-slate-900/90 backdrop-blur"
        >
          <div class="px-4 py-3 space-y-1">
            <router-link @click="closeAll" to="/" class="block px-3 py-2 rounded-lg hover:bg-white/10" :class="isActive('/')">Inicio</router-link>
            <router-link @click="closeAll" to="/carrito" class="block px-3 py-2 rounded-lg hover:bg-white/10" :class="isActive('/carrito')">
              Carro <span v-if="cartCount>0" class="ml-2 text-xs rounded-full bg-fuchsia-500 px-1.5 py-0.5 align-middle">{{ cartCount }}</span>
            </router-link>
            <router-link @click="closeAll" to="/acerca" class="block px-3 py-2 rounded-lg hover:bg-white/10" :class="isActive('/acerca')">Acerca de nosotros</router-link>

            <div class="pt-2 mt-2 border-t border-white/10 grid grid-cols-2 gap-2">
              <router-link @click="closeAll" to="/login" class="px-3 py-2 text-center rounded-lg border border-white/20 hover:bg-white/10">Login</router-link>
              <router-link @click="closeAll" to="/register" class="px-3 py-2 text-center rounded-lg bg-gradient-to-r from-fuchsia-500 to-indigo-500 hover:opacity-95">Registrarse</router-link>
              <router-link @click="closeAll" to="/privado" class="col-span-2 px-3 py-2 text-center rounded-lg hover:bg-white/10">Privado</router-link>
            </div>
          </div>
        </div>
      </transition>
    </header>

    <!-- Contenido -->
    <main class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
      <h2 class="text-3xl font-semibold tracking-tight">Bienvenido a iEssence</h2>
      <p class="mt-2 text-slate-300">Pronto verás aquí el catálogo cuando el endpoint esté listo.</p>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();
const menuOpen = ref(false);
const userMenuOpen = ref(false);
const cartCount = ref(0); // cámbialo cuando conectes tu estado real

const userBtn = ref<HTMLElement | null>(null);
const userMenu = ref<HTMLElement | null>(null);

const toggleMenu = () => (menuOpen.value = !menuOpen.value);
const toggleUserMenu = () => (userMenuOpen.value = !userMenuOpen.value);
const closeAll = () => { menuOpen.value = false; userMenuOpen.value = false; };

const handleClickOutside = (e: MouseEvent) => {
  const t = e.target as Node;
  if (userMenuOpen.value) {
    if (userMenu.value && !userMenu.value.contains(t) && userBtn.value && !userBtn.value.contains(t)) {
      userMenuOpen.value = false;
    }
  }
};

onMounted(() => document.addEventListener("click", handleClickOutside));
onBeforeUnmount(() => document.removeEventListener("click", handleClickOutside));

/** Aplica estilos de link activo sin depender de exact-active-class */
const isActive = (to: string) => {
  const active = route.path === to || route.path.startsWith(to) && to !== "/";
  return active ? "bg-white/10" : "";
};
</script>
