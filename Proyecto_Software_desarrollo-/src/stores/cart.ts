import { defineStore } from 'pinia'
import { api } from '@/lib/api'

export interface CartProduct {
  id: number
  nombre_producto: string
  cantidad: number
  precio: string
  marca: string
  descripcion: string
  imagen_url: string | null
}

export interface CartItem {
  id: number
  product: CartProduct
  quantity: number
  line_total: string
}

interface CartSummaryPayload {
  total_quantity?: number
  total_amount?: string
}

interface CartResponse {
  items?: CartItem[]
  summary?: CartSummaryPayload
}

interface CartSummary {
  totalQuantity: number
  totalAmount: number
}

interface CartState {
  items: CartItem[]
  summary: CartSummary
  loading: boolean
  error: string | null
  isLoaded: boolean
}

function parseSummary(summary?: CartSummaryPayload): CartSummary {
  const totalQuantity = summary?.total_quantity ?? 0
  const totalAmount = summary?.total_amount ? Number(summary.total_amount) : 0
  return {
    totalQuantity,
    totalAmount,
  }
}

export const useCart = defineStore('cart', {
  state: (): CartState => ({
    items: [],
    summary: { totalQuantity: 0, totalAmount: 0 },
    loading: false,
    error: null,
    isLoaded: false,
  }),

  getters: {
    totalCount: (state) => state.summary.totalQuantity,
    totalAmount: (state) => state.summary.totalAmount,
  },

  actions: {
    applyPayload(payload: CartResponse) {
      this.items = Array.isArray(payload.items) ? payload.items : []
      this.summary = parseSummary(payload.summary)
      this.isLoaded = true
    },

    reset() {
      this.items = []
      this.summary = { totalQuantity: 0, totalAmount: 0 }
      this.loading = false
      this.error = null
      this.isLoaded = false
    },

    async fetchCart() {
      this.loading = true
      this.error = null
      try {
        const { data } = await api.get<CartResponse>('/api/cart/')
        this.applyPayload(data)
      } catch (error: any) {
        if (error?.response?.status === 401) {
          this.reset()
          return
        }
        this.error = error?.response?.data?.detail ?? 'No se pudo cargar el carrito'
      } finally {
        this.loading = false
      }
    },

    async addToCart(productId: number, quantity = 1) {
      this.error = null
      try {
        const { data } = await api.post<CartResponse>('/api/cart/', {
          product_id: productId,
          quantity,
        })
        this.applyPayload(data)
      } catch (error: any) {
        this.error = error?.response?.data?.detail ?? 'No se pudo agregar al carrito'
        throw error
      }
    },

    async updateQuantity(productId: number, quantity: number) {
      if (quantity < 0) quantity = 0
      try {
        const { data } = await api.patch<CartResponse>(`/api/cart/${productId}/`, { quantity })
        this.applyPayload(data)
      } catch (error: any) {
        this.error = error?.response?.data?.detail ?? 'No se pudo actualizar la cantidad'
        throw error
      }
    },

    async removeItem(productId: number) {
      try {
        const { data } = await api.delete<CartResponse>(`/api/cart/${productId}/`)
        this.applyPayload(data)
      } catch (error: any) {
        this.error = error?.response?.data?.detail ?? 'No se pudo eliminar el producto'
        throw error
      }
    },
  },
})

export type CartStore = ReturnType<typeof useCart>
