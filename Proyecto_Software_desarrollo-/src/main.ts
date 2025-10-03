import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import { useAuth } from '@/services/auth'
import 'leaflet/dist/leaflet.css'
// IMPORTANTE: importa el CSS de Tailwind
import './assets/tailwind.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

app.mount('#app')

const auth = useAuth(pinia)
auth.$patch({})
auth.fetchMe().catch(() => { /* silent: tokens inválidos */ })
// TODO: hydrate authenticated user via /auth/me when the backend exposes it.
