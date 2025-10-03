<template>
  <div class="min-h-screen bg-slate-900 text-white">
    <AppHeader />
    <router-view />
  </div>
</template>

<script setup lang="ts">
import AppHeader from '@/components/AppHeader.vue'

</script>
