<template>
  <div class="admin-home">
    <h1>Panel de Administración</h1>
    <p>Bienvenido al panel de control.</p>

    <div class="admin-options">
      <router-link to="/admin/productos" class="option-card">🛒 Gestionar Productos</router-link>
      <router-link to="/admin/bodegas" class="option-card">🏭 Gestionar Bodegas</router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
// Aquí puedes verificar si el usuario tiene rol admin (si hay login)
</script>

<style scoped>
.admin-home {
  text-align: center;
  margin-top: 3rem;
}

.admin-options {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  margin-top: 2rem;
}

.option-card {
  display: block;
  padding: 1.5rem;
  border-radius: 10px;
  background-color: #4caf50;
  color: white;
  text-decoration: none;
  font-weight: bold;
  transition: 0.3s;
}
.option-card:hover {
  background-color: #43a047;
}
</style>
