import { defineStore } from 'pinia'
import { api, loginWithEmailQuick, logout, getMe, updateProfileNames } from '@/lib/api'
import { useCart } from '@/stores/cart'

export interface RegisterPayload {
  email: string
  password: string
  first_name?: string
  last_name?: string
}

export function registerUser(payload: RegisterPayload): Promise<any> {
  return api.post('/api/register/', payload) // backend mapea a users.register
}

interface UserInfo {
  id: number | null
  email: string | null
  username: string | null
  first_name: string | null
  last_name: string | null
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
    user: { id: null, email: null, username: null, first_name: null, last_name: null },
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

    async register(email: string, password: string, firstName?: string, lastName?: string): Promise<void> {
      this.loading = true
      this.error = null
      try {
        await registerUser({ email, password, first_name: firstName, last_name: lastName })
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
        this.user = {
          id: data.id,
          email: data.email,
          username: data.username,
          first_name: data.first_name,
          last_name: data.last_name,
        }
      } catch {
        // token inválido => cerrar sesión
        this.signout()
      }
    },

    async updateNames(firstName: string, lastName: string): Promise<void> {
      this.loading = true
      this.error = null
      try {
        const data = await updateProfileNames(firstName, lastName)
        this.user.first_name = data.first_name
        this.user.last_name = data.last_name
        this.user.username = data.username
      } catch (e: any) {
        this.error =
          e?.response?.data?.first_name?.[0] ??
          e?.response?.data?.last_name?.[0] ??
          e?.response?.data?.detail ??
          'No se pudo actualizar el perfil'
        throw e
      } finally {
        this.loading = false
      }
    },

    signout(): void {
      logout()
      this.isAuth = false
      this.user = { id: null, email: null, username: null, first_name: null, last_name: null }
      this.error = null
      this.loading = false
      const cart = useCart()
      cart.reset()
    },
  },
})
