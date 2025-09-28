<template>
  <div class="min-h-screen bg-slate-900 text-white">
    <main class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
      <!-- Card “Acerca de nosotros” -->
      <section class="rounded-2xl border border-white/10 bg-slate-900/60 backdrop-blur p-6 md:p-8 shadow-xl">
        <div class="grid grid-cols-1 md:grid-cols-5 gap-6 md:gap-8 items-start">
          <!-- Imagen -->
          <div class="md:col-span-2">
            <img
              src="/generico1.jpg"
              alt="Tienda iEssence"
              class="w-full h-56 md:h-72 object-cover rounded-xl shadow-lg"
            />
          </div>
          <!-- Texto -->
          <div class="md:col-span-3">
            <h2 class="text-2xl md:text-3xl font-semibold tracking-tight">Acerca de Nosotros</h2>
            <p class="mt-3 text-slate-300 leading-relaxed">
              Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor.
              Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus
              mus. Donec quam felis.
            </p>
            <!-- CTA opcional -->
            <div class="mt-5 flex flex-wrap gap-3">
              <router-link
                to="/carrito"
                class="inline-flex items-center px-4 py-2 rounded-xl bg-gradient-to-r from-fuchsia-500 to-indigo-500 hover:opacity-95 focus:outline-none focus:ring-2 focus:ring-white/40"
              >
                Ver productos
              </router-link>
              <router-link
                to="/"
                class="inline-flex items-center px-4 py-2 rounded-xl border border-white/20 hover:bg-white/10 focus:outline-none focus:ring-2 focus:ring-white/40"
              >
                Ir al inicio
              </router-link>
            </div>
          </div>
        </div>
      </section>

      <!-- Card de contacto -->
      <section class="mt-8 grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="rounded-2xl border border-white/10 bg-slate-900/60 backdrop-blur p-6 shadow-xl lg:col-span-2">
          <h3 class="text-xl font-semibold">Contáctanos</h3>
          <div class="mt-4 space-y-3">
            <div class="flex items-center gap-3">
              <span class="text-2xl leading-none">📍</span>
              <span class="text-slate-300">Ubicación.....</span>
            </div>
            <div class="flex items-center gap-6 flex-wrap">
              <div class="flex items-center gap-2">
                <span class="text-xl leading-none">📞</span>
                <span class="text-slate-300">Teléfono</span>
              </div>
              <div class="flex items-center gap-2">
                <span class="text-xl leading-none">✉️</span>
                <span class="text-slate-300">Correo</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Bloque extra (opcional: horario, mapa, redes) -->
        <div class="rounded-2xl border border-white/10 bg-slate-900/60 backdrop-blur p-6 shadow-xl">
          <h3 class="text-xl font-semibold">Horario</h3>
          <ul class="mt-4 space-y-1 text-slate-300">
            <li>Lun–Vie: 09:00–18:00</li>
            <li>Sábados: 10:00–14:00</li>
            <li>Domingo: Cerrado</li>
          </ul>
        </div>
      </section>
    </main>
  </div>
</template>
