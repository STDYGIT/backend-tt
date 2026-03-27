<template>
  <div>
    <div class="mb-8 flex items-end justify-between">
      <div>
        <h1 class="text-3xl font-extrabold text-gray-900 tracking-tight">User Management</h1>
        <p class="text-gray-500 mt-2 font-medium">{{ users.length }} registered users</p>
      </div>
      <button @click="fetchUsers" class="btn-outline btn-sm bg-white" :class="{ 'animate-pulse': loading }">
        <svg class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" /></svg>
        Refresh
      </button>
    </div>

    <div v-if="loading" class="space-y-3">
      <div v-for="i in 5" :key="i" class="h-16 bg-gray-200 animate-pulse rounded-2xl"></div>
    </div>

    <!-- Search Bar -->
    <div class="mb-6">
      <div class="relative max-w-md">
        <span class="absolute inset-y-0 left-4 text-gray-400 flex items-center">🔍</span>
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="Search users by name or email..." 
          class="input pl-11 shadow-sm w-full bg-white border-gray-200"
        >
      </div>
    </div>

    <!-- Admins Section -->
    <div v-if="adminUsers.length > 0" class="mb-8">
      <h2 class="text-lg font-bold text-gray-900 mb-4 px-1 flex items-center gap-2">

        Administrators ({{ adminUsers.length }})
      </h2>
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-x-auto">
        <table class="w-full text-sm min-w-[800px]">
          <thead>
            <tr class="border-b border-gray-100 bg-gray-50">
              <th class="text-left px-6 py-4 text-xs font-bold text-gray-500 uppercase tracking-wider">Admin</th>
              <th class="text-left px-6 py-4 text-xs font-bold text-gray-500 uppercase tracking-wider">Entries Reviewed</th>
              <th class="text-left px-6 py-4 text-xs font-bold text-gray-500 uppercase tracking-wider">Joined</th>
              <th class="text-right px-6 py-4 text-xs font-bold text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-50">
            <tr v-for="u in adminUsers" :key="u.id" class="hover:bg-gray-50/50 transition-colors group">
              <td class="px-6 py-4">
                <div class="flex items-center gap-3">
                  <div class="w-9 h-9 rounded-full bg-purple-100 text-purple-700 flex items-center justify-center font-bold text-sm flex-shrink-0">
                    {{ (u.name || u.email).charAt(0).toUpperCase() }}
                  </div>
                  <div>
                    <p class="font-semibold text-gray-900">{{ u.name || 'No name' }}</p>
                    <p class="text-xs text-gray-400">{{ u.email }}</p>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 font-semibold text-gray-700">{{ u.reviewed_count || 0 }}</td>
              <td class="px-6 py-4 text-gray-400 text-xs">{{ new Date(u.created_at).toLocaleDateString() }}</td>
              <td class="px-6 py-4">
                <div class="flex items-center justify-end gap-2">
                  <router-link :to="`/admin/users/${u.id}`" class="btn-outline btn-sm text-xs px-3 py-1.5">View</router-link>
                  <button @click="toggleRole(u)" class="btn-sm text-xs px-3 py-1.5 bg-gray-50 hover:bg-gray-100 text-gray-600 border border-gray-200 rounded-lg font-semibold transition-colors">
                    ↓ Demote
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Normal Users Section -->
    <div>
      <h2 class="text-lg font-bold text-gray-900 mb-4 px-1 flex items-center gap-2">
        Normal Users ({{ normalUsers.length }})
      </h2>
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-x-auto">
        <table class="w-full text-sm min-w-[800px]">
          <thead>
            <tr class="border-b border-gray-100 bg-gray-50">
              <th class="text-left px-6 py-4 text-xs font-bold text-gray-500 uppercase tracking-wider">User</th>
              <th class="text-left px-6 py-4 text-xs font-bold text-gray-500 uppercase tracking-wider">Entries</th>
              <th class="text-left px-6 py-4 text-xs font-bold text-gray-500 uppercase tracking-wider">Earnings</th>
              <th class="text-left px-6 py-4 text-xs font-bold text-gray-500 uppercase tracking-wider">Joined</th>
              <th class="text-right px-6 py-4 text-xs font-bold text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-50">
            <tr v-for="u in normalUsers" :key="u.id" class="hover:bg-gray-50/50 transition-colors group">
              <td class="px-6 py-4">
                <div class="flex items-center gap-3">
                  <div class="w-9 h-9 rounded-full bg-green-100 text-green-700 flex items-center justify-center font-bold text-sm flex-shrink-0">
                    {{ (u.name || u.email).charAt(0).toUpperCase() }}
                  </div>
                  <div>
                    <p class="font-semibold text-gray-900">{{ u.name || 'No name' }}</p>
                    <p class="text-xs text-gray-400">{{ u.email }}</p>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 font-semibold text-gray-700">{{ u.entries_count || 0 }}</td>
              <td class="px-6 py-4 font-semibold text-green-700">₹{{ (u.total_earnings || 0).toFixed(0) }}</td>
              <td class="px-6 py-4 text-gray-400 text-xs">{{ new Date(u.created_at).toLocaleDateString() }}</td>
              <td class="px-6 py-4">
                <div class="flex items-center justify-end gap-2">
                  <router-link :to="`/admin/users/${u.id}`" class="btn-outline btn-sm text-xs px-3 py-1.5">View</router-link>
                  <button @click="toggleRole(u)" class="btn-sm text-xs px-3 py-1.5 bg-purple-50 hover:bg-purple-100 text-purple-700 border border-purple-200 rounded-lg font-semibold transition-colors">
                    ↑ Promote
                  </button>
                  <button @click="confirmDelete(u)" class="btn-sm text-xs px-3 py-1.5 bg-red-50 hover:bg-red-100 text-red-600 border border-red-200 rounded-lg font-semibold transition-colors">
                    Delete
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="!normalUsers.length">
              <td colspan="5" class="px-6 py-12 text-center text-gray-400 font-medium">No normal users found</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../../api'

const users = ref([])
const loading = ref(true)
const searchQuery = ref('')

const filteredUsers = computed(() => {
  if (!searchQuery.value) return users.value
  const q = searchQuery.value.toLowerCase()
  return users.value.filter(u => 
    (u.name && u.name.toLowerCase().includes(q)) || 
    (u.email && u.email.toLowerCase().includes(q))
  )
})

const adminUsers = computed(() => filteredUsers.value.filter(u => u.role === 'admin'))
const normalUsers = computed(() => filteredUsers.value.filter(u => u.role === 'user'))

async function fetchUsers() {
  loading.value = true
  try {
    const { data } = await api.get('/api/admin/users')
    users.value = data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function toggleRole(u) {
  const action = u.role === 'admin' ? 'demote to user' : 'promote to admin'
  if (!confirm(`Are you sure you want to ${action} ${u.email}?`)) return
  try {
    const { data } = await api.put(`/api/admin/users/${u.id}/promote`)
    u.role = data.user.role
  } catch (e) {
    alert(e.response?.data?.error || 'Failed to update role')
  }
}

async function confirmDelete(u) {
  if (!confirm(`Permanently delete ${u.email} and all their data?`)) return
  try {
    await api.delete(`/api/admin/users/${u.id}`)
    users.value = users.value.filter(x => x.id !== u.id)
  } catch (e) {
    alert(e.response?.data?.error || 'Failed to delete user')
  }
}

onMounted(fetchUsers)
</script>
