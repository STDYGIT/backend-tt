<template>
  <button 
    class="flex flex-col items-center justify-center p-4 bg-white rounded-2xl shadow-card hover:shadow-card-lg hover:-translate-y-1 transition-all group"
    @click="$emit('click')"
  >
    <div class="w-12 h-12 rounded-full flex items-center justify-center text-2xl mb-2 transition-transform group-hover:scale-110" :style="{ backgroundColor: category.color + '20' }">
      {{ category.icon }}
    </div>
    <span class="text-xs font-semibold text-gray-700 text-center">{{ category.name }}</span>
  </button>
</template>

<script setup>
defineProps({ category: Object })
defineEmits(['click'])
</script>
