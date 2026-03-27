<template>
  <div>
    <div class="mb-8 flex flex-col sm:flex-row sm:items-end justify-between gap-4">
      <div>
        <h1 class="text-3xl font-extrabold text-gray-900 tracking-tight">Waste Entries</h1>
        <p class="text-gray-500 mt-2 font-medium">Manage and verify user scrap submissions</p>
      </div>
      
      <div class="flex items-center gap-3">
        <select v-model="statusFilter" @change="fetchEntries" class="input bg-white w-full sm:w-48 py-2.5">
          <option value="">All Statuses</option>
          <option value="pending">🟡 Pending</option>
          <option value="under_verification">🔍 Under Review</option>
          <option value="verified">✅ Verified</option>
          <option value="location_required">📍 Need Location</option>
          <option value="confirmed">✔️ Confirmed</option>
          <option value="scheduled">📅 Scheduled</option>
          <option value="completed">🚚 Completed</option>
          <option value="rejected">❌ Rejected</option>
        </select>
        <button @click="fetchEntries" class="btn-primary py-2.5 px-4"><svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" /></svg></button>
      </div>
    </div>

    <div v-if="loading" class="space-y-4">
      <div v-for="i in 5" :key="i" class="h-20 bg-gray-200 animate-pulse rounded-2xl"></div>
    </div>

    <div v-else-if="entries.length === 0" class="card p-12 text-center text-gray-500 shadow-sm border border-dashed border-gray-200">
      <div class="text-5xl mb-4 opacity-70 flex justify-center">📭</div>
      <p class="font-semibold text-lg text-gray-700">No entries found</p>
      <p class="text-sm mt-1">Try changing the status filter.</p>
    </div>

    <div v-else class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden text-sm">
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse min-w-[800px]">
          <thead>
            <tr class="bg-gray-50/80 border-b border-gray-100 uppercase tracking-wider text-[11px] font-bold text-gray-500">
              <th class="px-6 py-4">ID / Date</th>
              <th class="px-6 py-4">User</th>
              <th class="px-6 py-4">Category</th>
              <th class="px-6 py-4">Location</th>
              <th class="px-6 py-4">Status</th>
              <th class="px-6 py-4 text-right">Action</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-for="entry in entries" :key="entry.id" class="hover:bg-gray-50 transition-colors group">
              <td class="px-6 py-4">
                <p class="font-mono font-bold text-gray-900 mb-1">#{{ entry.id }}</p>
                <p class="text-[11px] text-gray-500">{{ formatDate(entry.created_at) }}</p>
              </td>
              <td class="px-6 py-4">
                <p class="font-semibold text-gray-800">{{ entry.user_name || 'No Name' }}</p>
                <p class="text-xs text-gray-500">{{ entry.user_phone }}</p>
              </td>
              <td class="px-6 py-4">
                <p class="font-semibold text-gray-800">{{ entry.category?.name }} <span class="text-gray-400 font-normal ml-1" v-if="entry.subtype">· {{entry.subtype.name}}</span></p>
                <p class="text-xs text-gray-500 truncate max-w-[150px]">{{ entry.description || 'No desc' }}</p>
              </td>
              <td class="px-6 py-4">
                <p v-if="entry.location_address" class="text-xs text-gray-600 truncate max-w-[150px]" :title="entry.location_address">{{ entry.location_address }}</p>
                <p v-else class="text-xs text-gray-400 italic">Not provided</p>
              </td>
              <td class="px-6 py-4">
                <StatusBadge :status="entry.status" />
              </td>
              <td class="px-6 py-4 text-right">
                <router-link :to="`/admin/entries/${entry.id}`" class="btn-outline btn-sm bg-white">
                  Review
                </router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api'
import StatusBadge from '../../components/ui/StatusBadge.vue'

const entries = ref([])
const loading = ref(true)
const statusFilter = ref('')

async function fetchEntries() {
  loading.value = true
  try {
    const url = statusFilter.value ? `/api/admin/entries?status=${statusFilter.value}` : '/api/admin/entries'
    const { data } = await api.get(url)
    entries.value = data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

onMounted(() => fetchEntries())

function formatDate(iso) {
  return new Date(iso).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year:'numeric' })
}
</script>
