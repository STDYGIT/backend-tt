<template>
  <div class="min-h-screen bg-gray-50 flex relative">
    
    <!-- Mobile Backdrop -->
    <div v-if="mobileMenuOpen" @click="mobileMenuOpen = false" class="fixed inset-0 bg-black/50 z-30 md:hidden backdrop-blur-sm transition-opacity"></div>

    <!-- Sidebar / Navigation -->
    <aside :class="['w-64 bg-white border-r border-gray-200 flex flex-col flex-shrink-0 fixed md:sticky top-0 bottom-0 h-screen overflow-y-auto z-40 transition-transform duration-300 md:translate-x-0', mobileMenuOpen ? 'translate-x-0' : '-translate-x-full']">
      <div class="p-6 pb-2 border-b border-gray-100 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="text-3xl">♻️</div>
          <div>
            <h2 class="font-extrabold text-gray-900 tracking-tight leading-4">TrashTreasure</h2>
            <span class="text-[10px] font-bold text-primary-600 uppercase tracking-widest">Admin Panel</span>
          </div>
        </div>
        <button @click="mobileMenuOpen = false" class="md:hidden p-2 text-gray-500 hover:bg-gray-100 rounded-lg">
           <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
        </button>
      </div>

      <nav class="flex-1 p-4 space-y-1.5 mt-2">
        <router-link @click="mobileMenuOpen = false" to="/admin/dashboard" class="flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-semibold text-gray-600 hover:bg-gray-50 hover:text-gray-900 transition-colors" active-class="bg-primary-50 text-primary-700 hover:bg-primary-50">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" /></svg>
          Overview
        </router-link>
        <router-link @click="mobileMenuOpen = false" to="/admin/entries" class="flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-semibold text-gray-600 hover:bg-gray-50 hover:text-gray-900 transition-colors" active-class="bg-primary-50 text-primary-700 hover:bg-primary-50">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" /></svg>
          Waste Entries
        </router-link>
        <router-link @click="mobileMenuOpen = false" to="/admin/users" class="flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-semibold text-gray-600 hover:bg-gray-50 hover:text-gray-900 transition-colors" active-class="bg-primary-50 text-primary-700 hover:bg-primary-50">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
          Users
        </router-link>
        <router-link @click="mobileMenuOpen = false" to="/admin/categories" class="flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-semibold text-gray-600 hover:bg-gray-50 hover:text-gray-900 transition-colors" active-class="bg-primary-50 text-primary-700 hover:bg-primary-50">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" /></svg>
          Categories
        </router-link>
        <router-link @click="mobileMenuOpen = false" to="/admin/zones" class="flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-semibold text-gray-600 hover:bg-gray-50 hover:text-gray-900 transition-colors" active-class="bg-primary-50 text-primary-700 hover:bg-primary-50">
           <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
          Pickup Zones & Slots
        </router-link>
      </nav>

      <div class="p-4 border-t border-gray-100">
        <button @click="logout" class="flex items-center gap-3 w-full px-4 py-3 rounded-xl text-sm font-semibold text-red-600 hover:bg-red-50 transition-colors">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg>
          Sign Out
        </button>
      </div>
    </aside>

    <!-- Wrapper for Header & Content -->
    <div class="flex-1 flex flex-col min-w-0 h-screen overflow-y-auto">
      
      <!-- Mobile Header -->
      <div class="md:hidden sticky top-0 bg-white shadow-sm border-b border-gray-200 z-20 px-4 py-3 flex items-center justify-between w-full h-14 shrink-0">
         <div class="flex items-center gap-2">
           <span class="text-xl">♻️</span> <span class="font-bold">Admin</span>
         </div>
         <button @click="mobileMenuOpen = !mobileMenuOpen" class="p-2 bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors">
           <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
             <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
           </svg>
         </button>
      </div>

      <!-- Main Content -->
      <main class="flex-1 w-full flex flex-col">
        <div class="p-6 md:p-8 max-w-6xl mx-auto w-full">
          <router-view v-slot="{ Component }">
            <transition name="fade" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </div>
      </main>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const mobileMenuOpen = ref(false)

onMounted(() => {
  document.getElementById('app').classList.add('admin-layout')
})

onUnmounted(() => {
  document.getElementById('app').classList.remove('admin-layout')
})

function logout() {
  authStore.logout()
  router.push('/login')
}
</script>

<style>
/* Admin layout specific global reset */
body { background: #f8fafb; }
</style>
