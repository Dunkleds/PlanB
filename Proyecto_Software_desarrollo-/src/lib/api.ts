import axios, { AxiosError, AxiosRequestConfig } from 'axios'

const rawBaseURL = (import.meta.env.VITE_API_URL as string | undefined) ?? ''
const baseURL = rawBaseURL.replace(/\/+$/, '')

const ACCESS_KEY = 'access_token'
const REFRESH_KEY = 'refresh_token'

const TOKEN_URL = '/api/token/'            // TODO adjust if backend differs
const REFRESH_URL = '/api/token/refresh/'  // TODO adjust if backend differs

// Reminder: backend CORS must allow these origins when deploying on Netlify.
// https://<SITE>.netlify.app
// https://deploy-preview-*.netlify.app

export const api = axios.create({
  baseURL: baseURL || undefined,
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json',
  },
})

type QueueEntry = {
  onSuccess: (token: string) => void
  onError: (error: unknown) => void
}

let isRefreshing = false
let refreshQueue: QueueEntry[] = []

function setAuthHeader(config: AxiosRequestConfig, token: string) {
  if (!token) return

  if (!config.headers) {
    config.headers = { Authorization: `Bearer ${token}` }
    return
  }

  const headers = config.headers as Record<string, unknown> & { set?: (name: string, value: string) => void }
  if (typeof headers.set === 'function') {
    headers.set('Authorization', `Bearer ${token}`)
  } else {
    headers.Authorization = `Bearer ${token}`
  }
}

function drainQueue(error?: unknown, token?: string) {
  refreshQueue.forEach(({ onSuccess, onError }) => {
    if (error || !token) {
      onError(error ?? new Error('Token refresh failed'))
      return
    }
    onSuccess(token)
  })
  refreshQueue = []
}

export function setTokens(access?: string | null, refresh?: string | null) {
  if (access) {
    localStorage.setItem(ACCESS_KEY, access)
  } else {
    localStorage.removeItem(ACCESS_KEY)
  }

  if (refresh) {
    localStorage.setItem(REFRESH_KEY, refresh)
  } else {
    localStorage.removeItem(REFRESH_KEY)
  }
}

export function getAccessToken(): string | null {
  return localStorage.getItem(ACCESS_KEY)
}

export function getRefreshToken(): string | null {
  return localStorage.getItem(REFRESH_KEY)
}

export function clearTokens(): void {
  localStorage.removeItem(ACCESS_KEY)
  localStorage.removeItem(REFRESH_KEY)
}

type RetriableConfig = AxiosRequestConfig & { _retry?: boolean }

api.interceptors.request.use((config) => {
  const access = getAccessToken()
  if (access) {
    setAuthHeader(config, access)
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = (error.config || {}) as RetriableConfig

    if (error.response?.status !== 401 || originalRequest._retry) {
      throw error
    }

    const refreshToken = getRefreshToken()
    if (!refreshToken) {
      clearTokens()
      redirectToLogin()
      throw error
    }

    if (isRefreshing) {
      return new Promise((resolve, reject) => {
        refreshQueue.push({
          onSuccess: (token) => {
            setAuthHeader(originalRequest, token)
            resolve(api(originalRequest))
          },
          onError: reject,
        })
      })
    }

    originalRequest._retry = true
    isRefreshing = true

    try {
      const { data } = await axios.post(
        `${baseURL}${REFRESH_URL}`,
        { refresh: refreshToken },
        { headers: { Accept: 'application/json', 'Content-Type': 'application/json' } },
      )

      const newAccess: string | undefined = data?.access
      const newRefresh: string | undefined = data?.refresh ?? refreshToken

      if (!newAccess) {
        throw new Error('Refresh endpoint did not return access token')
      }

      setTokens(newAccess, newRefresh)
      drainQueue(undefined, newAccess)
      setAuthHeader(originalRequest, newAccess)
      return api(originalRequest)
    } catch (refreshError) {
      drainQueue(refreshError)
      clearTokens()
      redirectToLogin()
      throw refreshError
    } finally {
      isRefreshing = false
    }
  },
)

function redirectToLogin() {
  if (typeof window === 'undefined') return
  const { pathname, search, hash } = window.location
  if (pathname === '/login') return
  const redirectPath = `${pathname}${search}${hash}` || '/'
  const target = `/login?redirect=${encodeURIComponent(redirectPath)}`
  window.location.replace(target)
}

export async function loginWithEmailQuick(email: string, password: string) {
  const { data } = await api.post(TOKEN_URL, { email, password })
  if (data?.access) {
    setTokens(data.access, data?.refresh)
    api.defaults.headers.Authorization = `Bearer ${data.access}`
  }
  return data
}

export function logout(): void {
  clearTokens()
}

export interface ProfileResponse {
  id: number
  email: string
  username: string
  first_name: string
  last_name: string
  message?: string
}

export async function getMe() {
  const { data } = await api.get('/api/auth/me/')
  return data as ProfileResponse
}

export async function updateProfileNames(first_name: string, last_name: string) {
  const { data } = await api.patch('/api/auth/me/', { first_name, last_name })
  return data as ProfileResponse
}
