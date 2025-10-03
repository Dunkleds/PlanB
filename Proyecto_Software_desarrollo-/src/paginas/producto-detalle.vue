<template>
  <div class="min-h-screen bg-slate-900 text-white">
    <main class="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8 py-12">
      <div class="mb-6 flex items-center justify-between gap-4">
        <RouterLink
          :to="{ name: 'home' }"
          class="inline-flex items-center gap-2 text-sm text-slate-300 transition hover:text-white"
        >
          <span aria-hidden="true">←</span>
          <span>Volver al catálogo</span>
        </RouterLink>
        <button
          v-if="product"
          type="button"
          class="text-sm text-fuchsia-300 transition hover:text-fuchsia-200"
          @click="reloadProduct()"
        >
          Recargar
        </button>
      </div>

      <section v-if="loading" class="rounded-2xl border border-white/10 bg-slate-900/60 p-10 text-center">
        <p class="text-slate-300">Cargando producto…</p>
      </section>

      <section v-else-if="error" class="rounded-2xl border border-red-500/30 bg-red-500/10 p-10 text-center text-sm text-red-200">
        {{ error }}
      </section>

      <section v-else-if="product" class="grid gap-10 lg:grid-cols-[1.2fr,1fr]">
        <div class="flex flex-col gap-6">
          <div class="overflow-hidden rounded-3xl border border-white/10 bg-slate-900/60">
            <img
              v-if="product.imagen_url"
              :src="product.imagen_url"
              :alt="product.nombre_producto"
              class="h-full w-full object-cover"
            />
            <div v-else class="flex h-80 items-center justify-center text-slate-400">
              <span class="text-sm">Sin imagen disponible</span>
            </div>
          </div>

          <div class="rounded-3xl border border-white/10 bg-slate-900/60 p-6">
            <h1 class="text-3xl font-semibold">{{ product.nombre_producto }}</h1>
            <p class="mt-2 text-sm uppercase tracking-widest text-fuchsia-300/80">{{ product.marca }}</p>
            <p class="mt-6 text-base leading-relaxed text-slate-200">{{ product.descripcion }}</p>
          </div>
        </div>

        <aside class="flex flex-col gap-6">
          <div class="rounded-3xl border border-white/10 bg-slate-900/60 p-6">
            <p class="text-sm text-slate-400">Precio</p>
            <p class="text-3xl font-semibold">{{ formatPrice(product.precio) }}</p>
            <p class="mt-4 text-sm text-slate-400">Existencias: {{ product.cantidad }}</p>
          </div>

          <div class="rounded-3xl border border-white/10 bg-slate-900/60 p-6">
            <h2 class="text-lg font-semibold">Añadir al carrito</h2>
            <p v-if="cartError" class="mt-3 rounded-xl border border-amber-500/40 bg-amber-500/15 px-4 py-3 text-xs text-amber-200">
              {{ cartError }}
            </p>

            <div class="mt-6 flex flex-col gap-4">
              <div class="flex items-center gap-4">
                <span class="text-sm text-slate-300">Cantidad</span>
                <div class="inline-flex items-center gap-3 rounded-xl border border-white/15 bg-white/5 px-4 py-2 text-sm">
                  <button
                    type="button"
                    class="rounded-full bg-white/10 px-2 py-1 text-lg leading-none text-white transition hover:bg-white/20 disabled:opacity-40"
                    :disabled="quantity <= 1"
                    @click="decrementQuantity"
                  >
                    −
                  </button>
                  <span class="min-w-[2ch] text-center font-semibold">{{ quantity }}</span>
                  <button
                    type="button"
                    class="rounded-full bg-white/10 px-2 py-1 text-lg leading-none text-white transition hover:bg-white/20 disabled:opacity-40"
                    :disabled="product.cantidad === 0 || quantity >= product.cantidad"
                    @click="incrementQuantity"
                  >
                    +
                  </button>
                </div>
              </div>

              <button
                class="inline-flex items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-fuchsia-500 to-indigo-500 px-5 py-3 text-sm font-medium hover:opacity-95 focus:outline-none focus:ring-2 focus:ring-white/40 disabled:opacity-60"
                :disabled="cartLoading || product.cantidad === 0"
                @click="addToCart(product.id)"
              >
                <svg v-if="pending" class="h-4 w-4 animate-spin" viewBox="0 0 24 24" fill="none">
                  <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-opacity="0.25" stroke-width="4" />
                  <path d="M22 12a10 10 0 0 1-10 10" stroke="currentColor" stroke-width="4" />
                </svg>
                <span v-else>Agregar al carrito</span>
              </button>
            </div>
          </div>
        </aside>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { api } from '@/lib/api'
import { useAuth } from '@/services/auth'
import { useCart } from '@/stores/cart'

interface Product {
  id: number | string
  nombre_producto: string
  cantidad: number
  precio: string | number
  marca: string
  descripcion: string
  imagen_url: string | null
}

const route = useRoute()
const router = useRouter()
const auth = useAuth()
const cart = useCart()
const { isAuth } = storeToRefs(auth)
const { loading: cartLoading, error: cartError } = storeToRefs(cart)

const product = ref<Product | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)
const pending = ref(false)
const quantity = ref(1)

const formatPrice = (value: string | number) => {
  const amount = typeof value === 'number' ? value : Number(value)
  return new Intl.NumberFormat('es-CL', { style: 'currency', currency: 'CLP', maximumFractionDigits: 0 }).format(amount)
}

const resolveRouteId = (): string | null => {
  const param = route.params.id
  if (Array.isArray(param)) {
    const first = param[0]
    return first != null ? String(first) : null
  }
  if (param == null) return null
  const value = typeof param === 'string' ? param : String(param)
  const trimmed = value.trim()
  return trimmed.length ? trimmed : null
}

const fetchProduct = async () => {
  const rawId = resolveRouteId()
  if (!rawId) {
    error.value = 'Producto no encontrado'
    product.value = null
    quantity.value = 0
    loading.value = false
    return
  }

  loading.value = true
  error.value = null
  cart.error = null

  const encodedId = encodeURIComponent(rawId)
  const endpoints = [`/api/products/${encodedId}/`, `/api/products/${encodedId}`]

  let lastError: any = null

  for (const url of endpoints) {
    try {
      const { data } = await api.get<Product>(url)
      product.value = data
      quantity.value = data.cantidad > 0 ? 1 : 0
      error.value = null
      loading.value = false
      return
    } catch (err: any) {
      lastError = err
      if (err?.response?.status === 404) {
        continue
      }
      break
    }
  }

  if (lastError?.response?.status === 404) {
    error.value = 'Producto no encontrado'
  } else {
    error.value = 'No se pudo cargar el producto'
  }
  product.value = null
  quantity.value = 0
  loading.value = false
}

const addToCart = async (productId: Product['id']) => {
  if (!isAuth.value) {
    router.push({ name: 'login', query: { redirect: route.fullPath } })
    return
  }

  pending.value = true
  cart.error = null

  try {
    if (!product.value) return
    const available = product.value.cantidad
    if (available <= 0) {
      return
    }
    const desired = Math.min(Math.max(quantity.value, 1), available || 1)
    await cart.addToCart(productId, desired)
  } finally {
    pending.value = false
  }
}

const reloadProduct = () => {
  if (!loading.value) {
    fetchProduct()
  }
}

const incrementQuantity = () => {
  if (!product.value) return
  if (product.value.cantidad <= 0) return
  quantity.value = Math.min(product.value.cantidad, quantity.value + 1)
}

const decrementQuantity = () => {
  if (quantity.value <= 1) return
  quantity.value = Math.max(1, quantity.value - 1)
}

onMounted(fetchProduct)

watch(
  () => route.params.id,
  () => {
    fetchProduct()
  },
)
</script>
