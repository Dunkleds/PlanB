<template>
  <div class="p-6 space-y-8">
    <h1 class="text-2xl font-bold text-white mb-6">Mi perfil</h1>

    <!-- 🧍 Datos del usuario -->
    <section class="bg-slate-900 p-6 rounded-2xl border border-white/10">
      <h2 class="text-xl font-semibold text-white mb-4">Información personal</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-slate-300">
        <p><span class="font-semibold">Nombre:</span> {{ user.first_name }}</p>
        <p><span class="font-semibold">Apellido:</span> {{ user.last_name }}</p>
        <p><span class="font-semibold">Correo:</span> {{ user.email }}</p>
      </div>
    </section>

    <!-- 🚚 Direcciones de despacho -->
    <section class="bg-slate-900 p-6 rounded-2xl border border-white/10">
      <h2 class="text-xl font-semibold text-white mb-4">Direcciones de despacho</h2>

      <!-- Lista de direcciones -->
      <div v-if="dispatches.length" class="space-y-3 mb-6">
        <div
          v-for="item in dispatches"
          :key="item.id"
          class="bg-slate-800 p-4 rounded-xl flex justify-between items-center border border-white/10"
        >
          <div>
            <p class="text-white font-medium">{{ item.label }}</p>
            <p class="text-slate-400 text-sm">
              {{ item.recipient_name }} · {{ item.phone || 'Sin teléfono' }}
            </p>
            <p class="text-slate-400 text-sm">{{ item.street }} {{ item.number }}, {{ item.commune }}</p>
            <p class="text-slate-400 text-xs">
              {{ item.city }}, {{ item.region }}, {{ item.country }} {{ item.postal_code }}
            </p>
          </div>
          <div class="flex gap-2">
            <button @click="editDispatch(item)" class="text-indigo-400 hover:text-indigo-300 text-sm">
              Editar
            </button>
            <button @click="removeDispatch(item)" class="text-red-400 hover:text-red-300 text-sm">
              Eliminar
            </button>
          </div>
        </div>
      </div>

      <!-- Formulario nueva dirección -->
      <div class="border-t border-white/10 pt-4">
        <h3 class="text-lg font-medium text-white mb-4">
          {{ editingDispatchId ? 'Editar dirección' : 'Agregar nueva dirección' }}
        </h3>

        <form @submit.prevent="submitDispatch" class="space-y-4">
          <!-- Nombre automático -->
          <div>
            <label class="block text-sm text-slate-300 mb-1">Destinatario</label>
            <p class="bg-slate-800 border border-white/10 rounded-xl px-3 py-2 text-white">
              {{ user.first_name }} {{ user.last_name }}
            </p>
          </div>

          <!-- Teléfono -->
          <div>
            <label class="block text-sm text-slate-300 mb-1">Teléfono</label>
            <input
              v-model="dispatchForm.phone"
              type="tel"
              required
              class="w-full rounded-xl bg-slate-800 border border-white/10 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-400"
              placeholder="+56 9 1234 5678"
            />
          </div>

          <!-- Dirección -->
          <div>
            <label class="block text-sm text-slate-300 mb-1">Calle y número</label>
            <div class="flex gap-2">
              <input
                v-model="dispatchForm.street"
                placeholder="Calle"
                class="w-full rounded-xl bg-slate-800 border border-white/10 px-3 py-2"
              />
              <input
                v-model="dispatchForm.number"
                placeholder="N°"
                class="w-24 rounded-xl bg-slate-800 border border-white/10 px-3 py-2"
              />
            </div>
          </div>

          <div class="flex gap-2">
            <input
              v-model="dispatchForm.apartment"
              placeholder="Departamento / Casa"
              class="w-1/2 rounded-xl bg-slate-800 border border-white/10 px-3 py-2"
            />
            <input
              v-model="dispatchForm.commune"
              placeholder="Comuna"
              class="w-1/2 rounded-xl bg-slate-800 border border-white/10 px-3 py-2"
            />
          </div>

          <div class="flex gap-2">
            <input
              v-model="dispatchForm.city"
              placeholder="Ciudad"
              class="w-1/2 rounded-xl bg-slate-800 border border-white/10 px-3 py-2"
            />
            <input
              v-model="dispatchForm.region"
              placeholder="Región"
              class="w-1/2 rounded-xl bg-slate-800 border border-white/10 px-3 py-2"
            />
          </div>

          <div>
            <input
              v-model="dispatchForm.country"
              placeholder="País"
              class="w-full rounded-xl bg-slate-800 border border-white/10 px-3 py-2"
            />
          </div>

          <!-- Botón de búsqueda -->
          <button
            @click="searchAddress"
            type="button"
            class="w-full bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl py-2 transition"
          >
            Buscar en el mapa
          </button>

          <!-- Mapa -->
          <div ref="mapElement" class="w-full h-72 rounded-xl overflow-hidden border border-white/10"></div>

          <div v-if="dispatchForm.latitude && dispatchForm.longitude" class="text-sm text-slate-400 mt-2">
            📍 Lat: {{ dispatchForm.latitude.toFixed(5) }}, Lng: {{ dispatchForm.longitude.toFixed(5) }}
          </div>

          <button
            type="submit"
            class="w-full bg-green-600 hover:bg-green-700 text-white rounded-xl py-2 transition"
          >
            {{ editingDispatchId ? 'Guardar cambios' : 'Agregar dirección' }}
          </button>
        </form>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import L from 'leaflet'
import { useAuthStore } from '@/stores/auth'
import { createDispatch, updateDispatch, deleteDispatch, getDispatches } from '@/api/dispatch'

const user = useAuthStore()

const dispatches = ref<any[]>([])
const dispatchForm = ref({
  label: '',
  phone: '',
  street: '',
  number: '',
  apartment: '',
  commune: '',
  city: '',
  region: '',
  country: '',
  postal_code: '',
  is_default: false,
  latitude: null,
  longitude: null,
})
const editingDispatchId = ref<number | null>(null)

// Mapa
const map = ref<L.Map | null>(null)
const marker = ref<L.Marker | null>(null)
const mapElement = ref<HTMLDivElement | null>(null)

// Cargar direcciones guardadas
async function loadDispatches() {
  dispatches.value = await getDispatches()
}
onMounted(loadDispatches)

// Inicializar mapa
onMounted(() => {
  if (mapElement.value) {
    map.value = L.map(mapElement.value).setView([-33.45, -70.66], 13)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors',
    }).addTo(map.value)
    marker.value = L.marker([-33.45, -70.66], { draggable: true }).addTo(map.value)

    marker.value.on('moveend', (e) => {
      const { lat, lng } = e.target.getLatLng()
      dispatchForm.value.latitude = lat
      dispatchForm.value.longitude = lng
    })

    map.value.on('click', (e) => {
      const { lat, lng } = e.latlng
      marker.value?.setLatLng([lat, lng])
      dispatchForm.value.latitude = lat
      dispatchForm.value.longitude = lng
    })
  }
})

// Buscar dirección
async function searchAddress() {
  const query = `${dispatchForm.value.street} ${dispatchForm.value.number}, ${dispatchForm.value.commune}, ${dispatchForm.value.city}, ${dispatchForm.value.region}, ${dispatchForm.value.country}`
  const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}`
  const response = await fetch(url)
  const results = await response.json()
  if (results.length > 0) {
    const { lat, lon } = results[0]
    const latitude = parseFloat(lat)
    const longitude = parseFloat(lon)
    dispatchForm.value.latitude = latitude
    dispatchForm.value.longitude = longitude
    map.value?.setView([latitude, longitude], 16)
    marker.value?.setLatLng([latitude, longitude])
  } else {
    alert('No se encontró la dirección. Intenta ser más específico.')
  }
}

// CRUD de direcciones
async function submitDispatch() {
  const payload = {
    ...dispatchForm.value,
    recipient_name: `${user.value?.first_name || ''} ${user.value?.last_name || ''}`.trim(),
  }
  if (editingDispatchId.value) {
    await updateDispatch(editingDispatchId.value, payload)
  } else {
    await createDispatch(payload)
  }
  await loadDispatches()
  resetForm()
}

function resetForm() {
  dispatchForm.value = {
    label: '',
    phone: '',
    street: '',
    number: '',
    apartment: '',
    commune: '',
    city: '',
    region: '',
    country: '',
    postal_code: '',
    is_default: false,
    latitude: null,
    longitude: null,
  }
  editingDispatchId.value = null
}

async function removeDispatch(item: any) {
  if (confirm(`¿Eliminar la dirección "${item.label}"?`)) {
    await deleteDispatch(item.id)
    await loadDispatches()
  }
}

function editDispatch(item: any) {
  dispatchForm.value = { ...item }
  editingDispatchId.value = item.id
  if (map.value && item.latitude && item.longitude) {
    map.value.setView([item.latitude, item.longitude], 16)
    marker.value?.setLatLng([item.latitude, item.longitude])
  }
}
</script>

<style scoped>
.leaflet-container {
  width: 100%;
  height: 100%;
}
</style>
