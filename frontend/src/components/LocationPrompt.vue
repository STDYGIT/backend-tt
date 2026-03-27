<template>
  <div v-if="show" class="fixed inset-0 z-50 flex items-end justify-center sm:items-center bg-black/40 backdrop-blur-sm animate-fadeIn" @click.self="$emit('close')">
    <div class="bg-white w-full max-w-5xl w-full rounded-t-3xl sm:rounded-3xl p-6 pb-safe animate-slideUp">
      
      <div class="flex justify-between items-center mb-6">
        <h3 class="text-xl font-bold">Add Location</h3>
        <button @click="$emit('close')" class="p-2 bg-gray-100 rounded-full text-gray-500 hover:bg-gray-200">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
        </button>
      </div>

      <div class="space-y-4">
        <button 
          @click="getCurrentLocation" 
          class="w-full flex items-center gap-3 p-4 border-2 border-primary-100 bg-primary-50 rounded-2xl text-primary-700 font-semibold hover:bg-primary-100 transition-colors"
          :disabled="loading"
        >
          <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
          {{ loading ? 'Getting location...' : 'Use Current Location' }}
        </button>

        <div class="relative flex items-center py-2">
          <div class="flex-grow border-t border-gray-200"></div>
          <span class="flex-shrink-0 mx-4 text-xs text-gray-400 font-medium tracking-wider">OR ENTER MANUALLY</span>
          <div class="flex-grow border-t border-gray-200"></div>
        </div>

        <div>
          <label class="label">Full Address</label>
          <textarea v-model="address" rows="3" class="textarea mb-4" placeholder="House/Flat No., Street, Area, City, Pincode..."></textarea>
          <button @click="save" class="btn-primary w-full py-3.5" :disabled="loading || !address.trim()">
            Confirm Address
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({ show: Boolean })
const emit = defineEmits(['close', 'save'])

const address = ref('')
const loading = ref(false)

function getCurrentLocation() {
  loading.value = true
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        // Reverse geocoding would happen here in production
        address.value = `Lat: ${pos.coords.latitude.toFixed(4)}, Lng: ${pos.coords.longitude.toFixed(4)}`
        emit('save', { lat: pos.coords.latitude, lng: pos.coords.longitude, address: 'Detected Location' })
        loading.value = false
      },
      (err) => {
        console.error(err)
        alert('Could not get location. Please type manually.')
        loading.value = false
      }
    )
  } else {
    alert('Geolocation not supported.')
    loading.value = false
  }
}

function save() {
  if (address.value.trim()) {
    emit('save', { lat: null, lng: null, address: address.value })
  }
}
</script>

<style scoped>
.pb-safe { padding-bottom: env(safe-area-inset-bottom, 1.5rem); }
.animate-fadeIn { animation: fadeIn 0.2s ease-out forwards; }
.animate-slideUp { animation: slideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes slideUp { from { transform: translateY(100%); } to { transform: translateY(0); } }
</style>
