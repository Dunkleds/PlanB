// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import { useAuth } from '@/services/auth'



import Home from '@/paginas/home.vue'
import Inventario from '@/paginas/inventario.vue'
import Reportes from '@/paginas/Reportes.vue'
import Login from '@/paginas/login.vue'
import Register from '@/paginas/register.vue'
import Carrito from '@/paginas/carrito.vue'
import Acerca from '@/paginas/acerca.vue'
import Privado from '@/paginas/privado.vue'
import Perfil from '@/paginas/perfil.vue'
import Terminos from "@/paginas/Terminos.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL || '/'),
  routes: [
    { path: '/',           name: 'home',       component: Home },
    { path: '/inventario', name: 'inventario', component: Inventario, meta: { requiresAuth: true } },
    { path: '/reportes',   name: 'reportes',   component: Reportes,   meta: { requiresAuth: true } },
    { path: '/login',      name: 'login',      component: Login },
    { path: '/register',   name: 'register',   component: Register },
    { path: '/privado',    name: 'privado',    component: Privado,    meta: { requiresAuth: true } },
    { path: '/perfil',    name: 'perfil',    component: Perfil,    meta: { requiresAuth: true } },
    { path: '/carrito',    name: 'carrito',    component: Carrito },
    { path: '/acerca',     name: 'acerca',     component: Acerca },
    { path: '/:pathMatch(.*)*', redirect: '/' },
    { path: "/terminos", name: "terminos", component: Terminos, meta: { requiresAuth: false } }
  ],
})

// Guard mínimo: si la ruta pide auth y no hay token, manda a /login
// NOTE: this guard stays local-storage based until an auth.init() bootstraps the user profile.
router.beforeEach((to) => {
  if (!to.meta?.requiresAuth) return true

  // intenta usar el store de Pinia si ya está disponible…
  try {
    const auth = useAuth()
    if (auth?.isAuth) return true
  } catch (_) {
    // Pinia aún no inicializado; cae al fallback
  }

  // …fallback directo a localStorage (por si el store no está listo)
  const isAuth = !!localStorage.getItem('access_token')
  if (!isAuth) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }
  return true
})

export default router

