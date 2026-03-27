<template>
  <div class="mt-6">
    <div v-if="loading" class="text-center py-6 text-gray-500 flex flex-col items-center">
      <div class="w-8 h-8 border-4 border-primary-200 border-t-primary-600 rounded-full animate-spin mb-3"></div>
      Loading time slots...
    </div>
    
    <div v-else-if="slots.length === 0" class="text-center py-6 text-gray-500 bg-gray-50 rounded-xl border border-dashed border-gray-200">
      No pickup slots currently available in your area. Please check back later.
    </div>
    
    <div v-else class="space-y-4">
      <h3 class="text-sm font-bold text-gray-800">Select Pickup Time</h3>
      
      <!-- Group by Date -->
      <div v-for="(daySlots, date) in groupedSlots" :key="date" class="mb-4">
        <p class="text-xs font-semibold text-gray-500 uppercase tracking-widest mb-2">{{ formatDate(date) }}</p>
        <div class="grid grid-cols-2 gap-2">
          <button 
            v-for="slot in daySlots" 
            :key="slot.id"
            @click="selectedSlot = slot.id"
            :class="[
              'p-3 rounded-xl border-2 text-sm font-semibold transition-all text-left flex flex-col',
              selectedSlot === slot.id 
                ? 'border-primary-500 bg-primary-50 text-primary-800' 
                : 'border-gray-200 bg-white hover:border-primary-300 text-gray-700'
            ]"
          >
            <span>{{ slot.time_range }}</span>
            <span :class="['text-xs font-normal mt-1', selectedSlot === slot.id ? 'text-primary-600' : 'text-gray-400']">
              {{ slot.zone_name }}
            </span>
          </button>
        </div>
      </div>
      
      <button 
        v-if="selectedSlot" 
        @click="$emit('schedule', selectedSlot)" 
        class="w-full btn-primary py-3.5 shadow-lg shadow-primary-500/20 animate-fadeInUp"
      >
        Confirm Pickup
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useEntriesStore } from '../stores/entries'

const props = defineProps({ entryId: Number })
defineEmits(['schedule'])

const entriesStore = useEntriesStore()
const slots = ref([])
const loading = ref(true)
const selectedSlot = ref(null)

onMounted(async () => {
  slots.value = await entriesStore.fetchSlots(props.entryId)
  loading.value = false
})

const groupedSlots = computed(() => {
  return slots.value.reduce((groups, slot) => {
    if (!groups[slot.date]) groups[slot.date] = []
    groups[slot.date].push(slot)
    return groups
  }, {})
})

function formatDate(dateStr) {
  const d = new Date(dateStr)
  const today = new Date()
  today.setHours(0,0,0,0)
  const compareDate = new Date(d)
  compareDate.setHours(0,0,0,0)
  
  if (compareDate.getTime() === today.getTime()) return 'Today'
  
  const tomorrow = new Date(today)
  tomorrow.setDate(tomorrow.getDate() + 1)
  if (compareDate.getTime() === tomorrow.getTime()) return 'Tomorrow'
  
  return d.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' })
}
</script>
