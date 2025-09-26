import { ref } from 'vue';
import { apiLogin, apiRegister, apiMe, apiLogout } from '@/api/auth';

const currentUser = ref(null);
const loading = ref(false);
const errorMsg = ref(null);
const isReady = ref(false);

function setToken(token) {
  if (!token) return;
  try { localStorage.setItem('auth_token', token); } catch {}
}

export function useAuth() {
  async function init() {
    try {
      loading.value = true;
      errorMsg.value = null;
      const { user } = await apiMe();
      currentUser.value = user || null;
    } catch {
      currentUser.value = null;
    } finally {
      isReady.value = true;
      loading.value = false;
    }
  }

  async function register(email, password, name) {
    try {
      loading.value = true;
      errorMsg.value = null;
      const { user, token } = await apiRegister({ email, password, name });
      if (token) setToken(token);
      if (!token) await init(); else currentUser.value = user || null;
      return true;
    } catch (e) {
      errorMsg.value = e?.response?.data?.message || 'No se pudo registrar';
      return false;
    } finally {
      loading.value = false;
    }
  }

  async function login(email, password) {
    try {
      loading.value = true;
      errorMsg.value = null;
      const { user, token } = await apiLogin({ email, password });
      if (token) setToken(token);
      if (!token) await init(); else currentUser.value = user || null;
      return true;
    } catch (e) {
      errorMsg.value = e?.response?.data?.message || 'Credenciales inválidas';
      return false;
    } finally {
      loading.value = false;
    }
  }

  async function logout() {
    try {
      loading.value = true;
      errorMsg.value = null;
      localStorage.removeItem('auth_token');
      await apiLogout().catch(() => {});
      currentUser.value = null;
      return true;
    } finally {
      loading.value = false;
    }
  }

  return { currentUser, loading, errorMsg, isReady, init, register, login, logout };
}
