<template>
  <div>
    <div class="mb-8 flex items-end justify-between">
      <div>
        <h1 class="text-3xl font-extrabold text-gray-900 tracking-tight">Dashboard Overview</h1>
        <p class="text-gray-500 mt-2 font-medium">Real-time platform metrics</p>
      </div>
      <button @click="fetchStats" class="btn-outline btn-sm bg-white" :class="{ 'animate-pulse': loading }">
         <svg class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" /></svg>
         Refresh
      </button>
    </div>

    <div v-if="loading && !stats" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div v-for="i in 4" :key="i" class="h-32 bg-gray-200 animate-pulse rounded-2xl"></div>
    </div>

    <div v-if="stats" class="space-y-8 animate-fadeInUp">
      <!-- Top level metrics -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard title="Total Entries" :value="stats.total_entries" icon="📦" color="bg-blue-500" />
        <StatCard title="Registered Users" :value="stats.total_users" icon="👥" color="bg-indigo-500" />
        <StatCard title="Pending Review" :value="stats.pending + stats.under_verification" icon="🔍" color="bg-amber-500" />
        <StatCard title="Successfully Completed" :value="stats.completed" icon="✅" color="bg-emerald-500" />
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
        <StatCard title="Total Earnings" :value="`₹${(stats.total_earnings || 0).toFixed(0)}`" icon="💰" color="bg-green-600" />
        <StatCard title="Rejected" :value="stats.rejected" icon="❌" color="bg-red-400" />
      </div>

      <!-- Funnel Metrics -->
      <div>
        <h3 class="text-lg font-bold text-gray-800 mb-4">Verification Funnel</h3>
        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 flex flex-col xl:flex-row gap-4 divide-y xl:divide-y-0 xl:divide-x divide-gray-100">
          <div class="flex-1 py-4 xl:py-0 xl:px-4 text-center">
            <p class="text-[11px] font-bold text-gray-400 uppercase tracking-widest mb-2">New/Under Review</p>
            <p class="text-3xl font-extrabold text-amber-600">{{ stats.pending + stats.under_verification }}</p>
          </div>
          <div class="flex-1 py-4 xl:py-0 xl:px-4 text-center">
            <p class="text-[11px] font-bold text-gray-400 uppercase tracking-widest mb-2">Verified (Need Loc)</p>
            <p class="text-3xl font-extrabold text-green-500">{{ stats.verified }}</p>
          </div>
          <div class="flex-1 py-4 xl:py-0 xl:px-4 text-center">
            <p class="text-[11px] font-bold text-gray-400 uppercase tracking-widest mb-2">Confirmed (Need Slot)</p>
            <p class="text-3xl font-extrabold text-teal-600">{{ stats.confirmed || 0 }}</p>
          </div>
          <div class="flex-1 py-4 xl:py-0 xl:px-4 text-center">
            <p class="text-[11px] font-bold text-gray-400 uppercase tracking-widest mb-2">Scheduled (Pickup)</p>
            <p class="text-3xl font-extrabold text-purple-600">{{ stats.scheduled }}</p>
          </div>
          <div class="flex-1 py-4 xl:py-0 xl:px-4 text-center">
             <p class="text-[11px] font-bold text-gray-400 uppercase tracking-widest mb-2">Rejected</p>
             <p class="text-3xl font-extrabold text-red-500">{{ stats.rejected }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api'

const stats = ref(null)
const loading = ref(true)

const StatCard = {
  template: `
    <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-5 flex items-center gap-4 hover:-translate-y-1 hover:shadow-md transition-all">
      <div :class="[color, 'w-14 h-14 rounded-full flex items-center justify-center text-white text-2xl shadow-sm']">{{icon}}</div>
      <div>
        <p class="text-xs font-bold text-gray-500 uppercase tracking-wide mb-1">{{title}}</p>
        <p class="text-3xl font-extrabold text-gray-900 leading-tight">{{value}}</p>
      </div>
    </div>
  `,
  props: ['title', 'value', 'icon', 'color']
}

async function fetchStats() {
  loading.value = true
  try {
    const { data } = await api.get('/api/admin/dashboard')
    stats.value = data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchStats()
})
</script>
