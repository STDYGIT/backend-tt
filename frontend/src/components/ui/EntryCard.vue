<template>
  <div class="card animate-fadeInUp cursor-pointer hover:shadow-card-lg transition-shadow duration-200" @click="$emit('click')">
    <div class="flex items-start gap-3">
      <div class="w-16 h-16 rounded-xl overflow-hidden bg-gray-100 flex-shrink-0">
        <img v-if="entry.image_url" :src="imgSrc" class="w-full h-full object-cover" alt="waste" />
        <div v-else class="w-full h-full flex items-center justify-center text-2xl">
          {{ entry.category?.icon || '♻️' }}
        </div>
      </div>
      <div class="flex-1 min-w-0">
        <div class="flex items-center justify-between mb-1">
          <span class="text-sm font-semibold text-gray-800 truncate">
            {{ entry.category?.name }}
            <span v-if="entry.subtype" class="text-gray-500 font-normal"> · {{ entry.subtype.name }}</span>
          </span>
          <StatusBadge :status="entry.status" />
        </div>
        <p class="text-xs text-gray-500 line-clamp-2 mb-2">{{ entry.description || 'No description' }}</p>
        <p class="text-[11px] text-gray-400">{{ formatDate(entry.created_at) }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import StatusBadge from './StatusBadge.vue'

const props = defineProps({ entry: Object })
defineEmits(['click'])

const imgSrc = props.entry.image_url?.startsWith('http')
  ? props.entry.image_url
  : `${import.meta.env.VITE_API_URL || 'http://localhost:5001'}${props.entry.image_url}`

function formatDate(iso) {
  if (!iso) return ''
  return new Date(iso).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })
}
</script>
