<template>
  <div class="min-h-screen bg-white">
    <!-- Nav -->
    <nav class="fixed top-0 w-full z-50 bg-white/80 backdrop-blur-md border-b border-gray-100 px-6 py-4 flex items-center justify-between">
      <div class="flex items-center gap-2">
        <span class="text-2xl">♻️</span>
        <span class="font-extrabold text-gray-900 text-lg tracking-tight">TrashTreasure</span>
      </div>
      <div class="flex items-center gap-3">
        <router-link to="/login" class="text-sm font-semibold text-gray-600 hover:text-gray-900 transition-colors px-4 py-2 rounded-xl hover:bg-gray-100">Login</router-link>
        <router-link to="/register" class="text-sm font-bold text-white bg-green-600 hover:bg-green-700 transition-colors px-5 py-2.5 rounded-xl shadow-sm shadow-green-200">Get Started</router-link>
      </div>
    </nav>

    <!-- Hero -->
    <section class="pt-32 pb-24 px-6 text-center bg-gradient-to-b from-green-50 to-white relative overflow-hidden">
      <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-green-100/60 via-transparent to-transparent pointer-events-none"></div>
      <div class="relative max-w-3xl mx-auto">
        <div class="inline-flex items-center gap-2 bg-green-100 text-green-800 text-xs font-bold px-4 py-2 rounded-full mb-6 border border-green-200">
          <span>🌱</span> Sustainable Recycling Platform
        </div>
        <h1 class="text-5xl md:text-6xl font-extrabold text-gray-900 leading-tight tracking-tight mb-6">
          From <span class="text-transparent bg-clip-text bg-gradient-to-r from-green-500 to-emerald-600">Trash</span><br>to <span class="text-transparent bg-clip-text bg-gradient-to-r from-green-500 to-emerald-600">Treasure</span>
        </h1>
        <p class="text-xl text-gray-500 max-w-xl mx-auto font-medium leading-relaxed mb-10">
          List your recyclable waste, get it verified, schedule a free pickup, and earn cash — all in one place.
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <router-link to="/register" class="inline-flex items-center justify-center gap-2 bg-green-600 hover:bg-green-700 text-white font-bold px-8 py-4 rounded-2xl text-base shadow-lg shadow-green-200 transition-all hover:-translate-y-0.5">
            Start Recycling <span>→</span>
          </router-link>
          <router-link to="/login" class="inline-flex items-center justify-center gap-2 bg-white border-2 border-gray-200 hover:border-gray-300 text-gray-700 font-bold px-8 py-4 rounded-2xl text-base transition-all hover:-translate-y-0.5">
            Sign In
          </router-link>
        </div>
      </div>
      <!-- Floating cards -->
      <div class="relative max-w-2xl mx-auto mt-16 grid grid-cols-3 gap-4">
        <div v-for="item in floatingItems" :key="item.label" class="bg-white rounded-2xl p-4 shadow-md border border-gray-100 text-center hover:-translate-y-1 transition-transform">
          <div class="text-3xl mb-2">{{ item.icon }}</div>
          <p class="text-xs font-bold text-gray-600">{{ item.label }}</p>
        </div>
      </div>
    </section>

    <!-- How It Works -->
    <section class="py-24 px-6 bg-white">
      <div class="max-w-4xl mx-auto text-center mb-12">
        <h2 class="text-3xl font-extrabold text-gray-900 mb-3">How It Works</h2>
        <p class="text-gray-500 font-medium">Four simple steps to turn your waste into value</p>
      </div>
      <div class="max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-6">
        <div v-for="(step, i) in steps" :key="i" class="relative text-center group">
          <div class="w-16 h-16 bg-gradient-to-br from-green-400 to-emerald-600 rounded-2xl flex items-center justify-center text-2xl mx-auto mb-4 shadow-lg shadow-green-200 group-hover:-translate-y-1 transition-transform">
            {{ step.icon }}
          </div>
          <div class="absolute top-8 left-[calc(50%+2rem)] w-[calc(100%-4rem)] h-0.5 bg-gradient-to-r from-green-200 to-transparent hidden md:block last:hidden"></div>
          <div class="inline-flex w-6 h-6 bg-green-100 text-green-700 text-xs font-bold rounded-full items-center justify-center mb-3">{{ i + 1 }}</div>
          <h3 class="font-bold text-gray-900 mb-1">{{ step.title }}</h3>
          <p class="text-sm text-gray-500 font-medium leading-relaxed">{{ step.desc }}</p>
        </div>
      </div>
    </section>

    <!-- Impact -->
    <section class="py-24 px-6 bg-gradient-to-br from-green-600 to-emerald-700 text-white">
      <div class="max-w-4xl mx-auto text-center">
        <h2 class="text-3xl font-extrabold mb-4">Making a Real Impact</h2>
        <p class="text-green-100 font-medium max-w-xl mx-auto mb-12 text-lg leading-relaxed">
          Every item you recycle helps reduce landfill waste, lower carbon emissions, and build a cleaner tomorrow.
        </p>
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-6">
          <div v-for="stat in impactStats" :key="stat.label" class="bg-white/10 backdrop-blur-sm border border-white/20 rounded-2xl p-6 hover:bg-white/20 transition-colors">
            <div class="text-4xl font-extrabold mb-2">{{ stat.value }}</div>
            <p class="text-green-100 text-sm font-semibold">{{ stat.label }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="py-24 px-6 bg-gray-50 text-center">
      <div class="max-w-xl mx-auto">
        <div class="text-5xl mb-6">🌍</div>
        <h2 class="text-3xl font-extrabold text-gray-900 mb-4">Ready to make a difference?</h2>
        <p class="text-gray-500 font-medium mb-8">Join thousands of eco-conscious citizens turning waste into earnings.</p>
        <router-link to="/register" class="inline-flex items-center gap-2 bg-green-600 hover:bg-green-700 text-white font-bold px-10 py-4 rounded-2xl text-lg shadow-lg shadow-green-200 transition-all hover:-translate-y-0.5">
          Get Started — It's Free <span>✨</span>
        </router-link>
      </div>
    </section>

    <!-- Footer -->
    <footer class="py-8 px-6 border-t border-gray-100 text-center text-sm text-gray-400">
      <p>© 2026 TrashTreasure · Built for a cleaner planet ♻️</p>
    </footer>
  </div>
</template>

<script setup>
const floatingItems = [
  { icon: '📦', label: 'Upload Waste' },
  { icon: '✅', label: 'Get Verified' },
  { icon: '💰', label: 'Earn Cash' },
]

const steps = [
  { icon: '📸', title: 'Upload Waste', desc: 'Take a photo and submit your recyclable item with details.' },
  { icon: '🔍', title: 'Verification', desc: 'Our team reviews and verifies your waste submission.' },
  { icon: '🚐', title: 'Pickup', desc: 'Schedule a free pickup at your doorstep.' },
  { icon: '♻️', title: 'Recycling', desc: 'Your waste is recycled and you earn cash rewards.' },
]

const impactStats = [
  { value: '500+', label: 'Items Recycled' },
  { value: '200kg', label: 'CO₂ Saved' },
  { value: '₹25K+', label: 'Paid to Users' },
]
</script>
