// src/lib/api.ts
import axios from 'axios'

const BASE = (import.meta.env.VITE_API_URL as string || '').replace(/\/+$/, '')

export const api = axios.create({
  baseURL: BASE,
  headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
})

// === Helpers de tokens en localStorage ===
const ACCESS_KEY = 'access_token'
const REFRESH_KEY = 'refresh_token'

export function setTokens(access: string, refresh: string) {
  localStorage.setItem(ACCESS_KEY, access)
  localStorage.setItem(REFRESH_KEY, refresh)
}
export function clearTokens() {
  localStorage.removeItem(ACCESS_KEY)
  localStorage.removeItem(REFRESH_KEY)
}
export function getAccess() { return localStorage.getItem(ACCESS_KEY) || '' }
export function getRefresh() { return localStorage.getItem(REFRESH_KEY) || '' }

// === Interceptor: Authorization + refresh en 401 ===
api.interceptors.request.use(cfg => {
  const t = getAccess()
  if (t) cfg.headers.Authorization = `Bearer ${t}`
  return cfg
})

let isRefreshing = false
let queue: Array<() => void> = []
api.interceptors.response.use(
  r => r,
  async (err) => {
    const original: any = err.config
    if (err.response?.status === 401 && !original._retry) {
      if (isRefreshing) {
        await new Promise<void>(res => queue.push(res))
        original.headers.Authorization = `Bearer ${getAccess()}`
        return api(original)
      }
      original._retry = true
      isRefreshing = true
      try {
        const rt = getRefresh()
        if (!rt) throw new Error('No refresh token')
        const { data } = await axios.post(`${BASE}/api/token/refresh/`, { refresh: rt })
        setTokens(data.access, rt)
        original.headers.Authorization = `Bearer ${data.access}`
        queue.forEach(fn => fn()); queue = []
        return api(original)
      } finally {
        isRefreshing = false
      }
    }
    throw err
  }
)

// === Login "rápido" para SimpleJWT (username = parte antes del @) ===
export async function loginWithEmailQuick(email: string, password: string) {
  const username = email.split('@')[0]
  const { data } = await api.post('/api/token/', { username, password })
  setTokens(data.access, data.refresh)
  return data
}

// === Logout ===
export function logout() { clearTokens() }
