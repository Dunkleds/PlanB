<template>
  <main class="mx-auto max-w-3xl px-4 sm:px-6 lg:px-8 py-10 space-y-6">
    <!-- Banner de éxito tras registro -->
    <div v-if="registered" class="rounded-xl border border-emerald-400/30 bg-emerald-400/10 px-4 py-3">
      <p class="text-emerald-300">¡Tu cuenta se creó correctamente! Bienvenido/a.</p>
    </div>

<section class="grid gap-6">
      <!-- Card: Información básica -->
      <div class="rounded-2xl border border-white/10 bg-white/[0.02] p-6">
        <h2 class="text-xl font-semibold mb-4">Información básica</h2>
        <div class="text-sm text-slate-300 space-y-1">
          <p><span class="text-slate-400">Email:</span> {{ user?.email ?? '—' }}</p>
          <p><span class="text-slate-400">Nombre:</span> <span class="font-medium">{{ user?.first_name || '—' }}</span></p>
          <p><span class="text-slate-400">Apellido:</span> <span class="font-medium">{{ user?.last_name || '—' }}</span></p>
        </div>
      </div>

      <!-- Card: Actualizar nombre -->
      <div class="rounded-2xl border border-white/10 bg-white/[0.02] p-6">
        <h2 class="text-xl font-semibold mb-4">Actualizar datos personales</h2>
        <form @submit.prevent="onUpdateNames" class="grid gap-3">
          <div class="grid gap-3 sm:grid-cols-2">
            <div>
              <label class="block text-sm text-slate-300 mb-1">Nombre</label>
              <input
                v-model="firstName"
                type="text"
                required
                class="w-full rounded-xl bg-slate-800 border border-white/10 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-400"
                placeholder="Nombre"
              />
            </div>
            <div>
              <label class="block text-sm text-slate-300 mb-1">Apellido</label>
              <input
                v-model="lastName"
                type="text"
                required
                class="w-full rounded-xl bg-slate-800 border border-white/10 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-400"
                placeholder="Apellido"
              />
            </div>
          </div>
          <div class="flex items-center gap-3">
            <button
              type="submit"
              :disabled="auth.loading"
              class="inline-flex items-center gap-2 rounded-xl px-4 py-2 bg-indigo-500 hover:bg-indigo-600 focus:outline-none focus:ring-2 focus:ring-indigo-300 disabled:opacity-60"
            >
              Guardar
            </button>
            <span v-if="savedOk" class="text-emerald-300 text-sm">Datos actualizados</span>
          </div>
          <p v-if="auth.error" class="text-red-400 text-sm">{{ auth.error }}</p>
        </form>
      </div>

      <!-- Card: Opciones varias -->
      <div class="rounded-2xl border border-white/10 bg-white/[0.02] p-6">
        <h2 class="text-xl font-semibold mb-4">Opciones</h2>
        <ul class="grid gap-2 text-sm">
          <li class="flex items-center justify-between">
            <span class="text-slate-300">Cambiar contraseña (próximamente)</span>
            <button disabled class="px-3 py-1.5 rounded-lg border border-white/10 text-slate-400">En desarrollo</button>
          </li>
          <li class="flex items-center justify-between">
            <span class="text-slate-300">Cerrar sesión</span>
            <button @click="signout" class="px-3 py-1.5 rounded-lg border border-white/20 hover:bg-white/10">Salir</button>
          </li>
        </ul>
      </div>

      <!-- Card: Direcciones de despacho -->
      <div class="rounded-2xl border border-white/10 bg-white/[0.02] p-6">
        <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h2 class="text-xl font-semibold">Direcciones de despacho</h2>
            <p class="text-sm text-slate-400">Puedes registrar hasta dos direcciones y marcar una como principal.</p>
          </div>
          <button
            v-if="!formVisible && canAddDispatch"
            @click="startCreateDispatch"
            class="inline-flex items-center gap-2 rounded-xl border border-white/20 px-4 py-2 text-sm hover:bg-white/10 focus:outline-none focus:ring-2 focus:ring-white/40"
            :disabled="dispatchLoading"
          >
            Nueva dirección
          </button>
        </div>

        <p v-else-if="!formVisible" class="mt-3 text-sm text-amber-300">Ya tienes el máximo de direcciones. Edita o elimina una existente para agregar otra.</p>

        <div v-if="dispatchError" class="mt-4 rounded-xl border border-red-500/30 bg-red-500/10 px-3 py-2 text-sm text-red-200">
          {{ dispatchError }}
        </div>

        <div v-if="dispatches.length" class="mt-4 grid gap-3">
          <article
            v-for="item in dispatches"
            :key="item.id"
            class="rounded-xl border border-white/10 bg-slate-900/70 p-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between"
          >
            <div class="space-y-1 text-sm text-slate-300">
              <p class="text-base font-semibold text-white">
                {{ item.label }}
                <span v-if="item.is_default" class="ml-2 rounded-full bg-emerald-500/20 px-2 py-0.5 text-emerald-200 text-xs uppercase">Predeterminada</span>
              </p>
              <p>{{ item.recipient_name }} · {{ item.phone || 'Sin teléfono' }}</p>
              <p>
                {{ item.street }}
                <span v-if="item.number">#{{ item.number }}</span>
                <span v-if="item.apartment">, Depto {{ item.apartment }}</span>
              </p>
              <p>
                {{ [item.commune, item.city, item.region].filter(Boolean).join(', ') }}
              </p>
              <p>{{ item.country }} <span v-if="item.postal_code">· {{ item.postal_code }}</span></p>
            </div>
            <div class="flex gap-2">
              <button
                class="rounded-lg border border-white/20 px-3 py-1.5 text-xs uppercase tracking-wide hover:bg-white/10 focus:outline-none focus:ring-2 focus:ring-white/40"
                @click="startEditDispatch(item)"
                :disabled="dispatchLoading"
              >
                Editar
              </button>
              <button
                class="rounded-lg border border-white/20 px-3 py-1.5 text-xs uppercase tracking-wide hover:bg-white/10 focus:outline-none focus:ring-2 focus:ring-white/40"
                @click="setDefaultDispatch(item)"
                :disabled="dispatchLoading || item.is_default"
              >
                Predeterminar
              </button>
              <button
                class="rounded-lg border border-red-400/40 px-3 py-1.5 text-xs uppercase tracking-wide text-red-200 hover:bg-red-500/10 focus:outline-none focus:ring-2 focus:ring-red-300"
                @click="removeDispatch(item)"
                :disabled="dispatchLoading"
              >
                Eliminar
              </button>
            </div>
          </article>
        </div>

        <p v-else-if="!formVisible" class="mt-4 text-sm text-slate-300">Aún no registras direcciones de despacho.</p>

        <form v-if="formVisible" class="mt-6 grid gap-4" @submit.prevent="submitDispatch">
          <div class="grid gap-4 sm:grid-cols-2">
            <div>
              <label class="block text-sm text-slate-300 mb-1">Etiqueta</label>
              <input
                v-model="dispatchForm.label"
                type="text"
                maxlength="40"
                required
                class="w-full rounded-xl bg-slate-800 border border-white/10 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-400"
                placeholder="Casa, Trabajo..."
              />
            </div>
            <div>
              <label class="block text-sm text-slate-300 mb-1">Destinatario</label>
              <input
                v-model="dispatchForm.recipient_name"
                type="text"
                maxlength="120"
                required
                class="w-full rounded-xl bg-slate-800 border border-white/10 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-400"
                placeholder="Nombre completo"
              />
            </div>
            <div>
              <label class="block text-sm text-slate-300 mb-1">Teléfono</label>
              <input
                v-model="dispatchForm.phone"
                type="tel"
                maxlength="30"
                class="w-full rounded-xl bg-slate-800 border border-white/10 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-400"
                placeholder="+56 9..."
              />
            </div>
            <div>
              <label class="block text-sm text-slate-300 mb-1">Calle</label>
              <input
                v-model="dispatchForm.street"
                type="text"
                maxlength="120"
                required
                class="w-full rounded-xl bg-slate-800 border border-white/10 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-400"
              />
            </div>
            <div>
              <label class="block text-sm text-slate-300 mb-1">Número</label>
              <input
                v-model="dispatchForm.number"
                type="text"
                maxlength="20"
                class="w-full rounded-xl bg-slate-800 border border-white/10 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-400"
              />
            </div>
            <div>
              <label class="block text-sm text-slate-300 mb-1">Departamento</label>
              <input
                v-model="dispatchForm.apartment"
                type="text"
                maxlength="20"
                class="w-full rounded-xl bg-slate-800 border border-white/10 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-400"
              />
            </div>
            <div>
              <label class="block text-sm text-slate-300 mb-1">Comuna</label>
              <input
                v-model="dispatchForm.commune"
                type="text"
                maxlength="80"
                class="w-full rounded-xl bg-slate-800 border border-white/10 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-400"
              />
            </div>
            <div>
              <label class="block text-sm text-slate-300 mb-1">Ciudad</label>
              <input
                v-model="dispatchForm.city"
                type="text"
                maxlength="80"
                required
                class="w-full rounded-xl bg-slate-800 border border-white/10 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-400"
              />
            </div>
            <div>
              <label class="block text-sm text-slate-300 mb-1">Región</label>
              <input
                v-model="dispatchForm.region"
                type="text"
                maxlength="80"
                class="w-full rounded-xl bg-slate-800 border border-white/10 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-400"
              />
            </div>
            <div>
              <label class="block text-sm text-slate-300 mb-1">País</label>
              <input
                v-model="dispatchForm.country"
                type="text"
                maxlength="60"
                required
                class="w-full rounded-xl bg-slate-800 border border-white/10 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-400"
              />
            </div>
            <div>
              <label class="block text-sm text-slate-300 mb-1">Código postal</label>
              <input
                v-model="dispatchForm.postal_code"
                type="text"
                maxlength="20"
                class="w-full rounded-xl bg-slate-800 border border-white/10 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-400"
              />
            </div>
          </div>
          <label class="flex items-center gap-2 text-sm text-slate-300">
            <input type="checkbox" v-model="dispatchForm.is_default" class="h-4 w-4 rounded border-white/20 bg-slate-800" />
            Marcar como dirección predeterminada
          </label>
          <div class="flex flex-wrap gap-3">
            <button
              type="submit"
              :disabled="dispatchLoading"
              class="inline-flex items-center gap-2 rounded-xl bg-indigo-500 px-4 py-2 text-sm font-medium hover:bg-indigo-600 focus:outline-none focus:ring-2 focus:ring-indigo-300 disabled:opacity-60"
            >
              {{ editingDispatchId ? 'Actualizar' : 'Guardar' }}
            </button>
            <button
              type="button"
              @click="cancelDispatchForm"
              class="inline-flex items-center gap-2 rounded-xl border border-white/20 px-4 py-2 text-sm hover:bg-white/10 focus:outline-none focus:ring-2 focus:ring-white/40"
              :disabled="dispatchLoading"
            >
              Cancelar
            </button>
          </div>
        </form>
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuth } from '@/services/auth'
import {
  listDispatch,
  createDispatch,
  updateDispatch,
  deleteDispatch,
  type DispatchInfo,
} from '@/lib/api'

const route = useRoute()
const router = useRouter()
const auth = useAuth()

const registered = computed(() => route.query.registered === '1')
const user = computed(() => auth.user)

const firstName = ref('')
const lastName = ref('')
const savedOk = ref(false)
const dispatches = ref<DispatchInfo[]>([])
const dispatchLoading = ref(false)
const dispatchError = ref<string | null>(null)
const formVisible = ref(false)
const editingDispatchId = ref<number | null>(null)

type DispatchForm = Omit<DispatchInfo, 'id' | 'created_at' | 'updated_at'>

const dispatchForm = reactive<DispatchForm>({
  label: 'Principal',
  recipient_name: '',
  phone: '',
  street: '',
  number: '',
  apartment: '',
  commune: '',
  city: '',
  region: '',
  country: 'Chile',
  postal_code: '',
  is_default: false,
})

const canAddDispatch = computed(() => dispatches.value.length < 2)

function extractErrorMessage(error: any, fallback: string): string {
  const detail = error?.response?.data?.detail
  if (typeof detail === 'string') return detail
  const data = error?.response?.data
  if (typeof data === 'string') return data
  const message = error?.message
  if (typeof message === 'string') return message
  return fallback
}

onMounted(async () => {
  if (!auth.isAuth) {
    router.replace({ name: 'login', query: { redirect: '/perfil' } })
    return
  }
  await auth.fetchMe()
  firstName.value = auth.user.first_name ?? ''
  lastName.value = auth.user.last_name ?? ''
  await loadDispatches()
})

async function onUpdateNames() {
  savedOk.value = false
  await auth.updateNames(firstName.value.trim(), lastName.value.trim())
  savedOk.value = true
}

function signout() {
  auth.signout()
  router.replace({ name: 'login' })
}

function resetDispatchForm() {
  dispatchForm.label = 'Principal'
  dispatchForm.recipient_name = ''
  dispatchForm.phone = ''
  dispatchForm.street = ''
  dispatchForm.number = ''
  dispatchForm.apartment = ''
  dispatchForm.commune = ''
  dispatchForm.city = ''
  dispatchForm.region = ''
  dispatchForm.country = 'Chile'
  dispatchForm.postal_code = ''
  dispatchForm.is_default = dispatches.value.length === 0
}

async function loadDispatches() {
  dispatchLoading.value = true
  dispatchError.value = null
  try {
    dispatches.value = await listDispatch()
  } catch (error: any) {
    dispatchError.value = extractErrorMessage(error, 'No se pudieron cargar las direcciones.')
  } finally {
    dispatchLoading.value = false
  }
}

function startCreateDispatch() {
  if (!canAddDispatch.value) {
    dispatchError.value = 'Solo puedes registrar hasta 2 direcciones de despacho.'
    return
  }
  editingDispatchId.value = null
  resetDispatchForm()
  formVisible.value = true
  dispatchError.value = null
}

function startEditDispatch(item: DispatchInfo) {
  editingDispatchId.value = item.id
  dispatchForm.label = item.label
  dispatchForm.recipient_name = item.recipient_name
  dispatchForm.phone = item.phone
  dispatchForm.street = item.street
  dispatchForm.number = item.number
  dispatchForm.apartment = item.apartment
  dispatchForm.commune = item.commune
  dispatchForm.city = item.city
  dispatchForm.region = item.region
  dispatchForm.country = item.country
  dispatchForm.postal_code = item.postal_code
  dispatchForm.is_default = item.is_default
  formVisible.value = true
  dispatchError.value = null
}

function cancelDispatchForm() {
  formVisible.value = false
  editingDispatchId.value = null
  dispatchError.value = null
  resetDispatchForm()
}

function buildDispatchPayload(): DispatchForm {
  return {
    label: dispatchForm.label.trim() || 'Principal',
    recipient_name: dispatchForm.recipient_name.trim(),
    phone: dispatchForm.phone.trim(),
    street: dispatchForm.street.trim(),
    number: dispatchForm.number.trim(),
    apartment: dispatchForm.apartment.trim(),
    commune: dispatchForm.commune.trim(),
    city: dispatchForm.city.trim(),
    region: dispatchForm.region.trim(),
    country: dispatchForm.country.trim() || 'Chile',
    postal_code: dispatchForm.postal_code.trim(),
    is_default: dispatchForm.is_default,
  }
}

async function submitDispatch() {
  dispatchLoading.value = true
  dispatchError.value = null
  const payload = buildDispatchPayload()
  try {
    if (editingDispatchId.value) {
      await updateDispatch(editingDispatchId.value, payload)
    } else {
      await createDispatch(payload)
    }
    await loadDispatches()
    cancelDispatchForm()
  } catch (error: any) {
    dispatchError.value = extractErrorMessage(error, 'No se pudo guardar la dirección.')
  } finally {
    dispatchLoading.value = false
  }
}

async function removeDispatch(item: DispatchInfo) {
  if (dispatchLoading.value) return
  if (!confirm(`¿Eliminar la dirección "${item.label}"?`)) return
  dispatchLoading.value = true
  dispatchError.value = null
  try {
    await deleteDispatch(item.id)
    await loadDispatches()
    if (editingDispatchId.value === item.id) {
      cancelDispatchForm()
    }
  } catch (error: any) {
    dispatchError.value = extractErrorMessage(error, 'No se pudo eliminar la dirección.')
  } finally {
    dispatchLoading.value = false
  }
}

async function setDefaultDispatch(item: DispatchInfo) {
  if (dispatchLoading.value || item.is_default) return
  dispatchLoading.value = true
  dispatchError.value = null
  try {
    await updateDispatch(item.id, { is_default: true })
    await loadDispatches()
  } catch (error: any) {
    dispatchError.value = extractErrorMessage(error, 'No se pudo marcar como predeterminada.')
  } finally {
    dispatchLoading.value = false
  }
}
</script>
