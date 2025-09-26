<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-4">📊 Reportes de Inventario</h1>

    <!-- Tabla de productos -->
    <div class="overflow-x-auto bg-white shadow rounded-lg p-4 mb-6">
      <h2 class="text-xl font-semibold mb-3">Resumen de Productos</h2>
      <table class="w-full border-collapse border border-gray-200">
        <thead class="bg-gray-100">
          <tr>
            <th class="border border-gray-300 p-2">Producto</th>
            <th class="border border-gray-300 p-2">Categoría</th>
            <th class="border border-gray-300 p-2">Stock</th>
            <th class="border border-gray-300 p-2">Mínimo</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in productos" :key="index">
            <td class="border border-gray-300 p-2">{{ item.nombre }}</td>
            <td class="border border-gray-300 p-2">{{ item.categoria }}</td>
            <td
              class="border border-gray-300 p-2"
              :class="item.stock < item.minimo ? 'text-red-500 font-bold' : ''"
            >
              {{ item.stock }}
            </td>
            <td class="border border-gray-300 p-2">{{ item.minimo }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Gráfico -->
    <div class="bg-white shadow rounded-lg p-4">
      <h2 class="text-xl font-semibold mb-3">Stock por Categoría</h2>
      <canvas id="stockChart"></canvas>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { Chart, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

// Registrar componentes de Chart.js
Chart.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

// Datos de prueba
const productos = [
  { nombre: 'Laptop', categoria: 'Electrónica', stock: 8, minimo: 5 },
  { nombre: 'Mouse', categoria: 'Electrónica', stock: 3, minimo: 10 },
  { nombre: 'Silla', categoria: 'Muebles', stock: 15, minimo: 5 },
  { nombre: 'Escritorio', categoria: 'Muebles', stock: 4, minimo: 6 },
  { nombre: 'Café', categoria: 'Alimentos', stock: 20, minimo: 10 },
]

// Cuando se monta el componente, se dibuja el gráfico
onMounted(() => {
  const ctx = document.getElementById('stockChart') as HTMLCanvasElement

  // Agrupar stock por categoría
  const categorias = [...new Set(productos.map((p) => p.categoria))]
  const stockPorCategoria = categorias.map((cat) =>
    productos.filter((p) => p.categoria === cat).reduce((acc, p) => acc + p.stock, 0)
  )

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: categorias,
      datasets: [
        {
          label: 'Stock disponible',
          data: stockPorCategoria,
          backgroundColor: ['#3B82F6', '#10B981', '#F59E0B'], // azul, verde, amarillo
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'top' },
      },
    },
  })
})
</script>

<style scoped>
h1,
h2 {
  color: #1f2937; /* gris oscuro */
}
</style>
