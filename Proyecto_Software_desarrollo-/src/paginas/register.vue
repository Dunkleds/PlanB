<template>
  <div class="auth-container">
    <div class="auth-box">
      <h2 class="title">Registro</h2>
      <form @submit.prevent="register">
        <input type="email" v-model="email" placeholder="Dirección de correo" required />
        <input type="password" v-model="password" placeholder="Crear contraseña" required />
        <input type="password" v-model="confirmPassword" placeholder="Repite contraseña" required />
        <router-link to="/login" class="btn-link">Login</router-link>

        <div class="social-buttons">
          <button type="button" class="btn-social facebook">Facebook</button>
          <button type="button" class="btn-social google">Google</button>
          <button type="button" class="btn-social apple">Apple</button>
        </div>

        <button type="submit" class="btn-main">Continuar</button>
      </form>
    </div>
    <!-- logo -->
    <router-link to="/" class="logo-link">
      <h1 class="logo">iEssence</h1>
    </router-link>
  </div>
</template>

<script setup lang="ts">
/* ----------------------------
   ✅ Imports
----------------------------- */
import { ref } from 'vue'
import axios from 'axios'

/* ----------------------------
   ✅ Axios con baseURL desde Vite
   - En dev:  VITE_API_URL=http://127.0.0.1:8000
   - En prod: VITE_API_URL=https://planb-production.up.railway.app
----------------------------- */
const API_BASE = (import.meta.env.VITE_API_URL as string) || ''
if (!API_BASE) {
  console.warn('VITE_API_URL no está definida. Configúrala para que el registro funcione.')
}
const api = axios.create({ baseURL: API_BASE })

/* ----------------------------
   ✅ Variables reactivas
----------------------------- */
const email = ref('')
const password = ref('')
const confirmPassword = ref('')

/* ----------------------------
   ✅ Lógica de registro (conexión backend Django)
----------------------------- */
const register = async () => {
  if (password.value !== confirmPassword.value) {
    alert('Las contraseñas no coinciden')
    return
  }

  try {
    // OJO: usar slash final en /api/register/
    const { data } = await api.post('/api/register/', {
      email: email.value,
      password: password.value
    })

    alert(data?.message ?? 'Usuario creado con éxito')
    email.value = ''
    password.value = ''
    confirmPassword.value = ''
  } catch (error: unknown) {
    const err = error as any
    const msg =
      err?.response?.data?.error ||
      err?.response?.data?.detail ||
      err?.message ||
      'Error en el registro'
    alert(String(msg))
  }
}
</script>

<style scoped>
/* Contenedor principal centrado */
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: #1f1f2e;
  color: white;
}

/* Caja del formulario */
.auth-box {
  background: #2c2c3e;
  padding: 2rem;
  border-radius: 12px;
  width: 100%;
  max-width: 400px;
  text-align: center;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.3);
}

/* Título */
.title {
  margin-bottom: 1.5rem;
  font-size: 1.8rem;
  font-weight: bold;
}

/* Inputs */
input {
  display: block;
  width: 100%;
  padding: 0.8rem;
  margin: 0.7rem 0;
  border-radius: 8px;
  border: none;
  outline: none;
  background: #3a3a4d;
  color: white;
  font-size: 1rem;
}

input::placeholder {
  color: #b0b0c3;
}

/* Botones sociales */
.social-buttons {
  display: flex;
  justify-content: space-between;
  margin: 1rem 0;
}

.btn-social {
  flex: 1;
  margin: 0 0.3rem;
  padding: 0.6rem;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-weight: bold;
  transition: transform 0.2s ease;
}

.btn-social:hover {
  transform: scale(1.05);
}

.facebook {
  background: #3b5998;
  color: white;
}

.google {
  background: #db4437;
  color: white;
}

.apple {
  background: #000;
  color: white;
}

/* Botón principal */
.btn-main {
  width: 100%;
  padding: 0.8rem;
  border-radius: 8px;
  border: none;
  background: #4cafef;
  color: white;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  margin-top: 1rem;
  transition: background 0.2s ease;
}

.btn-main:hover {
  background: #369ad6;
}

.logo-link {
  position: absolute;
  top: 20px;
  left: 20px;
  color: white;
  text-decoration: none;
  font-size: 1.8rem;
  font-weight: bold;
}

.logo {
  margin: 0;
}
</style>
