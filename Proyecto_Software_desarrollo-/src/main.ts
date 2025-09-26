import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'

// IMPORTANTE: importa el CSS de Tailwind
import './assets/tailwind.css'

const app = createApp(App)

app.use(createPinia())   // ← IMPORTANTE
app.use(router)

app.mount('#app')
