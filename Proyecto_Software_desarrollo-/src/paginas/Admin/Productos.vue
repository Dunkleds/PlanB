<template>
  <div class="min-h-screen bg-slate-950 text-slate-100">
    <main class="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 py-10">
      <header class="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 class="text-3xl font-semibold tracking-tight">Gestión de productos</h1>
          <p class="text-sm text-slate-400">Visualiza y administra el catálogo disponible en la plataforma.</p>
        </div>
        <button
          type="button"
          class="inline-flex items-center gap-2 rounded-xl border border-slate-700 px-4 py-2 text-sm font-medium text-slate-200 transition hover:bg-slate-800"
          :disabled="loading"
          @click="fetchProducts"
        >
          <svg
            v-if="loading"
            class="h-4 w-4 animate-spin"
            viewBox="0 0 24 24"
            fill="none"
            aria-hidden="true"
          >
            <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-opacity="0.25" stroke-width="4" />
            <path d="M22 12a10 10 0 0 1-10 10" stroke="currentColor" stroke-width="4" />
          </svg>
          <span>{{ loading ? 'Actualizando…' : 'Recargar' }}</span>
        </button>
      </header>

      <section class="mt-8 rounded-2xl border border-slate-800 bg-slate-900/70 backdrop-blur">
        <div v-if="loading" class="p-8 text-center text-sm text-slate-400">Cargando productos…</div>

        <div v-else-if="error" class="p-6 text-sm text-red-300">{{ error }}</div>

        <div v-else>
          <div v-if="products.length === 0" class="p-8 text-center text-sm text-slate-400">
            No se encontraron productos registrados.
          </div>
          <div v-else class="overflow-x-auto">
            <table class="min-w-full divide-y divide-slate-800 text-left text-sm">
              <thead class="bg-slate-900/60 text-slate-300">
                <tr>
                  <th scope="col" class="px-6 py-3 font-medium uppercase tracking-wide">ID</th>
                  <th scope="col" class="px-6 py-3 font-medium uppercase tracking-wide">Nombre</th>
                  <th scope="col" class="px-6 py-3 font-medium uppercase tracking-wide">Marca</th>
                  <th scope="col" class="px-6 py-3 font-medium uppercase tracking-wide">Stock</th>
                  <th scope="col" class="px-6 py-3 font-medium uppercase tracking-wide">Precio</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-800">
                <tr v-for="product in products" :key="product.id" class="bg-slate-900/40">
                  <td class="px-6 py-3 text-slate-400">#{{ product.id }}</td>
                  <td class="px-6 py-3 font-medium text-slate-100">{{ product.nombre_producto }}</td>
                  <td class="px-6 py-3 text-slate-300">{{ product.marca }}</td>
                  <td class="px-6 py-3 text-slate-300">{{ product.cantidad }}</td>
                  <td class="px-6 py-3 font-semibold text-slate-100">{{ formatPrice(product.precio) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { api } from '@/lib/api'

interface Product {
  id: number | string
  nombre_producto: string
  marca: string
  cantidad: number
  precio: string | number
}

const products = ref<Product[]>([])
const loading = ref(false)
const error = ref<string | null>(null)

const formatPrice = (value: string | number) => {
  const amount = typeof value === 'number' ? value : Number(value)
  return new Intl.NumberFormat('es-CL', { style: 'currency', currency: 'CLP', maximumFractionDigits: 0 }).format(amount)
}

const fetchProducts = async () => {
  loading.value = true
  error.value = null
  try {
    const { data } = await api.get<Product[]>('/api/products/')
    products.value = data
  } catch (err: any) {
    error.value = err?.response?.data?.detail ?? 'No se pudieron cargar los productos'
  } finally {
    loading.value = false
  }
}

onMounted(fetchProducts)
</script>
