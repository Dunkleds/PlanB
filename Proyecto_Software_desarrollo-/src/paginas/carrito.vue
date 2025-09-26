<template>
  <div class="carrito">
    <!-- NAVBAR -->
    <header class="navbar">
      <button @click="toggleMenu" class="menu-btn">☰</button>

      <router-link to="/" class="logo-link">
        <h1 class="logo">iEssence</h1>
      </router-link>

      <div class="user-actions">
        <router-link to="/login" class="btn-link">Login</router-link>
        <router-link to="/register" class="btn-link">Registrarse</router-link>
        <span class="user-icon">👤</span>
      </div>
    </header>

    <!-- SIDEBAR -->
    <aside v-if="menuOpen" class="sidebar">
      <div class="sidebar-header">
        <button @click="toggleMenu" class="close-btn">✖</button>
      </div>
      <ul>
        <li><router-link to="/">Catálogo</router-link></li>
        <li><router-link to="/carrito">Carro 🛒</router-link></li>
        <li><router-link to="/acerca">Acerca de nosotros</router-link></li>
      </ul>
    </aside>

    <!-- TÍTULO -->
    <h2 class="titulo">Resumen de Carrito 🛒</h2>

    <!-- TABLA DEL CARRITO -->
    <table class="tabla-carrito">
      <thead>
        <tr>
          <th>Imagen Miniatura</th>
          <th>Id_producto</th>
          <th>Nombre Producto</th>
          <th>Precio</th>
          <th>Cantidad</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in carrito" :key="index">
          <td>
            <img :src="item.imagen" :alt="item.nombre" class="miniatura" />
          </td>
          <td>{{ item.id }}</td>
          <td>{{ item.nombre }}</td>
          <td>$ {{ item.precio }}</td>
          <td>{{ item.cantidad }}</td>
        </tr>
      </tbody>
      <tfoot>
        <tr>
          <td colspan="4" class="total-label">Total:</td>
          <td class="total-precio">$ {{ total }}</td>
        </tr>
      </tfoot>
    </table>

    <!-- BOTÓN IR A PAGAR -->
    <div class="acciones">
      <button class="btn-pagar">Ir a pagar ➤</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";

const menuOpen = ref(false);
const toggleMenu = () => {
  menuOpen.value = !menuOpen.value;
};

const carrito = ref([
  {
    id: 1,
    nombre: "Audífonos Pro",
    precio: 129990,
    cantidad: 1,
    imagen: "audifonos1.png",
  },
  {
    id: 2,
    nombre: "Cable USB-C",
    precio: 19990,
    cantidad: 2,
    imagen: "cable.png",
  },
]);

// Calcular total dinámicamente
const total = computed(() =>
  carrito.value.reduce((acc, item) => acc + item.precio * item.cantidad, 0)
);
</script>

<style scoped>
.carrito {
  font-family: Arial, sans-serif;
  color: #fff;
  background-color: #1f1f2e;
  min-height: 100vh;
  padding-bottom: 2rem;
}

/* Navbar */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #243447;
  padding: 1rem;
}

.menu-btn {
  font-size: 1.5rem;
  background: none;
  color: white;
  border: none;
  cursor: pointer;
}

.logo {
  font-size: 1.5rem;
}

.user-actions {
  display: flex;
  align-items: center;
}

.btn-link {
  margin: 0 0.5rem;
  text-decoration: none;
  border: 1px solid white;
  color: white;
  padding: 0.3rem 0.7rem;
  border-radius: 5px;
  transition: background 0.2s;
}

.btn-link:hover {
  background: white;
  color: #243447;
}

.user-icon {
  margin-left: 10px;
}

/* Sidebar */
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  width: 200px;
  height: 100%;
  background-color: #2e3a4f;
  padding: 1rem;
}

.sidebar ul {
  list-style: none;
  padding: 0;
}

.sidebar li {
  margin: 1rem 0;
}

.sidebar a {
  color: white;
  text-decoration: none;
}

.sidebar a:hover {
  text-decoration: underline;
}

.logo-link {
  text-decoration: none;
  color: inherit;
}

/* Título */
.titulo {
  text-align: center;
  background: #2c2c3e;
  padding: 0.5rem 1rem;
  border-radius: 10px;
  margin: 1.5rem auto;
  display: inline-block;
  font-size: 1.5rem;
  font-weight: bold;
}

/* Tabla */
.tabla-carrito {
  width: 90%;
  margin: 1rem auto;
  border-collapse: collapse;
  background: #2c2c3e;
  border-radius: 10px;
  overflow: hidden;
  color: #fff;
}

.tabla-carrito th,
.tabla-carrito td {
  border: 1px solid #444;
  padding: 0.8rem;
  text-align: center;
}

.tabla-carrito th {
  background: #3a3a4a;
  font-weight: bold;
}

.miniatura {
  width: 50px;
  height: auto;
  border-radius: 5px;
}

/* Total */
.total-label {
  text-align: right;
  font-weight: bold;
}

.total-precio {
  font-weight: bold;
}

/* Botón pagar */
.acciones {
  text-align: right;
  width: 90%;
  margin: 1rem auto;
}

.btn-pagar {
  background: #4cafef;
  border: none;
  padding: 0.8rem 1.5rem;
  color: white;
  font-size: 1rem;
  font-weight: bold;
  border-radius: 20px;
  cursor: pointer;
  transition: background 0.2s ease;
}

.btn-pagar:hover {
  background: #369ad6;
}
</style>
