<template>
  <div>
    <div class="mb-6 flex items-center justify-between">
      <div class="flex items-center gap-4">
        <router-link to="/admin/entries" class="p-2 bg-white border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" /></svg>
        </router-link>
        <div>
          <h1 class="text-2xl font-extrabold text-gray-900 tracking-tight">Entry #{{ entry?.id }}</h1>
          <p class="text-gray-500 text-sm font-medium mt-0.5">Verification & Management</p>
        </div>
      </div>
      <StatusBadge v-if="entry" :status="entry.status" class="px-3 py-1.5 shadow-sm bg-white border border-gray-100" />
    </div>

    <div v-if="loading" class="flex justify-center p-12">
      <div class="w-8 h-8 border-4 border-primary-200 border-t-primary-600 rounded-full animate-spin"></div>
    </div>

    <div v-else-if="entry" class="grid grid-cols-1 lg:grid-cols-3 gap-6 animate-fadeInUp">
      
      <!-- Main Info -->
      <div class="lg:col-span-2 space-y-6">
        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
          <div class="bg-gray-50 p-4 border-b border-gray-100 flex items-center gap-4">
            <div class="w-12 h-12 rounded-xl bg-white shadow-sm flex items-center justify-center text-2xl">
              {{ entry.category?.icon || '♻️' }}
            </div>
            <div>
              <h2 class="text-lg font-bold text-gray-900">{{ entry.category?.name }}</h2>
              <p class="text-sm text-gray-500 font-medium">{{ entry.subtype?.name || 'No setup' }}</p>
            </div>
          </div>
          
          <div class="relative group">
            <img v-if="entry.image_url" :src="imgSrc" class="w-full h-80 object-cover" />
            <div v-if="entry.image_url" class="absolute inset-x-0 bottom-0 p-4 bg-gradient-to-t from-black/60 to-transparent flex justify-end">
              <a :href="imgSrc" target="_blank" class="btn-sm bg-white text-gray-900 border-none shadow-md hover:bg-gray-50 flex items-center gap-2">
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" /></svg>
                Open Full Image
              </a>
            </div>
          </div>
          <div class="p-6 grid grid-cols-2 gap-y-6 gap-x-8">
            <div class="col-span-2">
              <label class="label">User Details</label>
              <div class="flex items-center gap-3 mt-2">
                <div class="w-10 h-10 rounded-full bg-primary-100 text-primary-700 flex flex-col items-center justify-center font-bold text-lg">
                  {{ entry.user_name ? entry.user_name.charAt(0).toUpperCase() : 'U' }}
                </div>
                <div>
                  <p class="font-semibold text-gray-900">{{ entry.user_name || 'Anonymous' }}</p>
                  <p class="text-sm text-gray-500">{{ entry.user_phone }}</p>
                </div>
              </div>
            </div>

            <div class="col-span-2">
              <label class="label">Description provided</label>
              <p class="text-sm text-gray-800 bg-gray-50 p-4 rounded-xl border border-gray-100 whitespace-pre-wrap">{{ entry.description || 'No description provided.' }}</p>
            </div>

            <div>
              <label class="label">Condition</label>
              <p class="text-sm font-semibold text-gray-900">{{ entry.condition || 'N/A' }}</p>
            </div>
            
            <div>
              <label class="label">Age/Usage</label>
              <p class="text-sm font-semibold text-gray-900">{{ entry.age_usage || 'N/A' }}</p>
            </div>
            
            <div class="col-span-2" v-if="entry.location_address">
              <label class="label">Pickup Location</label>
              <div class="flex items-start gap-2 bg-blue-50 border border-blue-100 p-4 rounded-xl text-blue-900 text-sm mt-1">
                <span class="text-lg">📍</span> 
                <div>
                  <p class="font-semibold mb-1">Confirmed Address:</p>
                  <p>{{ entry.location_address }}</p>
                  <p v-if="entry.location_lat" class="text-[10px] font-mono mt-2 opacity-70">
                    Lat: {{ entry.location_lat }}, Lng: {{ entry.location_lng }}
                  </p>
                </div>
              </div>
            </div>
            
            <div class="col-span-2" v-if="entry.pickup">
              <label class="label">Scheduled Pickup</label>
              <div class="flex items-center gap-3 bg-purple-50 border border-purple-100 p-4 rounded-xl text-purple-900 text-sm mt-1">
                <span class="text-2xl">📅</span>
                <div>
                  <p class="font-bold">{{ entry.pickup.slot?.date }}</p>
                  <p>{{ entry.pickup.slot?.time_range }} — {{ entry.pickup.slot?.zone_name }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Admin Actions Sidebar -->
      <div class="space-y-6">
        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-5">
          <h3 class="font-bold text-gray-900 mb-4 border-b border-gray-100 pb-3">Update Status</h3>
          
          <div class="space-y-3">
            <label class="flex items-center gap-3 p-3 border rounded-xl cursor-pointer hover:bg-gray-50 transition-colors" :class="updateData.status === 'under_verification' ? 'border-blue-500 bg-blue-50' : 'border-gray-200'">
              <input type="radio" v-model="updateData.status" value="under_verification" class="text-blue-600 focus:ring-blue-500 h-4 w-4">
              <span class="text-sm font-semibold text-gray-900">🔍 Under Review</span>
            </label>
            
            <label class="flex items-center gap-3 p-3 border rounded-xl cursor-pointer hover:bg-gray-50 transition-colors" :class="updateData.status === 'location_required' ? 'border-orange-500 bg-orange-50' : 'border-gray-200'">
              <input type="radio" v-model="updateData.status" value="location_required" class="text-orange-600 focus:ring-orange-500 h-4 w-4">
              <span class="text-sm font-semibold text-gray-900">📍 Verified (Need Loc)</span>
            </label>
            
            <label class="flex items-center gap-3 p-3 border rounded-xl cursor-pointer hover:bg-gray-50 transition-colors" :class="updateData.status === 'completed' ? 'border-green-500 bg-green-50' : 'border-gray-200'">
              <input type="radio" v-model="updateData.status" value="completed" class="text-green-600 focus:ring-green-500 h-4 w-4">
              <span class="text-sm font-semibold text-gray-900">🚚 Completed</span>
            </label>

            <label class="flex items-center gap-3 p-3 border rounded-xl cursor-pointer hover:bg-gray-50 transition-colors" :class="updateData.status === 'rejected' ? 'border-red-500 bg-red-50' : 'border-gray-200'">
              <input type="radio" v-model="updateData.status" value="rejected" class="text-red-600 focus:ring-red-500 h-4 w-4">
              <span class="text-sm font-semibold text-gray-900">❌ Rejected</span>
            </label>
          </div>

          <div class="mt-4 mb-4">
            <label class="label">Admin Notes (Optional)</label>
            <textarea v-model="updateData.admin_notes" rows="3" class="textarea text-sm" placeholder="Internal notes…"></textarea>
          </div>

          <!-- Pricing -->
          <div class="mb-5 bg-green-50 border border-green-200 rounded-xl p-4">
            <h4 class="text-xs font-bold text-green-800 uppercase tracking-wider mb-3">💰 Set Price (Cash Payment)</h4>
            <div class="space-y-3">
              <div>
                <label class="label text-xs mb-1">Amount (₹)</label>
                <input v-model.number="updateData.price" type="number" min="0" step="0.01" class="input text-sm py-2" placeholder="e.g. 50">
              </div>
              <div>
                <label class="label text-xs mb-1">Pricing Type</label>
                <select v-model="updateData.price_type" class="input text-sm py-2">
                  <option value="">— Select type —</option>
                  <option value="per_item">Per Item</option>
                  <option value="per_image">Per Image</option>
                </select>
              </div>
            </div>
          </div>

          <button @click="saveStatus" class="btn-primary w-full shadow-sm py-3" :disabled="saving">
            {{ saving ? 'Saving...' : 'Update Entry' }}
          </button>
        </div>

        <div class="bg-gray-100 rounded-2xl p-5 border border-dashed border-gray-200">
          <h4 class="text-xs font-bold text-gray-500 uppercase tracking-widest mb-3">Timeline Logs</h4>
          <div class="space-y-3 relative before:absolute before:inset-0 before:ml-1.5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-gray-300 before:to-transparent">
             <div class="text-xs text-gray-600 relative z-10 pl-6 border-l-2 border-gray-300 pb-3">
               <span class="font-semibold text-gray-900 block mb-0.5">Created</span>
               {{ new Date(entry.created_at).toLocaleString() }}
             </div>
             <div class="text-xs text-gray-600 relative z-10 pl-6 border-l-2 border-gray-300">
               <span class="font-semibold text-gray-900 block mb-0.5">Last Updated</span>
               {{ new Date(entry.updated_at).toLocaleString() }}
             </div>
          </div>
        </div>
      </div>
      
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../../api'
import StatusBadge from '../../components/ui/StatusBadge.vue'

const route = useRoute()
const entry = ref(null)
const loading = ref(true)
const saving = ref(false)

const updateData = ref({
  status: '',
  admin_notes: '',
  price: null,
  price_type: ''
})

const imgSrc = computed(() => {
  const url = entry.value?.image_url
  if (!url) return ''
  return url.startsWith('http') ? url : `${import.meta.env.VITE_API_URL || 'http://localhost:5001'}${url}`
})

async function fetchEntry() {
  loading.value = true
  try {
    const { data } = await api.get(`/api/entries/${route.params.id}`)
    entry.value = data
    updateData.value.status = data.status
    updateData.value.admin_notes = data.admin_notes || ''
    updateData.value.price = data.price || null
    updateData.value.price_type = data.price_type || ''
  } catch (e) {
    alert('Failed to load entry')
  } finally {
    loading.value = false
  }
}

onMounted(() => fetchEntry())

async function saveStatus() {
  saving.value = true
  try {
    const { data } = await api.put(`/api/admin/entries/${entry.value.id}/status`, updateData.value)
    entry.value = data
    alert('Entry updated successfully')
  } catch (e) {
    alert(e.response?.data?.error || 'Failed to update entry')
  } finally {
    saving.value = false
  }
}
</script>
