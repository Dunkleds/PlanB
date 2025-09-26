<template>
  <div class="wrap">
    <h1>✅ Estás logeado</h1>
    <p v-if="email">Sesión de: <strong>{{ email }}</strong></p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAuth } from '@/services/auth' // tu store vive en services/auth.js

const auth = useAuth()
// si el store aún no tiene email, no pasa nada—igual mostramos el check.
const email = computed(() => auth?.email || '')
</script>

<style scoped>
.wrap {
  min-height: 50vh;
  display: grid;
  place-items: center;
  text-align: center;
}
</style>
