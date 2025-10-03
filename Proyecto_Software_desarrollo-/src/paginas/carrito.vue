<template>
  <div class="min-h-screen bg-slate-900 text-white">
    <main class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
      <header class="flex flex-col gap-2 sm:flex-row sm:items-baseline sm:justify-between">
        <div>
          <h2 class="text-3xl font-semibold tracking-tight">Tu carrito</h2>
          <p class="mt-1 text-slate-300">Revisa los productos agregados y ajusta sus cantidades.</p>
        </div>
        <router-link
          to="/"
          class="inline-flex items-center gap-2 rounded-xl border border-white/20 px-4 py-2 text-sm hover:bg-white/10 focus:outline-none focus:ring-2 focus:ring-white/40"
        >
          Seguir comprando
        </router-link>
      </header>

      <section class="mt-8">
        <div
          v-if="cartLoading && !isLoaded"
          class="rounded-2xl border border-white/10 bg-slate-900/60 backdrop-blur p-8 text-center"
        >
          <p class="text-slate-300">Cargando tu carrito…</p>
        </div>

        <div v-else>
          <div
            v-if="errorMessage"
            class="mb-6 rounded-2xl border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-200"
          >
            {{ errorMessage }}
          </div>

          <div v-if="!hasItems" class="rounded-2xl border border-white/10 bg-slate-900/60 backdrop-blur p-10 text-center">
            <p class="text-lg text-slate-200">Tu carrito está vacío.</p>
            <p class="mt-2 text-sm text-slate-400">Explora nuestro catálogo y agrega productos para verlos aquí.</p>
            <router-link
              to="/"
              class="mt-5 inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-fuchsia-500 to-indigo-500 px-5 py-2.5 text-sm font-medium hover:opacity-95 focus:outline-none focus:ring-2 focus:ring-white/40"
            >
              Ir al catálogo
            </router-link>
          </div>

          <div v-else class="grid gap-6 lg:grid-cols-[2fr_1fr]">
            <section class="rounded-2xl border border-white/10 bg-slate-900/60 backdrop-blur shadow-xl divide-y divide-white/10">
              <article
                v-for="item in items"
                :key="item.id"
                class="flex flex-col gap-4 p-5 sm:flex-row sm:items-center"
              >
                <img
                  :src="item.product.imagen_url || fallbackImage"
                  :alt="item.product.nombre_producto"
                  class="h-24 w-24 rounded-xl object-cover"
                />

                <div class="flex flex-1 flex-col gap-2">
                  <header>
                    <h3 class="text-lg font-semibold">{{ item.product.nombre_producto }}</h3>
                    <p class="text-sm text-slate-300">Marca: {{ item.product.marca }}</p>
                  </header>

                  <p class="text-sm text-slate-400 line-clamp-2">{{ item.product.descripcion }}</p>

                  <div class="mt-auto flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                    <div class="space-y-1">
                      <p class="text-sm text-slate-400">Precio unidad</p>
                      <p class="text-lg font-semibold">{{ formatCLP(item.product.precio) }}</p>
                    </div>
                    <div class="flex items-center gap-2">
                      <button
                        class="h-8 w-8 rounded-full border border-white/20 text-lg hover:bg-white/10 focus:outline-none focus:ring-2 focus:ring-white/40 disabled:opacity-60"
                        :disabled="itemPending(item.product.id) || cartLoading"
                        @click="changeQuantity(item.product.id, item.quantity - 1)"
                      >
                        −
                      </button>
                      <span class="min-w-[3rem] text-center text-lg font-semibold">{{ item.quantity }}</span>
                      <button
                        class="h-8 w-8 rounded-full border border-white/20 text-lg hover:bg-white/10 focus:outline-none focus:ring-2 focus:ring-white/40 disabled:opacity-60"
                        :disabled="itemPending(item.product.id) || cartLoading"
                        @click="changeQuantity(item.product.id, item.quantity + 1)"
                      >
                        +
                      </button>
                    </div>
                    <div class="text-right">
                      <p class="text-sm text-slate-400">Subtotal</p>
                      <p class="text-lg font-semibold">{{ formatCLP(item.line_total) }}</p>
                    </div>
                  </div>
                </div>

                <button
                  class="self-start rounded-xl border border-white/20 px-3 py-2 text-xs uppercase tracking-wide text-slate-300 hover:bg-white/10 focus:outline-none focus:ring-2 focus:ring-white/40 disabled:opacity-60"
                  :disabled="itemPending(item.product.id) || cartLoading"
                  @click="removeItem(item.product.id)"
                >
                  Quitar
                </button>
              </article>
            </section>

            <aside class="rounded-2xl border border-white/10 bg-slate-900/60 backdrop-blur shadow-xl p-6 space-y-4">
              <header class="flex items-center justify-between">
                <span class="text-slate-300">Productos</span>
                <span class="text-lg font-semibold">{{ summary.totalQuantity }}</span>
              </header>
              <div class="flex items-center justify-between">
                <span class="text-slate-300">Total</span>
                <span class="text-2xl font-semibold">{{ totalFormatted }}</span>
              </div>
              <router-link
                to="/pago"
                class="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-fuchsia-500 to-indigo-500 px-5 py-2.5 font-medium hover:opacity-95 focus:outline-none focus:ring-2 focus:ring-white/40"
              >
                Proceder al pago
                <span aria-hidden="true">➤</span>
              </router-link>
            </aside>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useAuth } from '@/services/auth'
import { useCart } from '@/stores/cart'

const auth = useAuth()
const cart = useCart()
const router = useRouter()
const route = useRoute()

const { isAuth } = storeToRefs(auth)
const { items, summary, loading, error, isLoaded } = storeToRefs(cart)

const pendingIds = ref(new Set<string>())
const fallbackImage = 'https://via.placeholder.com/150?text=Producto'

const cartLoading = computed(() => loading.value)
const errorMessage = computed(() => error.value)
const hasItems = computed(() => items.value.length > 0)

const formatCLP = (value: number | string) => {
  const amount = typeof value === 'number' ? value : Number(value)
  return new Intl.NumberFormat('es-CL', { style: 'currency', currency: 'CLP', maximumFractionDigits: 0 }).format(amount)
}

const totalFormatted = computed(() => formatCLP(summary.value.totalAmount))

const idKey = (value: number | string) => String(value)

const itemPending = (id: number | string) => pendingIds.value.has(idKey(id))

const changeQuantity = async (productId: number | string, nextQuantity: number) => {
  if (itemPending(productId)) return
  const key = idKey(productId)
  const updated = new Set(pendingIds.value)
  updated.add(key)
  pendingIds.value = updated
  try {
    await cart.updateQuantity(productId, nextQuantity)
  } finally {
    const cleared = new Set(pendingIds.value)
    cleared.delete(key)
    pendingIds.value = cleared
  }
}

const removeItem = async (productId: number | string) => {
  if (itemPending(productId)) return
  const key = idKey(productId)
  const updated = new Set(pendingIds.value)
  updated.add(key)
  pendingIds.value = updated
  try {
    await cart.removeItem(productId)
  } finally {
    const cleared = new Set(pendingIds.value)
    cleared.delete(key)
    pendingIds.value = cleared
  }
}

onMounted(async () => {
  if (!isAuth.value) {
    router.replace({ name: 'login', query: { redirect: route.fullPath } })
    return
  }
  if (!isLoaded.value) {
    await cart.fetchCart()
  }
})

watch(isAuth, async (loggedIn) => {
  if (loggedIn && !isLoaded.value) {
    await cart.fetchCart()
  } else if (!loggedIn) {
    pendingIds.value = new Set()
  }
})
</script>
