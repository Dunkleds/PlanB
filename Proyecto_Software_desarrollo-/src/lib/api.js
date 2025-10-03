import axios from 'axios';
const rawBaseURL = import.meta.env.VITE_API_URL ?? '';
const baseURL = rawBaseURL.replace(/\/+$/, '');
const ACCESS_KEY = 'access_token';
const REFRESH_KEY = 'refresh_token';
const TOKEN_URL = '/api/token/'; // TODO adjust if backend differs
const REFRESH_URL = '/api/token/refresh/'; // TODO adjust if backend differs
// Reminder: backend CORS must allow these origins when deploying on Netlify.
// https://<SITE>.netlify.app
// https://deploy-preview-*.netlify.app
export const api = axios.create({
    baseURL: baseURL || undefined,
    headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
    },
});
let isRefreshing = false;
let refreshQueue = [];
function setAuthHeader(config, token) {
    if (!token)
        return;
    if (!config.headers) {
        config.headers = { Authorization: `Bearer ${token}` };
        return;
    }
    const headers = config.headers;
    if (typeof headers.set === 'function') {
        headers.set('Authorization', `Bearer ${token}`);
    }
    else {
        headers.Authorization = `Bearer ${token}`;
    }
}
function drainQueue(error, token) {
    refreshQueue.forEach(({ onSuccess, onError }) => {
        if (error || !token) {
            onError(error ?? new Error('Token refresh failed'));
            return;
        }
        onSuccess(token);
    });
    refreshQueue = [];
}
export function setTokens(access, refresh) {
    if (access) {
        localStorage.setItem(ACCESS_KEY, access);
    }
    else {
        localStorage.removeItem(ACCESS_KEY);
    }
    if (refresh) {
        localStorage.setItem(REFRESH_KEY, refresh);
    }
    else {
        localStorage.removeItem(REFRESH_KEY);
    }
}
export function getAccessToken() {
    return localStorage.getItem(ACCESS_KEY);
}
export function getRefreshToken() {
    return localStorage.getItem(REFRESH_KEY);
}
export function clearTokens() {
    localStorage.removeItem(ACCESS_KEY);
    localStorage.removeItem(REFRESH_KEY);
}
api.interceptors.request.use((config) => {
    const access = getAccessToken();
    if (access) {
        setAuthHeader(config, access);
    }
    return config;
});
api.interceptors.response.use((response) => response, async (error) => {
    const originalRequest = (error.config || {});
    if (error.response?.status !== 401 || originalRequest._retry) {
        throw error;
    }
    const refreshToken = getRefreshToken();
    if (!refreshToken) {
        clearTokens();
        redirectToLogin();
        throw error;
    }
    if (isRefreshing) {
        return new Promise((resolve, reject) => {
            refreshQueue.push({
                onSuccess: (token) => {
                    setAuthHeader(originalRequest, token);
                    resolve(api(originalRequest));
                },
                onError: reject,
            });
        });
    }
    originalRequest._retry = true;
    isRefreshing = true;
    try {
        const { data } = await axios.post(`${baseURL}${REFRESH_URL}`, { refresh: refreshToken }, { headers: { Accept: 'application/json', 'Content-Type': 'application/json' } });
        const newAccess = data?.access;
        const newRefresh = data?.refresh ?? refreshToken;
        if (!newAccess) {
            throw new Error('Refresh endpoint did not return access token');
        }
        setTokens(newAccess, newRefresh);
        drainQueue(undefined, newAccess);
        setAuthHeader(originalRequest, newAccess);
        return api(originalRequest);
    }
    catch (refreshError) {
        drainQueue(refreshError);
        clearTokens();
        redirectToLogin();
        throw refreshError;
    }
    finally {
        isRefreshing = false;
    }
});
function redirectToLogin() {
    if (typeof window === 'undefined')
        return;
    const { pathname, search, hash } = window.location;
    if (pathname === '/login')
        return;
    const redirectPath = `${pathname}${search}${hash}` || '/';
    const target = `/login?redirect=${encodeURIComponent(redirectPath)}`;
    window.location.replace(target);
}
export async function loginWithEmailQuick(email, password) {
    const { data } = await api.post(TOKEN_URL, { email, password });
    if (data?.access) {
        setTokens(data.access, data?.refresh);
        api.defaults.headers.Authorization = `Bearer ${data.access}`;
    }
    return data;
}
export function logout() {
    clearTokens();
}
export async function getMe() {
    const { data } = await api.get('/api/auth/me/');
    return data;
}
export async function updateProfileNames(first_name, last_name) {
    const { data } = await api.patch('/api/auth/me/', { first_name, last_name });
    return data;
}
export async function listDispatch() {
    const { data } = await api.get('/api/dispatch/');
    return data;
}
export async function createDispatch(payload) {
    const { data } = await api.post('/api/dispatch/', payload);
    return data;
}
export async function updateDispatch(id, payload) {
    const { data } = await api.patch(`/api/dispatch/${id}/`, payload);
    return data;
}
export async function deleteDispatch(id) {
    await api.delete(`/api/dispatch/${id}/`);
}
