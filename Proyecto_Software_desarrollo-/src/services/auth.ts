import { defineStore } from 'pinia'
import { api, loginWithEmailQuick, logout, getMe, updateUsername } from '@/lib/api'
import { useCart } from '@/stores/cart'

export function registerUser(email: string, password: string): Promise<any> {
  return api.post('/api/register/', { email, password }) // backend mapea a users.register
}

interface UserInfo {
  id: number | null
  email: string | null
  username: string | null
}

interface AuthState {
  isAuth: boolean
  user: UserInfo
  loading: boolean
  error: string | null
}

export const useAuth = defineStore('auth', {
  state: (): AuthState => ({
    isAuth: !!localStorage.getItem('access_token'),
    user: { id: null, email: null, username: null },
    loading: false,
    error: null,
  }),

  actions: {
    async login(email: string, password: string): Promise<void> {
      this.loading = true
      this.error = null
      try {
        await loginWithEmailQuick(email, password)
        this.isAuth = true
        await this.fetchMe()
        const cart = useCart()
        await cart.fetchCart()
      } catch (e: any) {
        this.error = e?.response?.data?.detail ?? 'No se pudo iniciar sesión'
        this.isAuth = false
        throw e
      } finally {
        this.loading = false
      }
    },

    async register(email: string, password: string): Promise<void> {
      this.loading = true
      this.error = null
      try {
        await registerUser(email, password)
        // Autologin
        await this.login(email, password)
      } catch (e: any) {
        this.error = e?.response?.data?.detail ?? 'No se pudo registrar'
        throw e
      } finally {
        this.loading = false
      }
    },

    async fetchMe(): Promise<void> {
      if (!this.isAuth) return
      try {
        const data = await getMe()
        this.user = { id: data.id, email: data.email, username: data.username }
      } catch {
        // token inválido => cerrar sesión
        this.signout()
      }
    },

    async changeUsername(newUsername: string): Promise<void> {
      this.loading = true
      this.error = null
      try {
        const data = await updateUsername(newUsername)
        this.user.username = data.username
      } catch (e: any) {
        this.error = e?.response?.data?.username?.[0] ?? e?.response?.data?.detail ?? 'No se pudo actualizar el username'
        throw e
      } finally {
        this.loading = false
      }
    },

    signout(): void {
      logout()
      this.isAuth = false
      this.user = { id: null, email: null, username: null }
      this.error = null
      this.loading = false
      const cart = useCart()
      cart.reset()
    },
  },
})
