<template>
  <div>
    <div class="mb-8 flex flex-col sm:flex-row sm:items-end justify-between gap-4">
      <div>
        <h1 class="text-3xl font-extrabold text-gray-900 tracking-tight">Pickup Logistics</h1>
        <p class="text-gray-500 mt-2 font-medium">Manage areas and available times for waste collection</p>
      </div>
      
      <div class="flex bg-gray-100 p-1 rounded-xl">
        <button @click="tab = 'zones'" :class="tab === 'zones' ? 'bg-white shadow-sm text-gray-900' : 'text-gray-500 hover:text-gray-700'" class="px-6 py-2 rounded-lg text-sm font-bold transition-all">Zones</button>
        <button @click="tab = 'slots'" :class="tab === 'slots' ? 'bg-white shadow-sm text-gray-900' : 'text-gray-500 hover:text-gray-700'" class="px-6 py-2 rounded-lg text-sm font-bold transition-all">Schedules</button>
      </div>
    </div>

    <!-- Zones Tab -->
    <div v-if="tab === 'zones'">
       <div class="mb-6 pb-6 border-b border-gray-200">
         <h3 class="text-lg font-bold text-gray-800 mb-4">Add New Zone</h3>
         <form @submit.prevent="createZone" class="flex flex-col sm:flex-row gap-4 items-end">
           <div class="flex-1 w-full">
             <label class="label">Zone Name</label>
             <input v-model="zoneForm.name" type="text" class="input py-2.5" placeholder="e.g. North Area" required>
           </div>
           <div class="flex-2 w-full sm:w-1/2">
             <label class="label">Description</label>
             <input v-model="zoneForm.description" type="text" class="input py-2.5" placeholder="Which areas are covered?">
           </div>
           <button class="btn-primary py-2.5 px-6 whitespace-nowrap" :disabled="saving">Create Zone</button>
         </form>
       </div>

       <div v-if="loading" class="space-y-3"><div v-for="i in 3" :key="i" class="h-16 bg-gray-200 animate-pulse rounded-xl"></div></div>
       
       <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 stagger">
          <div v-for="z in zones" :key="z.id" class="bg-white p-5 rounded-2xl shadow-sm border border-gray-100 flex flex-col justify-between animate-fadeInUp hover:shadow-md transition-shadow">
             <div>
                <h4 class="font-bold text-lg text-gray-900 mb-1 flex items-center justify-between">
                  {{ z.name }}
                  <span class="text-xs px-2 py-0.5 rounded bg-gray-100 text-gray-500 font-mono">ID: {{z.id}}</span>
                </h4>
                <p class="text-sm text-gray-600 mb-4 line-clamp-2 h-10">{{ z.description || 'No description' }}</p>
             </div>
             <div>
                <button v-if="z.is_active" @click="toggleZone(z)" class="text-xs font-bold text-red-500 bg-red-50 hover:bg-red-100 px-3 py-1.5 rounded transition-colors w-full">Deactivate</button>
                <button v-else @click="toggleZone(z)" class="text-xs font-bold text-primary-600 bg-primary-50 hover:bg-primary-100 px-3 py-1.5 rounded transition-colors w-full">Activate</button>
             </div>
          </div>
       </div>
    </div>

    <!-- Slots Tab -->
    <div v-else>
       <div class="mb-6 pb-6 border-b border-gray-200">
         <h3 class="text-lg font-bold text-gray-800 mb-4">Schedule Next Week's Slots</h3>
         <form @submit.prevent="createSlot" class="grid grid-cols-1 sm:grid-cols-4 gap-4 items-end">
           <div>
             <label class="label">Zone</label>
             <select v-model="slotForm.zone_id" class="input py-2.5 bg-white" required>
               <option value="" disabled>Select Zone...</option>
               <option v-for="z in zones.filter(x=>x.is_active)" :key="z.id" :value="z.id">{{ z.name }}</option>
             </select>
           </div>
           <div>
             <label class="label">Date</label>
             <input v-model="slotForm.date" type="date" class="input py-2.5 bg-white" required>
           </div>
           <div>
             <label class="label">Time Range</label>
             <input v-model="slotForm.time_range" type="text" class="input py-2.5" placeholder="e.g. 9 AM - 12 PM" required>
           </div>
           <div>
             <label class="label">Capacity</label>
             <input v-model.number="slotForm.capacity" type="number" class="input py-2.5" min="1" required>
           </div>
           <div class="sm:col-span-4 mt-2">
             <button class="btn-primary w-full sm:w-auto px-8" :disabled="saving">Create Slot</button>
           </div>
         </form>
       </div>

       <div v-if="loading" class="space-y-3"><div v-for="i in 5" :key="i" class="h-12 bg-gray-200 animate-pulse rounded-xl"></div></div>

       <div class="overflow-hidden bg-white rounded-2xl shadow-sm border border-gray-100">
          <table class="w-full text-left border-collapse text-sm">
            <thead>
              <tr class="bg-gray-50/80 uppercase tracking-wider text-[11px] font-bold text-gray-500 border-b border-gray-100">
                <th class="px-6 py-3 border-r border-gray-100 w-1/4">Date</th>
                <th class="px-6 py-3 w-1/4">Time</th>
                <th class="px-6 py-3 w-1/4">Zone</th>
                <th class="px-6 py-3 flex-1">Capacity/Booked</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
              <tr v-for="s in slots" :key="s.id" class="hover:bg-gray-50/50" :class="!s.is_active || s.available===0 ? 'opacity-50 blur-[0.5px] hover:blur-none transition-all' : ''">
                 <td class="px-6 py-3 font-semibold font-mono border-r border-gray-100">{{ s.date }}</td>
                 <td class="px-6 py-3 text-gray-800">{{ s.time_range }}</td>
                 <td class="px-6 py-3 text-gray-600 font-medium">{{ s.zone_name }}</td>
                 <td class="px-6 py-3">
                    <div class="flex items-center justify-between">
                      <div class="flex items-center gap-2">
                         <div class="w-16 h-2 bg-gray-100 rounded-full overflow-hidden">
                           <div class="h-full bg-primary-500" :style="{width: (s.booked_count / s.capacity)*100 + '%'}"></div>
                         </div>
                         <span class="text-xs font-bold text-gray-600">{{s.booked_count}} / {{s.capacity}}</span>
                      </div>
                      <button v-if="s.is_active" @click="deleteSlot(s.id)" class="text-gray-400 hover:text-red-500 font-bold p-1">&times;</button>
                      <span v-else class="text-[10px] text-red-500 font-bold uppercase">Inactive</span>
                    </div>
                 </td>
              </tr>
              <tr v-if="slots.length === 0">
                 <td colspan="4" class="px-6 py-8 text-center text-gray-500">No upcoming slots scheduled.</td>
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

const tab = ref('zones')
const zones = ref([])
const slots = ref([])
const loading = ref(true)
const saving = ref(false)

const zoneForm = ref({ name: '', description: '' })
const slotForm = ref({ zone_id: '', date: '', time_range: '', capacity: 15 })

async function fetchAll() {
  loading.value = true
  try {
    const [zRes, sRes] = await Promise.all([
      api.get('/api/admin/zones'),
      api.get('/api/admin/slots')
    ])
    zones.value = zRes.data
    slots.value = sRes.data
  } catch(e) { console.error(e) }
  finally { loading.value = false }
}

onMounted(() => fetchAll())

async function createZone() {
  saving.value = true
  api.post('/api/admin/zones', zoneForm.value).then(() => {
    zoneForm.value = { name:'', description:'' }
    fetchAll()
  }).finally(() => saving.value = false)
}

async function toggleZone(z) {
  api.put(`/api/admin/zones/${z.id}`, { is_active: !z.is_active }).then(()=>fetchAll())
}

async function createSlot() {
  saving.value = true
  api.post('/api/admin/slots', slotForm.value).then(() => {
    slotForm.value.time_range = ''
    fetchAll()
  }).finally(() => saving.value = false)
}

async function deleteSlot(id) {
  if(!confirm('Deactivate slot?')) return
  api.delete(`/api/admin/slots/${id}`).then(()=>fetchAll())
}
</script>
