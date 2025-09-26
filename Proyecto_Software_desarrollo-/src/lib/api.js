
import axios from "axios";

const BASE = (import.meta.env.VITE_API_URL as string || "").replace(/\/+$/, "");

export const api = axios.create({
  baseURL: BASE,
  headers: { "Content-Type": "application/json", Accept: "application/json" },
});








// === Gestión de tokens en localStorage ===
const ACCESS_KEY = "access_token";
const REFRESH_KEY = "refresh_token";

export function setTokens(access: string, refresh: string) {
  localStorage.setItem(ACCESS_KEY, access);
  localStorage.setItem(REFRESH_KEY, refresh);
}

export function clearTokens() {
  localStorage.removeItem(ACCESS_KEY);
  localStorage.removeItem(REFRESH_KEY);
}

export function getAccess() {
  return localStorage.getItem(ACCESS_KEY) || "";
}
export function getRefresh() {
  return localStorage.getItem(REFRESH_KEY) || "";
}










// === Interceptor: añade Authorization y refresca si vence ===
api.interceptors.request.use((config) => {
  const token = getAccess();
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

let isRefreshing = false;
let queue: Array<() => void> = [];

api.interceptors.response.use(
  (r) => r,
  async (error) => {
    const original = error.config;
    // Si 401 y tenemos refresh, intentamos refrescar una sola vez
    if (error.response?.status === 401 && !original._retry) {
      if (isRefreshing) {
        await new Promise<void>((res) => queue.push(res));
        original.headers.Authorization = `Bearer ${getAccess()}`;
        return api(original);
      }
      original._retry = true;
      isRefreshing = true;
      try {
        const rt = getRefresh();
        if (!rt) throw new Error("No refresh token");
        const { data } = await axios.post(`${BASE}/api/token/refresh/`, { refresh: rt });
        setTokens(data.access, rt);
        original.headers.Authorization = `Bearer ${data.access}`;
        queue.forEach((fn) => fn());
        queue = [];
        return api(original);
      } catch (e) {
        clearTokens();
        queue.forEach((fn) => fn());
        queue = [];
        throw e;
      } finally {
        isRefreshing = false;
      }
    }
    throw error;
  }
);









// === API helpers ===
export async function loginWithEmailQuick(email: string, password: string) {
  // SimpleJWT espera "username": usamos la parte local del email que tú guardaste como username
  const username = email.split("@")[0];
  const { data } = await api.post("/api/token/", { username, password });
  setTokens(data.access, data.refresh);
  return data;
}

export async function logout() {
  clearTokens();
}

export async function getPrivado() {
  return api.get("/api/privado/");
}
