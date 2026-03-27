<template>
  <div class="relative pl-6 py-4">
    <div class="absolute left-[11px] top-6 bottom-6 w-0.5 bg-gray-100 rounded-full"></div>
    
    <div class="space-y-6">
      <div v-for="(step, i) in steps" :key="i" class="relative group">
        <!-- Dot -->
        <div class="absolute -left-[31px] top-1 mt-0.5 pointer-events-none">
          <div :class="[
            'w-4 h-4 rounded-full ring-4 ring-white shadow-sm flex items-center justify-center transition-all duration-300',
            step.active ? 'bg-primary-500 scale-125' : (step.done ? 'bg-primary-500' : 'bg-gray-200')
          ]">
            <div v-if="step.active" class="w-2 h-2 bg-white rounded-full"></div>
          </div>
          <!-- Pulse for active step -->
          <div v-if="step.active" class="absolute inset-0 bg-primary-500 rounded-full -z-10 animate-pulse-ring"></div>
        </div>

        <div :class="['transition-colors duration-200', step.done || step.active ? 'text-gray-900' : 'text-gray-400']">
          <h4 class="text-sm font-bold flex items-center gap-2">
            {{ step.title }}
            <span v-if="step.date" class="font-normal text-[10px] text-gray-400 mt-0.5">{{ formatDate(step.date) }}</span>
          </h4>
          <p class="text-xs leading-relaxed mt-1" :class="step.active ? 'text-gray-600' : 'text-gray-400'">
            {{ step.desc }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({ entry: Object })

const STATUS_ORDER = [
  'pending', 
  'under_verification', 
  'verified',
  'location_required',
  'confirmed', 
  'scheduled', 
  'completed'
]

const steps = computed(() => {
  if (!props.entry) return []
  const { status, created_at, updated_at, pickup } = props.entry
  
  if (status === 'rejected') {
    return [
      { id: 'pending', title: 'Request Received', done: true, date: created_at, desc: 'We got your waste entry.' },
      { id: 'rejected', title: 'Rejected', active: true, date: updated_at, desc: 'This entry does not meet our guidelines.' },
    ]
  }

  const currentIdx = STATUS_ORDER.indexOf(status)
  
  return [
    { 
      id: 'pending', 
      title: 'Request Received', 
      done: currentIdx > 0, 
      active: currentIdx === 0,
      date: created_at,
      desc: 'We got your request and are reviewing it.'
    },
    { 
      id: 'verified', 
      title: 'Verified', 
      done: currentIdx > 2, 
      active: currentIdx === 1 || currentIdx === 2,
      date: currentIdx >= 2 ? updated_at : null,
      desc: 'Our team verified the waste.'
    },
    { 
      id: 'confirmed', 
      title: 'Location & Slot Booking', 
      done: currentIdx > 4, 
      active: currentIdx === 3 || currentIdx === 4,
      date: currentIdx >= 4 ? updated_at : null,
      desc: 'Add location and pick a time slot.'
    },
    { 
      id: 'scheduled', 
      title: 'Pickup Scheduled', 
      done: currentIdx > 5, 
      active: currentIdx === 5,
      date: pickup?.assigned_at,
      desc: pickup ? `Agent will arrive: ${pickup.slot.date} (${pickup.slot.time_range})` : 'Awaiting agent.'
    },
    { 
      id: 'completed', 
      title: 'Collected!', 
      done: currentIdx === 6, 
      active: currentIdx === 6,
      desc: 'Waste sent to recycling center.'
    }
  ]
})

function formatDate(iso) {
  if (!iso) return ''
  return new Date(iso).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', hour: '2-digit', minute:'2-digit' })
}
</script>
