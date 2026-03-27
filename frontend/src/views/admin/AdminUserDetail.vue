<template>
  <div>
    <!-- Back + Header -->
    <div class="mb-6 flex items-center gap-4">
      <router-link to="/admin/users" class="p-2 bg-white border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" /></svg>
      </router-link>
      <div>
        <h1 class="text-2xl font-extrabold text-gray-900 tracking-tight">{{ user?.name || user?.email || 'User Detail' }}</h1>
        <p class="text-gray-500 text-sm font-medium mt-0.5">{{ user?.email }}</p>
      </div>
    </div>

    <div v-if="loading" class="flex justify-center p-12">
      <div class="w-8 h-8 border-4 border-primary-200 border-t-primary-600 rounded-full animate-spin"></div>
    </div>

    <div v-else-if="user" class="space-y-6 animate-fadeInUp">
      <!-- User Stats -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4" v-if="user.role === 'user'">
        <div class="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm text-center">
          <p class="text-3xl font-extrabold text-gray-900">{{ displayEntries?.length || 0 }}</p>
          <p class="text-xs font-bold text-gray-400 uppercase tracking-wider mt-1">Total Submissions</p>
        </div>
        <div class="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm text-center">
          <p class="text-3xl font-extrabold text-green-600">₹{{ (user.total_earnings || 0).toFixed(0) }}</p>
          <p class="text-xs font-bold text-gray-400 uppercase tracking-wider mt-1">Total Earned</p>
        </div>
        <div class="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm text-center">
          <p class="text-3xl font-extrabold text-blue-600">{{ completedCount }}</p>
          <p class="text-xs font-bold text-gray-400 uppercase tracking-wider mt-1">Completed</p>
        </div>
        <div class="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm text-center">
          <p class="text-3xl font-extrabold text-amber-600">{{ pendingCount }}</p>
          <p class="text-xs font-bold text-gray-400 uppercase tracking-wider mt-1">Pending</p>
        </div>
      </div>
      
      <!-- Admin Stats -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4" v-else>
        <div class="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm text-center">
          <p class="text-3xl font-extrabold text-purple-600">{{ displayEntries?.length || 0 }}</p>
          <p class="text-xs font-bold text-gray-400 uppercase tracking-wider mt-1">Entries Reviewed</p>
        </div>
      </div>

      <!-- User Info Card -->
      <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-6 flex items-center gap-5">
        <div class="w-16 h-16 rounded-2xl bg-primary-100 text-primary-700 flex items-center justify-center font-extrabold text-2xl flex-shrink-0">
          {{ (user.name || user.email).charAt(0).toUpperCase() }}
        </div>
        <div class="flex-1">
          <p class="font-bold text-gray-900 text-lg">{{ user.name || 'No name set' }}</p>
          <p class="text-gray-500 text-sm">{{ user.email }}</p>
          <div class="flex items-center gap-3 mt-2">
            <span :class="['text-xs font-bold px-3 py-1 rounded-full', user.role === 'admin' ? 'bg-purple-100 text-purple-700' : 'bg-green-100 text-green-700']">{{ user.role }}</span>
            <span :class="['text-xs font-bold px-3 py-1 rounded-full', user.is_verified ? 'bg-blue-100 text-blue-700' : 'bg-gray-100 text-gray-500']">{{ user.is_verified ? '✓ Verified' : 'Unverified' }}</span>
          </div>
        </div>
        <div class="flex gap-2">
          <button @click="toggleRole" class="btn-sm text-xs px-4 py-2 bg-purple-50 hover:bg-purple-100 text-purple-700 border border-purple-200 rounded-xl font-semibold transition-colors">
            {{ user.role === 'admin' ? '↓ Demote' : '↑ Make Admin' }}
          </button>
        </div>
      </div>

      <!-- Submissions -->
      <div>
        <h3 class="text-lg font-bold text-gray-900 mb-4">{{ user.role === 'admin' ? 'Reviewed History' : 'Submissions' }}</h3>
        <div class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-x-auto">
          <table class="w-full text-sm min-w-[700px]">
            <thead>
              <tr class="border-b border-gray-100 bg-gray-50">
                <th class="text-left px-5 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Item</th>
                <th class="text-left px-5 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Status</th>
                <th class="text-left px-5 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Price</th>
                <th class="text-left px-5 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Pickup</th>
                <th class="text-left px-5 py-3 text-xs font-bold text-gray-500 uppercase tracking-wider">Date</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-50">
              <tr v-for="entry in displayEntries" :key="entry.id" class="hover:bg-gray-50/50 transition-colors">
                <td class="px-5 py-3">
                  <div class="flex items-center gap-2">
                    <span class="text-lg">{{ entry.category?.icon || '♻️' }}</span>
                    <div>
                      <p class="font-semibold text-gray-900">{{ entry.category?.name }}</p>
                      <p class="text-xs text-gray-400">{{ entry.subtype?.name || entry.subtype_other || 'N/A' }}</p>
                    </div>
                  </div>
                </td>
                <td class="px-5 py-3">
                  <span :class="statusClass(entry.status)" class="text-xs font-bold px-2.5 py-1 rounded-full">{{ entry.status.replace(/_/g,' ') }}</span>
                </td>
                <td class="px-5 py-3 font-semibold text-green-700">{{ entry.price ? `₹${entry.price}` : '—' }}</td>
                <td class="px-5 py-3 text-gray-500 text-xs">{{ entry.pickup?.slot?.date || '—' }}</td>
                <td class="px-5 py-3 text-gray-400 text-xs">{{ new Date(entry.updated_at || entry.created_at).toLocaleDateString() }}</td>
              </tr>
              <tr v-if="!displayEntries?.length">
                <td colspan="5" class="px-5 py-8 text-center text-gray-400 font-medium">No records yet</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../../api'

const route = useRoute()
const user = ref(null)
const loading = ref(true)

const displayEntries = computed(() => user.value?.role === 'admin' ? user.value?.reviewed_entries : user.value?.entries)
const completedCount = computed(() => displayEntries.value?.filter(e => e.status === 'completed').length || 0)
const pendingCount = computed(() => displayEntries.value?.filter(e => ['pending', 'under_verification'].includes(e.status)).length || 0)

function statusClass(status) {
  const map = {
    pending: 'bg-amber-100 text-amber-700',
    under_verification: 'bg-blue-100 text-blue-700',
    verified: 'bg-teal-100 text-teal-700',
    location_required: 'bg-orange-100 text-orange-700',
    confirmed: 'bg-cyan-100 text-cyan-700',
    scheduled: 'bg-purple-100 text-purple-700',
    completed: 'bg-green-100 text-green-700',
    rejected: 'bg-red-100 text-red-700',
  }
  return map[status] || 'bg-gray-100 text-gray-600'
}

async function fetchUser() {
  loading.value = true
  try {
    const { data } = await api.get(`/api/admin/users/${route.params.id}`)
    user.value = data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function toggleRole() {
  const action = user.value.role === 'admin' ? 'demote to user' : 'promote to admin'
  if (!confirm(`${action} ${user.value.email}?`)) return
  try {
    const { data } = await api.put(`/api/admin/users/${user.value.id}/promote`)
    user.value.role = data.user.role
  } catch (e) {
    alert(e.response?.data?.error || 'Failed to update role')
  }
}

onMounted(fetchUser)
</script>
