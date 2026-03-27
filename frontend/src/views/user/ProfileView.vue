<template>
  <div class="bg-gray-50 min-h-screen pb-safe">
    <div class="bg-primary-600 text-white px-4 pt-12 pb-16 sticky top-0 rounded-b-[40px] shadow-lg shadow-primary-600/10">
      <div class="flex items-center justify-between">
        <button @click="$router.push('/dashboard')" class="p-2 -ml-2 text-primary-100 hover:text-white rounded-full transition-colors">
          <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 19l-7-7 7-7" /></svg>
        </button>
        <span class="text-sm font-semibold tracking-wide uppercase text-primary-200">Profile</span>
        <div class="w-10"></div>
      </div>
    </div>

    <div class="px-5 -mt-10 relative z-10 max-w-5xl w-full mx-auto">
      <div class="bg-white rounded-3xl p-6 shadow-card mb-6 flex flex-col items-center">
        <div class="w-24 h-24 bg-primary-100 text-primary-700 rounded-full flex items-center justify-center text-4xl font-bold mb-4 shadow-inner ring-4 ring-white">
          {{ avatarChar }}
        </div>
        
        <div class="w-full bg-green-50 rounded-2xl p-4 mb-6 text-center border border-green-100">
          <p class="text-[10px] font-bold text-green-700 uppercase tracking-widest mb-1">Total Earnings</p>
          <p class="text-3xl font-extrabold text-green-600">₹{{ (authStore.user?.total_earnings || 0).toFixed(0) }}</p>
        </div>
        
        <form @submit.prevent="saveProfile" class="w-full animate-fadeInUp">
          <div class="mb-4">
            <label class="label">Full Name</label>
            <input v-model="form.name" type="text" class="input bg-gray-50 border-gray-100 focus:bg-white" placeholder="Enter your name" required>
          </div>
          
          <div class="mb-6">
            <label class="label">Email Address <span class="text-[10px] text-gray-400 tracking-normal ml-1">(Verified)</span></label>
            <input :value="form.email" type="email" class="input bg-gray-100 text-gray-500 border-transparent cursor-not-allowed" disabled>
          </div>

          <button type="submit" class="btn-primary w-full py-3.5 shadow-md shadow-primary-500/20" :disabled="loading">
             {{ loading ? 'Saving...' : 'Save Changes' }}
          </button>
        </form>
      </div>

      <div class="bg-white rounded-3xl overflow-hidden shadow-card border border-gray-50 animate-fadeInUp">
        <button @click="logout" class="w-full flex items-center justify-between p-5 text-red-600 hover:bg-red-50 transition-colors font-semibold">
          <span class="flex items-center gap-3">
             <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg>
             Log Out
          </span>
          <svg class="w-5 h-5 opacity-50" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
        </button>
      </div>
      
      <p class="text-center text-xs text-gray-400 mt-8 font-medium">TrashTreasure App v1.0.0</p>
    </div>

    <BottomNav />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import BottomNav from '../../components/ui/BottomNav.vue'

const router = useRouter()
const authStore = useAuthStore()

const loading = ref(false)
const form = ref({
  name: authStore.user?.name || '',
  email: authStore.user?.email || ''
})

const avatarChar = computed(() => {
  return form.value.name ? form.value.name.charAt(0).toUpperCase() : '👤'
})

async function saveProfile() {
  loading.value = true
  try {
    await authStore.updateProfile({ name: form.value.name })
    alert('Profile saved!')
  } catch (e) {
    alert('Failed to save profile')
  } finally {
    loading.value = false
  }
}

function logout() {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.pb-safe { padding-bottom: env(safe-area-inset-bottom, 5rem); }
</style>
