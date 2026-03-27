<template>
  <div class="bg-gray-50 min-h-screen pb-safe">
    <!-- Header -->
    <div class="bg-white px-4 pt-12 pb-4 shadow-sm sticky top-0 z-20 flex items-center justify-between">
      <button @click="$router.push('/my-entries')" class="p-2 -ml-2 text-gray-600 hover:bg-gray-100 rounded-full transition-colors">
        <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 19l-7-7 7-7" /></svg>
      </button>
      <h1 class="text-lg font-bold tracking-tight text-gray-900">Request Details</h1>
      <div class="w-10"></div>
    </div>

    <div v-if="loading" class="flex justify-center p-12">
      <div class="w-8 h-8 border-4 border-primary-200 border-t-primary-600 rounded-full animate-spin"></div>
    </div>

    <main v-else-if="entry" class="px-5 mt-4 max-w-5xl w-full mx-auto stagger pb-8">
      
      <!-- Key Status Banner -->
      <div class="bg-white rounded-2xl p-5 shadow-sm border border-gray-100 mb-6 flex flex-col items-center text-center animate-fadeInUp">
        <div class="w-16 h-16 rounded-full flex items-center justify-center text-3xl mb-3 shadow-[0_0_20px_rgba(0,0,0,0.05)] bg-gray-50">
          {{ entry.category?.icon || '♻️' }}
        </div>
        <h2 class="text-xl font-bold tracking-tight">{{ entry.category?.name }} <span v-if="entry.subtype" class="text-gray-500 font-normal"> · {{ entry.subtype.name }}</span></h2>
        <StatusBadge :status="entry.status" class="mt-3 text-sm px-3 py-1 shadow-sm" />
      </div>

      <!-- Timeline -->
      <div class="bg-white rounded-2xl p-5 shadow-sm border border-gray-100 mb-6 animate-fadeInUp">
        <h3 class="font-bold text-gray-900 mb-2">Track Status</h3>
        <WasteTimeline :entry="entry" />
      </div>

      <!-- Action Required Panels -->
      <div class="space-y-4 mb-6 animate-fadeInUp">
        <!-- Add Location Action -->
        <div v-if="entry.status === 'location_required'" class="bg-orange-50 rounded-2xl p-5 border border-orange-200">
          <div class="flex items-start gap-3">
            <span class="text-2xl mt-0.5">📍</span>
            <div>
              <h4 class="font-bold text-orange-900 mb-1">Location Required</h4>
              <p class="text-sm text-orange-800 mb-4">Your request is verified! Now, please provide the pickup location so we can schedule an agent.</p>
              <button @click="showLocationPrompt = true" class="btn bg-orange-500 hover:bg-orange-600 text-white w-full py-3 shadow-sm">
                Add Pickup Location
              </button>
            </div>
          </div>
        </div>

        <!-- Schedule Pickup Action -->
        <div v-if="entry.status === 'confirmed'" class="bg-primary-50 rounded-2xl p-5 border border-primary-100">
           <div class="flex items-start gap-3 mb-4">
            <span class="text-2xl mt-0.5">📅</span>
            <div>
              <h4 class="font-bold text-primary-900 mb-1">Schedule Pickup</h4>
              <p class="text-sm text-primary-800">Choose a convenient time slot for the pickup agent to arrive.</p>
            </div>
          </div>
          <SlotPicker :entryId="entry.id" @schedule="handleSchedule" />
        </div>
      </div>

      <!-- Details Card -->
      <div class="bg-white rounded-2xl overflow-hidden shadow-sm border border-gray-100 animate-fadeInUp">
        <img v-if="entry.image_url" :src="imgSrc" class="w-full h-48 object-cover border-b border-gray-100" />
        <div class="p-5 space-y-4">
          <h3 class="font-bold text-gray-900 text-base">Item Information</h3>
          
          <div v-if="entry.description">
            <p class="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1">Description</p>
            <p class="text-sm text-gray-700 bg-gray-50 p-3 rounded-xl border border-gray-100">{{ entry.description }}</p>
          </div>
          
          <div class="grid grid-cols-2 gap-4 pt-2">
            <div v-if="entry.condition">
              <p class="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1">Condition</p>
              <p class="text-sm font-semibold text-gray-800">{{ entry.condition }}</p>
            </div>
            <div v-if="entry.age_usage">
              <p class="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1">Age/Usage</p>
              <p class="text-sm font-semibold text-gray-800">{{ entry.age_usage }}</p>
            </div>
          </div>

          <div v-if="entry.location_address" class="pt-4 border-t border-gray-100 mt-4">
             <p class="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1">Pickup Address</p>
             <p class="text-sm text-gray-700 flex items-start gap-2">
               <span class="mt-0.5 text-gray-400">📍</span>
               {{ entry.location_address }}
             </p>
          </div>
          
          <div class="pt-4 border-t border-gray-100 mt-4">
            <p class="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1">Submitted On</p>
            <p class="text-xs text-gray-500 font-medium">{{ formatDate(entry.created_at) }}</p>
          </div>
        </div>
      </div>
    </main>

    <LocationPrompt 
      v-if="showLocationPrompt" 
      :show="showLocationPrompt"
      @close="showLocationPrompt = false" 
      @save="handleLocationSave" 
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useEntriesStore } from '../../stores/entries'
import StatusBadge from '../../components/ui/StatusBadge.vue'
import WasteTimeline from '../../components/WasteTimeline.vue'
import LocationPrompt from '../../components/LocationPrompt.vue'
import SlotPicker from '../../components/SlotPicker.vue'

const route = useRoute()
const entriesStore = useEntriesStore()

const loading = ref(true)
const showLocationPrompt = ref(false)

onMounted(async () => {
  try {
    await entriesStore.fetchOne(route.params.id)
  } catch (e) {
    alert('Entry not found')
  } finally {
    loading.value = false
  }
})

const entry = computed(() => entriesStore.currentEntry)
const imgSrc = computed(() => {
  const url = entry.value?.image_url
  if (!url) return ''
  return url.startsWith('http') ? url : `${import.meta.env.VITE_API_URL || 'http://localhost:5001'}${url}`
})

async function handleLocationSave(payload) {
  loading.value = true
  try {
    await entriesStore.saveLocation(entry.value.id, payload)
    showLocationPrompt.value = false
  } catch (e) {
    alert('Failed to save location')
  } finally {
    loading.value = false
  }
}

async function handleSchedule(slotId) {
  loading.value = true
  try {
    await entriesStore.schedulePickup(entry.value.id, slotId)
  } catch (e) {
    alert(e.response?.data?.error || 'Failed to schedule pickup')
  } finally {
    loading.value = false
  }
}

function formatDate(iso) {
  if (!iso) return ''
  return new Date(iso).toLocaleString('en-IN', { 
    day: 'numeric', month: 'short', year: 'numeric', h: '2-digit', minute:'2-digit' 
  })
}
</script>
