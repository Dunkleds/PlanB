<template>
  <div class="home min-h-screen bg-slate-900 text-white">
    <main class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
      <header class="flex flex-col gap-2 sm:flex-row sm:items-baseline sm:justify-between">
        <div>
          <h2 class="text-3xl font-semibold tracking-tight">Catálogo de productos</h2>
          <p class="mt-1 text-slate-300">Descubre la selección de iEssence y agrégala a tu carrito.</p>
        </div>
        <button
          v-if="isAuth && !isLoaded"
          @click="reloadCart"
          class="inline-flex items-center gap-2 px-4 py-2 rounded-xl border border-white/20 hover:bg-white/10 focus:outline-none focus:ring-2 focus:ring-white/40 text-sm"
        >
          <span>Cargar carrito</span>
        </button>
      </header>

      <section class="mt-8">
        <div v-if="loadingCatalog" class="rounded-2xl border border-white/10 bg-slate-900/60 backdrop-blur p-8 text-center">
          <p class="text-slate-300">Cargando productos…</p>
        </div>

        <div
          v-else-if="catalogError"
          class="rounded-2xl border border-red-500/30 bg-red-500/10 p-6 text-center text-sm text-red-200"
        >
          {{ catalogError }}
        </div>

        <div v-else>
          <div
            v-if="cartError"
            class="mb-6 rounded-2xl border border-amber-500/40 bg-amber-500/15 px-4 py-3 text-sm text-amber-200"
          >
            {{ cartError }}
          </div>

          <p v-if="products.length === 0" class="text-slate-300">No hay productos disponibles por ahora.</p>

          <div
            v-else
            class="grid gap-6 sm:grid-cols-2 xl:grid-cols-3"
          >
            <article
              v-for="product in products"
              :key="product.id"
              class="rounded-2xl border border-white/10 bg-slate-900/60 backdrop-blur shadow-xl overflow-hidden flex flex-col"
            >
              <div class="relative h-48 bg-slate-800">
                <img
                  v-if="product.imagen_url"
                  :src="product.imagen_url"
                  :alt="product.nombre_producto"
                  class="h-full w-full object-cover"
                />
                <div v-else class="flex h-full w-full items-center justify-center text-slate-400">
                  <span class="text-sm">Sin imagen</span>
                </div>
                <span class="absolute top-3 left-3 rounded-full bg-fuchsia-500/80 px-3 py-1 text-xs uppercase tracking-wide">
                  {{ product.marca }}
                </span>
              </div>

              <div class="flex flex-1 flex-col gap-4 p-5">
                <header class="space-y-1">
                  <h3 class="text-xl font-semibold">{{ product.nombre_producto }}</h3>
                  <p class="text-sm text-slate-300 line-clamp-3">{{ product.descripcion }}</p>
                </header>

                <footer class="mt-auto flex flex-col gap-4">
                  <div class="flex items-center justify-between">
                    <div>
                      <p class="text-sm text-slate-400">Disponible: {{ product.cantidad }}</p>
                      <p class="text-lg font-semibold">{{ formatPrice(product.precio) }}</p>
                    </div>
                    <RouterLink
                      :to="{ name: 'product-detail', params: { id: product.id } }"
                      class="text-sm text-fuchsia-300 hover:text-fuchsia-200"
                    >
                      Ver detalle
                    </RouterLink>
                  </div>
                  <div class="flex flex-wrap items-center justify-end gap-3" :class="{ 'justify-between': isSelecting(product.id) }">
                    <div
                      v-if="isSelecting(product.id)"
                      class="inline-flex items-center gap-2 rounded-xl border border-white/15 bg-white/5 px-3 py-2 text-sm"
                    >
                      <button
                        type="button"
                        class="rounded-full bg-white/10 px-2 py-1 text-lg leading-none text-white transition hover:bg-white/20"
                        @click="decrementQuantity(product.id)"
                      >
                        −
                      </button>
                      <span class="min-w-[2ch] text-center font-semibold">{{ getDraftQuantity(product.id) }}</span>
                      <button
                        type="button"
                        class="rounded-full bg-white/10 px-2 py-1 text-lg leading-none text-white transition hover:bg-white/20"
                        @click="incrementQuantity(product.id, product.cantidad)"
                      >
                        +
                      </button>
                    </div>

                    <button
                      v-if="isSelecting(product.id)"
                      class="inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-fuchsia-500 to-indigo-500 px-4 py-2 text-sm font-medium hover:opacity-95 focus:outline-none focus:ring-2 focus:ring-white/40 disabled:opacity-60"
                      :disabled="pending(product.id) || cartLoading || product.cantidad <= 0"
                      @click="confirmAdd(product)"
                    >
                      <svg v-if="pending(product.id)" class="h-4 w-4 animate-spin" viewBox="0 0 24 24" fill="none">
                        <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-opacity="0.25" stroke-width="4" />
                        <path d="M22 12a10 10 0 0 1-10 10" stroke="currentColor" stroke-width="4" />
                      </svg>
                      <span v-else>Confirmar</span>
                      <span class="sr-only">Confirmar {{ product.nombre_producto }}</span>
                    </button>

                    <button
                      v-if="isSelecting(product.id)"
                      type="button"
                      class="inline-flex items-center gap-2 rounded-xl border border-white/20 px-4 py-2 text-sm font-medium text-slate-200 transition hover:bg-white/10 focus:outline-none focus:ring-2 focus:ring-white/40"
                      :disabled="pending(product.id) || cartLoading"
                      @click="cancelSelection(product.id)"
                    >
                      Cancelar
                    </button>

                    <button
                      v-else
                      class="inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-fuchsia-500 to-indigo-500 px-4 py-2 text-sm font-medium hover:opacity-95 focus:outline-none focus:ring-2 focus:ring-white/40 disabled:opacity-60"
                      :disabled="pending(product.id) || cartLoading || product.cantidad <= 0"
                      @click="openQuantitySelector(product.id, product.cantidad)"
                    >
                      <span>Agregar</span>
                      <span class="sr-only">{{ product.nombre_producto }}</span>
                    </button>
                  </div>
                </footer>
              </div>
            </article>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
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

const products = ref<Product[]>([])
const loadingCatalog = ref(false)
const catalogError = ref<string | null>(null)
const pendingIds = ref(new Set<string>())

const auth = useAuth()
const cart = useCart()
const { isAuth } = storeToRefs(auth)
const { loading: cartLoading, isLoaded, error: cartError } = storeToRefs(cart)
const router = useRouter()
const route = useRoute()

const quantityDrafts = ref<Record<string, number>>({})

const idKey = (value: Product['id']) => String(value)

const pending = (id: Product['id']) => pendingIds.value.has(idKey(id))

const getDraftQuantity = (productId: Product['id']) => {
  const key = idKey(productId)
  return quantityDrafts.value[key] ?? 1
}

const isSelecting = (productId: Product['id']) => {
  const key = idKey(productId)
  return Object.prototype.hasOwnProperty.call(quantityDrafts.value, key)
}

const openQuantitySelector = (productId: Product['id'], available: number) => {
  if (available <= 0) return
  const key = idKey(productId)
  quantityDrafts.value = {
    ...quantityDrafts.value,
    [key]: Math.min(quantityDrafts.value[key] ?? 1, available),
  }
}

const cancelSelection = (productId: Product['id']) => {
  if (!isSelecting(productId)) return
  const key = idKey(productId)
  const { [key]: _removed, ...rest } = quantityDrafts.value
  quantityDrafts.value = rest
}

const setDraftQuantity = (productId: Product['id'], quantity: number, available: number) => {
  if (available <= 0) return
  const safeQuantity = Math.max(1, Math.min(quantity, available))
  const key = idKey(productId)
  quantityDrafts.value = {
    ...quantityDrafts.value,
    [key]: safeQuantity,
  }
}

const incrementQuantity = (productId: Product['id'], available: number) => {
  const current = getDraftQuantity(productId)
  setDraftQuantity(productId, current + 1, available)
}

const decrementQuantity = (productId: Product['id']) => {
  const current = getDraftQuantity(productId)
  if (current <= 1) return
  const key = idKey(productId)
  quantityDrafts.value = {
    ...quantityDrafts.value,
    [key]: current - 1,
  }
}

const formatPrice = (value: string | number) => {
  const amount = typeof value === 'number' ? value : Number(value)
  return new Intl.NumberFormat('es-CL', { style: 'currency', currency: 'CLP', maximumFractionDigits: 0 }).format(amount)
}

const fetchProducts = async () => {
  loadingCatalog.value = true
  catalogError.value = null
  try {
    const { data } = await api.get<Product[]>('/api/products/')
    products.value = data
  } catch (error: any) {
    catalogError.value = error?.response?.data?.detail ?? 'No se pudo cargar el catálogo'
  } finally {
    loadingCatalog.value = false
  }
}

const addProductToCart = async (productId: Product['id'], quantity = 1) => {
  if (!isAuth.value) {
    router.push({ name: 'login', query: { redirect: route.fullPath } })
    return false
  }

  const key = idKey(productId)
  const next = new Set(pendingIds.value)
  next.add(key)
  pendingIds.value = next

  let wasSuccessful = false
  try {
    await cart.addToCart(productId, quantity)
    wasSuccessful = true
  } catch (_error) {
    // El store expone el mensaje de error; no hacemos nada extra aquí.
  } finally {
    const updated = new Set(pendingIds.value)
    updated.delete(key)
    pendingIds.value = updated
  }

  return wasSuccessful
}

const confirmAdd = async (product: Product) => {
  const quantity = getDraftQuantity(product.id)
  const success = await addProductToCart(product.id, quantity)
  if (success) {
    cancelSelection(product.id)
  }
}

const reloadCart = async () => {
  if (isAuth.value) {
    await cart.fetchCart()
  }
}

onMounted(() => {
  fetchProducts()
  if (isAuth.value && !isLoaded.value) {
    cart.fetchCart()
  }
})

</script>
