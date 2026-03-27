<template>
  <div class="min-h-screen bg-primary-50 flex flex-col justify-center px-6 selection:bg-primary-200">
    <div class="w-full max-w-sm mx-auto">
      
      <div class="text-center mb-10">
        <router-link to="/" class="inline-flex w-16 h-16 rounded-2xl bg-white shadow-card items-center justify-center text-4xl mb-4 hover:scale-105 transition-transform">♻️</router-link>
        <h1 class="text-3xl font-extrabold text-gray-900 tracking-tight">Sign In</h1>
        <p class="mt-2 text-sm text-gray-500 font-medium">Welcome back to TrashTreasure</p>
      </div>

      <div class="card-lg shadow-primary-500/10 border border-primary-100">
        <div v-if="error" class="mb-4 text-xs font-semibold text-red-600 bg-red-50 p-3 rounded-lg border border-red-100 flex items-center gap-2">
          <span>⚠️</span> {{ error }}
        </div>

        <form @submit.prevent="handleLogin">
          <div class="space-y-4">
            <div>
              <label class="label mb-2 text-primary-900">Email Address</label>
              <div class="relative flex items-center">
                <span class="absolute left-4 text-gray-400">✉️</span>
                <input 
                  v-model="email" 
                  type="email" 
                  class="input pl-12 font-semibold shadow-inner bg-gray-50/50" 
                  placeholder="you@example.com" 
                  required 
                  autofocus
                >
              </div>
            </div>

            <div>
              <label class="label mb-2 text-primary-900">Password</label>
              <div class="relative flex items-center">
                <span class="absolute left-4 text-gray-400">🔒</span>
                <input 
                  v-model="password" 
                  :type="showPassword ? 'text' : 'password'"
                  class="input pl-12 pr-12 font-semibold shadow-inner bg-gray-50/50"
                  placeholder="Your password"
                  required
                >
                <button type="button" @click="showPassword = !showPassword" class="absolute right-4 text-gray-400 hover:text-gray-600 text-sm">
                  {{ showPassword ? '🙈' : '👁️' }}
                </button>
              </div>
            </div>
          </div>

          <button type="submit" class="btn-primary w-full mt-6 py-3.5 text-base shadow-lg shadow-primary-500/20" :disabled="loading">
            <span v-if="loading" class="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin inline-block"></span>
            <span v-else>Sign In</span>
          </button>
        </form>

        <p class="text-center text-sm text-gray-500 mt-5 font-medium">
          New here? 
          <router-link to="/register" class="text-primary-600 font-bold hover:underline ml-1">Create account</router-link>
        </p>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const showPassword = ref(false)
const loading = ref(false)
const error = ref(null)

async function handleLogin() {
  loading.value = true
  error.value = null
  try {
    const data = await authStore.login(email.value, password.value)
    if (data.user?.role === 'admin') router.push('/admin/dashboard')
    else router.push('/dashboard')
  } catch (e) {
    error.value = e.response?.data?.error || 'Login failed. Please check your credentials.'
  } finally {
    loading.value = false
  }
}
</script>
