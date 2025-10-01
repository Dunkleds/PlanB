// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import { useAuth } from '@/services/auth'

// Páginas públicas y privadas existentes
import Home from '@/paginas/home.vue'
import Inventario from '@/paginas/inventario.vue'
import Reportes from '@/paginas/Reportes.vue'
import Login from '@/paginas/login.vue'
import Register from '@/paginas/register.vue'
import Carrito from '@/paginas/carrito.vue'
import Acerca from '@/paginas/acerca.vue'
import Privado from '@/paginas/privado.vue'

// ✅ NUEVAS páginas del administrador
const AdminHome = () => import('@/paginas/Admin/adminHome.vue')
const AdminProductos = () => import('@/paginas/Admin/Productos.vue')
const AdminBodegas = () => import('@/paginas/Admin/Bodegas.vue')

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL || '/'),
  routes: [
    { path: '/',           name: 'home',       component: Home },
    { path: '/inventario', name: 'inventario', component: Inventario, meta: { requiresAuth: true } },
    { path: '/reportes',   name: 'reportes',   component: Reportes,   meta: { requiresAuth: true } },
    { path: '/login',      name: 'login',      component: Login },
    { path: '/register',   name: 'register',   component: Register },
    { path: '/privado',    name: 'privado',    component: Privado,    meta: { requiresAuth: true } },
    { path: '/carrito',    name: 'carrito',    component: Carrito },
    { path: '/acerca',     name: 'acerca',     component: Acerca },

    // 🧩 Rutas del panel de administración
    {
      path: '/admin',
      name: 'admin-home',
      component: AdminHome,
      meta: { requiresAuth: true, isAdmin: true }
    },
    {
      path: '/admin/productos',
      name: 'admin-productos',
      component: AdminProductos,
      meta: { requiresAuth: true, isAdmin: true }
    },
    {
      path: '/admin/bodegas',
      name: 'admin-bodegas',
      component: AdminBodegas,
      meta: { requiresAuth: true, isAdmin: true }
    },

    // Ruta por defecto
    { path: '/:pathMatch(.*)*', redirect: '/' },
  ],
})

// ✅ Middleware de autenticación
router.beforeEach((to) => {
  // si no requiere autenticación → continuar
  if (!to.meta?.requiresAuth) return true

  try {
    const auth = useAuth()
    // si está autenticado, continuar
    if (auth?.isAuth) {
      // opcional: si es ruta admin, verificar rol
      if (to.meta.isAdmin && !auth.user?.is_admin) {
        return { name: 'home' } // o redirige a una página “no autorizado”
      }
      return true
    }
  } catch (_) {}

  // fallback: sin token → redirigir a login
  const isAuth = !!localStorage.getItem('access_token')
  if (!isAuth) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }

  return true
})

export default router
