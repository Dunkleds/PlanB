import { defineStore } from 'pinia'
import { api, loginWithEmailQuick, logout } from '@/lib/api'

export function registerUser(email: string, password: string): Promise<any> {

  return api.post('/api/register/', { email, password })
}

interface AuthState {
  email: string
  isAuth: boolean
}

export const useAuth = defineStore('auth', {
  state: (): AuthState => ({
    email: '',
    isAuth: !!localStorage.getItem('access_token'),
  }),
  actions: {
    async login(email: string, password: string): Promise<void> {
      await loginWithEmailQuick(email, password)
      this.email = email
      this.isAuth = true
    },
    signout(): void {
      logout()
      this.email = ''
      this.isAuth = false
    },
  },
})
