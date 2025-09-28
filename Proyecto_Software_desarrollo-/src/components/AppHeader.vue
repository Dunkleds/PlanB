<template>
  <header
    class="sticky top-0 z-50 backdrop-blur bg-slate-900/70 border-b border-white/10"
    @keydown.esc="closeAll"
  >
    <nav class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <button
          class="inline-flex items-center justify-center p-2 rounded-xl hover:bg-white/10 focus:outline-none focus:ring-2 focus:ring-white/40 lg:hidden"
          :aria-expanded="menuOpen ? 'true' : 'false'"
          aria-controls="mobile-menu"
          @click="toggleMenu"
        >
          <span class="sr-only">Abrir menú</span>
          <svg v-if="!menuOpen" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
          <svg v-else class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        <router-link to="/" class="flex items-center gap-2 group">
          <div class="h-8 w-8 rounded-xl bg-gradient-to-br from-fuchsia-500 to-indigo-500 shadow-md group-hover:scale-105 transition-transform"></div>
          <span class="text-xl font-semibold tracking-tight text-white">iEssence</span>
        </router-link>

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

      <div class="flex items-center gap-2">
        <template v-if="!isAuth">
          <router-link
            to="/login"
            class="hidden sm:inline-flex items-center px-3 py-2 rounded-lg border border-white/20 hover:border-white/40 hover:bg-white/10 focus:outline-none focus:ring-2 focus:ring-white/40"
            @click="closeAll"
          >Login</router-link>

          <router-link
            to="/register"
            class="hidden sm:inline-flex items-center px-3 py-2 rounded-lg bg-gradient-to-r from-fuchsia-500 to-indigo-500 hover:opacity-95 focus:outline-none focus:ring-2 focus:ring-white/40"
            @click="closeAll"
          >Registrarse</router-link>

          <router-link
            to="/privado"
            class="hidden md:inline-flex items-center px-3 py-2 rounded-lg hover:bg-white/10 focus:outline-none focus:ring-2 focus:ring-white/40"
            @click="closeAll"
          >Privado</router-link>
        </template>

        <template v-else>
          <div class="relative">
            <button
              ref="userBtn"
              @click="toggleUserMenu"
              class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full hover:bg-white/10 focus:outline-none focus:ring-2 focus:ring-white/40"
              :aria-expanded="userMenuOpen ? 'true' : 'false'"
              aria-haspopup="menu"
            >
              <span class="sr-only">Abrir menú de usuario</span>
              <span class="hidden sm:inline text-sm text-white">Hola, <span class="font-semibold">{{ displayName }}</span></span>
              <span class="sm:hidden h-8 w-8 rounded-full bg-white/15 grid place-items-center text-sm">👤</span>
              <svg class="h-4 w-4 opacity-70" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 11.17l3.71-3.94a.75.75 0 111.08 1.04l-4.24 4.5a.75.75 0 01-1.08 0L5.21 8.27a.75.75 0 01.02-1.06z" clip-rule="evenodd" />
              </svg>
            </button>

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
                <p class="px-3 py-2 text-sm text-slate-300">Hola, <span class="font-semibold text-white">{{ displayName }}</span></p>
                <router-link to="/perfil" class="block px-3 py-2 rounded-lg hover:bg-white/10" role="menuitem" @click="closeAll">Perfil</router-link>
                <router-link to="/privado" class="block px-3 py-2 rounded-lg hover:bg-white/10" role="menuitem" @click="closeAll">Panel privado</router-link>
                <hr class="my-1 border-white/10" />
                <button class="w-full text-left px-3 py-2 rounded-lg hover:bg-white/10" role="menuitem" @click="handleLogout">Cerrar sesión</button>
              </div>
            </transition>
          </div>
        </template>
      </div>
    </nav>

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
            <template v-if="!isAuth">
              <router-link @click="closeAll" to="/login" class="px-3 py-2 text-center rounded-lg border border-white/20 hover:bg-white/10">Login</router-link>
              <router-link @click="closeAll" to="/register" class="px-3 py-2 text-center rounded-lg bg-gradient-to-r from-fuchsia-500 to-indigo-500 hover:opacity-95">Registrarse</router-link>
              <router-link @click="closeAll" to="/privado" class="col-span-2 px-3 py-2 text-center rounded-lg hover:bg-white/10">Privado</router-link>
            </template>
            <template v-else>
              <router-link @click="closeAll" to="/perfil" class="col-span-2 px-3 py-2 text-center rounded-lg hover:bg-white/10">Perfil</router-link>
              <router-link @click="closeAll" to="/privado" class="col-span-2 px-3 py-2 text-center rounded-lg hover:bg-white/10">Panel privado</router-link>
              <button @click="handleLogout" class="col-span-2 px-3 py-2 text-center rounded-lg border border-white/20 hover:bg-white/10">Cerrar sesión</button>
            </template>
          </div>
        </div>
      </div>
    </transition>
  </header>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useRoute, useRouter } from 'vue-router'
import { useAuth } from '@/services/auth'

const router = useRouter()
const route = useRoute()
const auth = useAuth()
const { isAuth, user } = storeToRefs(auth)

const menuOpen = ref(false)
const userMenuOpen = ref(false)
const userBtn = ref<HTMLElement | null>(null)
const userMenu = ref<HTMLElement | null>(null)
const cartCount = ref(0) // integra tu estado real cuando esté disponible

const toggleMenu = () => {
  menuOpen.value = !menuOpen.value
  if (menuOpen.value) {
    userMenuOpen.value = false
  }
}

const toggleUserMenu = () => {
  if (!isAuth.value) return
  userMenuOpen.value = !userMenuOpen.value
  if (userMenuOpen.value) {
    menuOpen.value = false
  }
}

const closeAll = () => {
  menuOpen.value = false
  userMenuOpen.value = false
}

const handleClickOutside = (event: MouseEvent) => {
  if (!userMenuOpen.value) return
  const target = event.target as Node
  if (userMenu.value && !userMenu.value.contains(target) && userBtn.value && !userBtn.value.contains(target)) {
    userMenuOpen.value = false
  }
}

watch(
  () => route.path,
  () => closeAll(),
)

onMounted(async () => {
  document.addEventListener('click', handleClickOutside)
  if (isAuth.value && !user.value?.email) {
    await auth.fetchMe()
  }
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})

const displayName = computed(() => {
  if (user.value?.username && user.value.username.trim().length > 0) {
    return user.value.username
  }
  const email = user.value?.email ?? ''
  const local = email.split('@')[0] || 'usuario'
  return local
})

const isActive = (to: string) => {
  const active = route.path === to || (route.path.startsWith(to) && to !== '/')
  return active ? 'bg-white/10' : ''
}

const handleLogout = () => {
  auth.signout()
  closeAll()
  router.replace({ name: 'login' })
}
</script>
