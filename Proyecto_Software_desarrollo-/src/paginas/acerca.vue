<template>
  <div class="home">
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

    <!-- CONTENEDOR PRINCIPAL -->
    <main class="main-content">
      <!-- Sección Acerca de Nosotros: imagen + texto lado a lado -->
      <section class="about-section">
        <div class="about-content">
          <!-- Imagen a la izquierda -->
          <div class="image-column">
            <img src="/generico1.jpg" alt="Tienda iEssence" class="about-img" />
          </div>
          <!-- Texto a la derecha -->
          <div class="text-column">
            <h2>Acerca de Nosotros</h2>
            <p>
              Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget
              dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes,
              nascetur ridiculus mus. Donec quam felis.
            </p>
          </div>
        </div>
      </section>

      <!-- Sección de contacto -->
      <section class="contact-section">
        <div class="contact-info">
          <div class="location">
            <span class="icon">📍</span>
            <span>Ubicación.....</span>
          </div>
          <div class="contact-details">
            <span class="icon">📞</span>
            <span>Telefono</span>
            <span class="icon">✉️</span>
            <span>Correo</span>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const menuOpen = ref(false)
const toggleMenu = () => {
  menuOpen.value = !menuOpen.value
}
</script>

<style scoped>
/* Estilos generales */
.home {
  font-family: Arial, sans-serif;
  color: #fff;
  background-color: #1f1f2e;
  min-height: 100vh;
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

/* Contenido principal */
.main-content {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

/* Sección Acerca de Nosotros */
.about-section {
  background-color: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.about-content {
  display: flex;
  gap: 2rem;
  align-items: flex-start;
  flex-wrap: wrap;
}

.image-column {
  flex: 1;
  min-width: 250px;
}

.about-img {
  max-width: 100%;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.text-column {
  flex: 2;
  min-width: 300px;
}

.text-column h2 {
  font-size: 1.8rem;
  margin-bottom: 1rem;
  color: #1a2a3e;
}

.text-column p {
  font-size: 1.1rem;
  line-height: 1.6;
  color: #333;
}

/* Sección de contacto */
.contact-section {
  background-color: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.contact-info {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.location {
  display: flex;
  align-items: center;
  font-size: 1.1rem;
  color: #333;
}

.location .icon {
  margin-right: 0.5rem;
}

.contact-details {
  display: flex;
  gap: 1.5rem;
  font-size: 1.1rem;
  color: #333;
}

.contact-details .icon {
  margin-right: 0.5rem;
}

/* click boton */
.logo-link {
  text-decoration: none;
  color: inherit;
}

/* imagen */
@media (max-width: 768px) {
  .about-content {
    flex-direction: column;
  }

  .image-column,
  .text-column {
    width: 100%;
    margin-bottom: 1rem;
  }

  .contact-details {
    flex-direction: column;
    gap: 0.5rem;
  }
}
</style>
