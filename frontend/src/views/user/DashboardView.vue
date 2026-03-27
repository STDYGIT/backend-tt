<template>
  <div class="pb-24 bg-gray-50 min-h-screen">
    <!-- Header -->
    <header class="bg-primary-600 text-white rounded-b-3xl px-6 pt-12 pb-8 shadow-lg shadow-primary-600/20 sticky top-0 z-10">
      <div class="flex justify-between items-center mb-6">
        <div>
          <p class="text-primary-100 text-sm font-medium mb-0.5">Welcome back,</p>
          <h1 class="text-2xl font-bold tracking-tight">{{ authStore.user?.name || 'User' }}</h1>
        </div>
        <router-link to="/profile" class="w-11 h-11 bg-white/10 rounded-full flex items-center justify-center border border-white/20 backdrop-blur-sm shadow-sm hover:bg-white/20 transition-colors">
          <span class="text-lg">👤</span>
        </router-link>
      </div>

      <div class="bg-white/10 p-4 rounded-2xl border border-white/20 backdrop-blur-sm flex items-center gap-4">
        <div class="flex-1">
          <h3 class="font-semibold text-lg">Turn waste into worth</h3>
          <p class="text-xs text-primary-100 mt-1 font-medium leading-relaxed">List your recyclables and schedule a free pickup today.</p>
        </div>
        <div class="w-16 h-16 bg-white rounded-xl shadow-inner flex items-center justify-center flex-shrink-0 -rotate-3 hover:rotate-3 transition-transform">
          <span class="text-3xl">🌱</span>
        </div>
      </div>
    </header>

    <!-- Categories Grid -->
    <main class="px-5 mt-8 max-w-5xl w-full mx-auto">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-lg font-bold text-gray-900 tracking-tight">What do you want to recycle?</h2>
      </div>

      <div v-if="categoriesStore.loading" class="grid grid-cols-4 gap-3">
        <div v-for="i in 8" :key="i" class="h-24 bg-gray-200 animate-pulse rounded-2xl"></div>
      </div>
      
      <div v-else class="grid grid-cols-4 gap-x-3 gap-y-4">
        <CategoryCard 
          v-for="cat in categoriesStore.categories" 
          :key="cat.id" 
          :category="cat"
          @click="selectCategory(cat)"
        />
      </div>

      <!-- Earnings Summary -->
      <div v-if="authStore.user?.total_earnings > 0" class="mt-8 mb-2 bg-gradient-to-r from-green-50 to-emerald-50 border border-green-200 rounded-2xl p-5 flex items-center justify-between shadow-sm">
        <div>
          <p class="text-[10px] font-bold text-green-700 uppercase tracking-widest mb-1">Total Cash Earned</p>
          <p class="text-3xl font-extrabold text-green-600 tracking-tight">₹{{ (authStore.user.total_earnings || 0).toFixed(0) }}</p>
        </div>
        <div class="w-12 h-12 bg-white rounded-xl shadow-sm border border-green-100 text-2xl flex items-center justify-center">💰</div>
      </div>

      <!-- Recent Entries widget -->
       <div class="mt-6 mb-4 flex items-center justify-between">
        <h2 class="text-lg font-bold text-gray-900 tracking-tight">Recent Activity</h2>
        <router-link to="/my-entries" class="text-xs font-semibold text-primary-600 hover:text-primary-700 hover:underline">View All</router-link>
      </div>

      <div v-if="entriesStore.loading" class="space-y-3">
        <div class="h-20 bg-gray-200 animate-pulse rounded-2xl"></div>
        <div class="h-20 bg-gray-200 animate-pulse rounded-2xl"></div>
      </div>
      
      <div v-else-if="recentEntries.length" class="space-y-3">
        <EntryCard 
          v-for="entry in recentEntries" 
          :key="entry.id" 
          :entry="entry"
          @click="router.push(`/entry/${entry.id}`)"
        />
      </div>

      <div v-else class="card p-6 text-center shadow-sm border border-dashed border-gray-200 mt-2">
        <div class="text-3xl mb-3 opacity-80">📦</div>
        <p class="text-sm font-semibold text-gray-700">No recent activity</p>
        <p class="text-xs text-gray-500 mt-1 mb-4">You haven't listed any waste yet.</p>
        <router-link to="/submit" class="btn-primary text-xs py-2 px-5 inline-flex">List Item Now</router-link>
      </div>
    </main>

    <BottomNav />
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import { useCategoriesStore } from '../../stores/categories'
import { useEntriesStore } from '../../stores/entries'
import CategoryCard from '../../components/ui/CategoryCard.vue'
import EntryCard from '../../components/ui/EntryCard.vue'
import BottomNav from '../../components/ui/BottomNav.vue'

const router = useRouter()
const authStore = useAuthStore()
const categoriesStore = useCategoriesStore()
const entriesStore = useEntriesStore()

onMounted(() => {
  categoriesStore.fetch()
  entriesStore.fetchAll()
})

const recentEntries = computed(() => {
  return entriesStore.entries.slice(0, 3)
})

function selectCategory(cat) {
  router.push({ path: '/submit', query: { category_id: cat.id } })
}
</script>
