<template>
  <div class="bg-gray-50 min-h-screen pb-24">
    <div class="bg-white px-5 pt-12 pb-4 shadow-sm sticky top-0 z-10">
      <h1 class="text-xl font-bold tracking-tight text-gray-900 mb-3">My Activity</h1>
      
      <!-- Filter Tabs -->
      <div class="flex gap-2 p-1 bg-gray-100 rounded-xl overflow-x-auto scrollbar-hide">
        <button v-for="t in tabs" :key="t.id" @click="activeTab = t.id"
          class="flex-1 whitespace-nowrap px-4 py-2 rounded-lg text-xs font-semibold transition-all duration-200"
          :class="activeTab === t.id ? 'bg-white text-gray-900 shadow-sm ring-1 ring-black/5' : 'text-gray-500 hover:text-gray-700'"
        >
          {{ t.label }}
        </button>
      </div>
    </div>

    <main class="px-5 mt-6 max-w-5xl w-full mx-auto">
      <div v-if="entriesStore.loading" class="space-y-4">
        <div v-for="i in 3" :key="i" class="h-28 bg-gray-200 animate-pulse rounded-2xl"></div>
      </div>
      
      <div v-else-if="filteredEntries.length === 0" class="card p-8 text-center text-gray-500 shadow-sm border border-dashed border-gray-200 mt-4 max-w-5xl w-full mx-auto">
        <div class="text-4xl mb-4 opacity-70">🏜️</div>
        <p class="font-semibold text-gray-700">No entries found</p>
        <p class="text-sm mt-1 mb-4">You have no items in this status.</p>
        <router-link to="/submit" class="btn-outline text-xs">Submit Waste</router-link>
      </div>

      <div v-else class="space-y-4 max-w-5xl w-full mx-auto stagger">
        <EntryCard 
          v-for="entry in filteredEntries" 
          :key="entry.id" 
          :entry="entry" 
          class="animate-fadeInUp"
          @click="$router.push(`/entry/${entry.id}`)"
        />
      </div>
    </main>

    <BottomNav />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useEntriesStore } from '../../stores/entries'
import EntryCard from '../../components/ui/EntryCard.vue'
import BottomNav from '../../components/ui/BottomNav.vue'

const entriesStore = useEntriesStore()
const activeTab = ref('all')

const tabs = [
  { id: 'all', label: 'All Items' },
  { id: 'active', label: 'In Progress' },
  { id: 'done', label: 'Completed' },
]

onMounted(() => {
  entriesStore.fetchAll()
})

const filteredEntries = computed(() => {
  return entriesStore.entries.filter(e => {
    if (activeTab.value === 'active') return e.status !== 'completed' && e.status !== 'rejected'
    if (activeTab.value === 'done') return e.status === 'completed' || e.status === 'rejected'
    return true
  })
})
</script>

<style scoped>
.scrollbar-hide::-webkit-scrollbar { display: none; }
.scrollbar-hide { -ms-overflow-style: none; scrollbar-width: none; }
</style>
