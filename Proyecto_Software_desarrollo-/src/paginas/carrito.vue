<template>
  <div class="min-h-screen bg-slate-900 text-white">
    <main class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
      <h2 class="text-3xl font-semibold tracking-tight">Resumen de Carrito 🛒</h2>

      <!-- Tabla / lista -->
      <section class="mt-6 rounded-2xl border border-white/10 bg-slate-900/60 backdrop-blur shadow-xl overflow-hidden">
        <!-- Desktop table -->
        <div class="hidden md:block overflow-x-auto">
          <table class="min-w-full text-sm">
            <thead class="bg-white/5">
              <tr class="[&>th]:px-4 [&>th]:py-3 [&>th]:text-left [&>th]:font-semibold [&>th]:text-slate-200">
                <th>Imagen</th>
                <th>ID</th>
                <th>Producto</th>
                <th>Precio</th>
                <th>Cantidad</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-white/10">
              <tr v-for="(item, idx) in carrito" :key="idx" class="hover:bg-white/5">
                <td class="px-4 py-3">
                  <img :src="item.imagen" :alt="item.nombre" class="h-12 w-12 object-cover rounded-md" />
                </td>
                <td class="px-4 py-3 text-slate-300">{{ item.id }}</td>
                <td class="px-4 py-3">{{ item.nombre }}</td>
                <td class="px-4 py-3">{{ formatCLP(item.precio) }}</td>
                <td class="px-4 py-3">{{ item.cantidad }}</td>
              </tr>
            </tbody>
            <tfoot class="bg-white/5">
              <tr>
                <td colspan="4" class="px-4 py-3 text-right font-semibold">Total</td>
                <td class="px-4 py-3 font-semibold">{{ formatCLP(total) }}</td>
              </tr>
            </tfoot>
          </table>
        </div>

        <!-- Mobile cards -->
        <div class="md:hidden divide-y divide-white/10">
          <div v-for="(item, idx) in carrito" :key="idx" class="p-4 flex gap-4">
            <img :src="item.imagen" :alt="item.nombre" class="h-16 w-16 object-cover rounded-md" />
            <div class="flex-1">
              <div class="flex items-center justify-between">
                <h3 class="font-medium">{{ item.nombre }}</h3>
                <span class="text-slate-300">{{ formatCLP(item.precio) }}</span>
              </div>
              <div class="mt-1 text-xs text-slate-400">ID: {{ item.id }}</div>
              <div class="mt-1 text-sm">Cantidad: <span class="font-medium">{{ item.cantidad }}</span></div>
            </div>
          </div>
          <div class="p-4 flex items-center justify-between bg-white/5">
            <span class="font-semibold">Total</span>
            <span class="font-semibold">{{ formatCLP(total) }}</span>
          </div>
        </div>
      </section>

      <!-- Acciones -->
      <div class="mt-6 flex items-center justify-end">
        <router-link
          to="/pago"
          class="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-fuchsia-500 to-indigo-500 hover:opacity-95 focus:outline-none focus:ring-2 focus:ring-white/40"
        >
          Ir a pagar
          <span aria-hidden="true">➤</span>
        </router-link>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";

const carrito = ref([
  { id: 1, nombre: "Audífonos Pro", precio: 129990, cantidad: 1, imagen: "audifonos1.png" },
  { id: 2, nombre: "Cable USB-C", precio: 19990, cantidad: 2, imagen: "cable.png" },
]);

const total = computed(() =>
  carrito.value.reduce((acc, item) => acc + item.precio * item.cantidad, 0)
);

const formatCLP = (n: number) =>
  new Intl.NumberFormat("es-CL", { style: "currency", currency: "CLP", maximumFractionDigits: 0 }).format(n);
</script>
