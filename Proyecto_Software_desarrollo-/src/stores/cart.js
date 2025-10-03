import { defineStore } from 'pinia';
import { api } from '@/lib/api';
function parseSummary(summary) {
    const totalQuantity = summary?.total_quantity ?? 0;
    const totalAmount = summary?.total_amount ? Number(summary.total_amount) : 0;
    return {
        totalQuantity,
        totalAmount,
    };
}
export const useCart = defineStore('cart', {
    state: () => ({
        items: [],
        summary: { totalQuantity: 0, totalAmount: 0 },
        loading: false,
        error: null,
        isLoaded: false,
    }),
    getters: {
        totalCount: (state) => state.summary.totalQuantity,
        totalAmount: (state) => state.summary.totalAmount,
    },
    actions: {
        applyPayload(payload) {
            this.items = Array.isArray(payload.items) ? payload.items : [];
            this.summary = parseSummary(payload.summary);
            this.isLoaded = true;
        },
        reset() {
            this.items = [];
            this.summary = { totalQuantity: 0, totalAmount: 0 };
            this.loading = false;
            this.error = null;
            this.isLoaded = false;
        },
        async fetchCart() {
            this.loading = true;
            this.error = null;
            try {
                const { data } = await api.get('/api/cart/');
                this.applyPayload(data);
            }
            catch (error) {
                if (error?.response?.status === 401) {
                    this.reset();
                    return;
                }
                this.error = error?.response?.data?.detail ?? 'No se pudo cargar el carrito';
            }
            finally {
                this.loading = false;
            }
        },
        async addToCart(productId, quantity = 1) {
            this.error = null;
            try {
                const { data } = await api.post('/api/cart/', {
                    product_id: productId,
                    quantity,
                });
                this.applyPayload(data);
            }
            catch (error) {
                this.error = error?.response?.data?.detail ?? 'No se pudo agregar al carrito';
                throw error;
            }
        },
        async updateQuantity(productId, quantity) {
            if (quantity < 0)
                quantity = 0;
            try {
                const pathId = encodeURIComponent(String(productId));
                const { data } = await api.patch(`/api/cart/${pathId}/`, { quantity });
                this.applyPayload(data);
            }
            catch (error) {
                this.error = error?.response?.data?.detail ?? 'No se pudo actualizar la cantidad';
                throw error;
            }
        },
        async removeItem(productId) {
            try {
                const pathId = encodeURIComponent(String(productId));
                const { data } = await api.delete(`/api/cart/${pathId}/`);
                this.applyPayload(data);
            }
            catch (error) {
                this.error = error?.response?.data?.detail ?? 'No se pudo eliminar el producto';
                throw error;
            }
        },
    },
});
