<template>
  <div class="home">
    <header class="navbar">
      <button @click="toggleMenu" class="menu-btn">☰</button>

      <router-link to="/" class="logo-link">
        <h1 class="logo">iEssence</h1>
      </router-link>

      <div class="user-actions">
        <router-link to="/login" class="btn-link">Login</router-link>
        <router-link to="/register" class="btn-link">Registrarse</router-link>
        <router-link to="/privado" class="btn-link">privado</router-link>
        <span class="user-icon">👤</span>
      </div>
    </header>

    <aside v-if="menuOpen" class="sidebar">
      <div class="sidebar-header">
        <button @click="toggleMenu" class="close-btn">✖</button>
      </div>
      <ul>
        <li><router-link to="/">Inicio</router-link></li>
        <li><router-link to="/carrito">Carro 🛒</router-link></li>
        <li><router-link to="/acerca">Acerca de nosotros</router-link></li>
      </ul>
    </aside>

    <!-- Contenido temporal (sin productos) -->
    <main class="contenido">
      <h2 class="titulo">Bienvenido a iEssence</h2>
      <p class="subtitulo">Pronto verás aquí el catálogo cuando el endpoint esté listo.</p>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

const menuOpen = ref(false);
const toggleMenu = () => { menuOpen.value = !menuOpen.value; };
</script>

<style scoped>
/* Mantengo tus estilos base */
.home {
  font-family: Arial, sans-serif;
  color: #fff;
  background-color: #1f1f2e;
  min-height: 100vh;
}

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

/* Contenido temporal */
.contenido {
  display: grid;
  place-items: center;
  padding: 3rem 1rem;
}

.titulo {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.subtitulo {
  color: #b0b0c3;
}

/* Eliminados los estilos de .catalogo y .producto-card porque ya no se usan */
</style>
