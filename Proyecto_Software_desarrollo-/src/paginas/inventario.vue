<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-4">Inventario</h1>
    <button @click="cargarInventario" class="bg-blue-500 text-white px-4 py-2 rounded mb-4">
      Recargar
    </button>

    <table class="w-full border">
      <thead class="bg-gray-200">
        <tr>
          <th class="border p-2">ID</th>
          <th class="border p-2">Producto</th>
          <th class="border p-2">Cantidad</th>
          <th class="border p-2">Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in items" :key="item.id">
          <td class="border p-2">{{ item.id }}</td>
          <td class="border p-2">{{ item.nombre }}</td>
          <td class="border p-2">{{ item.cantidad }}</td>
          <td class="border p-2">
            <button @click="eliminar(item.id)" class="bg-red-500 text-white px-2 rounded">Eliminar</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import axios from "axios";

const items = ref<any[]>([]);

// Cargar inventario desde el backend
async function cargarInventario() {
  try {
    const res = await axios.get("http://localhost:8000/api/inventario");
    items.value = res.data;
  } catch (err) {
    console.error("Error cargando inventario", err);
  }
}

// Eliminar un producto
async function eliminar(id: number) {
  try {
    await axios.delete(`http://localhost:8000/api/inventario/${id}`);
    items.value = items.value.filter((i) => i.id !== id);
  } catch (err) {
    console.error("Error eliminando producto", err);
  }
}

onMounted(() => {
  cargarInventario();
});
</script>
