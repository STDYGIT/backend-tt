<template>
  <div class="min-h-screen bg-primary-50 flex flex-col justify-center px-6 selection:bg-primary-200">
    <div class="w-full max-w-sm mx-auto">

      <div class="text-center mb-10">
        <router-link to="/" class="inline-flex w-16 h-16 rounded-2xl bg-white shadow-card items-center justify-center text-4xl mb-4 hover:scale-105 transition-transform">♻️</router-link>
        <h1 class="text-3xl font-extrabold text-gray-900 tracking-tight">Create Account</h1>
        <p class="mt-2 text-sm text-gray-500 font-medium">Join TrashTreasure and start earning</p>
      </div>

      <!-- Step Indicator -->
      <div class="flex items-center justify-center gap-2 mb-6">
        <div v-for="s in 3" :key="s" class="flex items-center gap-2">
          <div :class="['w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold transition-all', step >= s ? 'bg-primary-600 text-white' : 'bg-gray-200 text-gray-500']">{{ s }}</div>
          <div v-if="s < 3" :class="['w-10 h-1 rounded-full transition-all', step > s ? 'bg-primary-600' : 'bg-gray-200']"></div>
        </div>
      </div>

      <div class="card-lg shadow-primary-500/10 border border-primary-100">
        <div v-if="error" class="mb-4 text-xs font-semibold text-red-600 bg-red-50 p-3 rounded-lg border border-red-100 flex items-center gap-2">
          <span>⚠️</span> {{ error }}
        </div>
        <div v-if="success" class="mb-4 text-xs font-semibold text-green-700 bg-green-50 p-3 rounded-lg border border-green-100 flex items-center gap-2">
          <span>✅</span> {{ success }}
        </div>

        <!-- Step 1: Email -->
        <form v-if="step === 1" @submit.prevent="handleRequestOtp">
          <p class="text-sm font-bold text-gray-700 mb-4">Step 1: Enter your email</p>
          <div>
            <label class="label mb-2 text-primary-900">Email Address</label>
            <div class="relative flex items-center">
              <span class="absolute left-4 text-gray-400">✉️</span>
              <input v-model="email" type="email" class="input pl-12 font-semibold shadow-inner bg-gray-50/50"
                placeholder="you@example.com" required autofocus>
            </div>
          </div>
          <button type="submit" class="btn-primary w-full mt-6 py-3.5 text-base shadow-lg shadow-primary-500/20" :disabled="loading || !email.includes('@')">
            <span v-if="loading" class="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin inline-block"></span>
            <span v-else>Send Verification Code</span>
          </button>
        </form>

        <!-- Step 2: OTP -->
        <form v-else-if="step === 2" @submit.prevent="handleVerifyOtp" class="animate-fadeInUp">
          <p class="text-sm font-bold text-gray-700 mb-1">Step 2: Verify your email</p>
          <p class="text-xs text-gray-500 mb-4 font-medium">Code sent to <strong>{{ email }}</strong> <button @click="step = 1" type="button" class="text-primary-600 font-bold ml-1 hover:underline">Edit</button></p>
          <label class="label mb-2 text-primary-900">Verification Code</label>
          <input v-model="otp" type="text" class="input text-center text-2xl tracking-[0.5em] font-mono shadow-inner bg-gray-50/50 py-4"
            placeholder="------" maxlength="6" required autofocus>
          <p v-if="debugOtp" class="mt-2 text-[11px] text-center font-mono text-amber-700 bg-amber-50 py-1.5 rounded-lg border border-amber-200">
            ⚠️ Dev OTP: {{ debugOtp }}
          </p>
          <button type="submit" class="btn-primary w-full mt-6 py-3.5 text-base shadow-lg shadow-primary-500/20" :disabled="loading || otp.length < 6">
            <span v-if="loading" class="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin inline-block"></span>
            <span v-else>Verify Code</span>
          </button>
        </form>

        <!-- Step 3: Set Password -->
        <form v-else-if="step === 3" @submit.prevent="handleSetPassword" class="animate-fadeInUp">
          <p class="text-sm font-bold text-gray-700 mb-4">Step 3: Set your password</p>
          <div class="space-y-4">
            <div>
              <label class="label mb-2 text-primary-900">Password</label>
              <div class="relative flex items-center">
                <span class="absolute left-4 text-gray-400">🔒</span>
                <input v-model="password" :type="showPass ? 'text' : 'password'" class="input pl-12 pr-12 font-semibold bg-gray-50/50"
                  placeholder="Min 6 characters" required>
                <button type="button" @click="showPass = !showPass" class="absolute right-4 text-gray-400 hover:text-gray-600 text-sm">
                  {{ showPass ? '🙈' : '👁️' }}
                </button>
              </div>
            </div>
            <div>
              <label class="label mb-2 text-primary-900">Confirm Password</label>
              <div class="relative flex items-center">
                <span class="absolute left-4 text-gray-400">🔒</span>
                <input v-model="confirmPassword" :type="showPass ? 'text' : 'password'" class="input pl-12 font-semibold bg-gray-50/50"
                  placeholder="Repeat password" required>
              </div>
              <p v-if="confirmPassword && password !== confirmPassword" class="text-xs text-red-500 mt-1 font-medium">Passwords do not match</p>
            </div>
          </div>
          <button type="submit" class="btn-primary w-full mt-6 py-3.5 text-base shadow-lg shadow-primary-500/20" :disabled="loading || !password || password !== confirmPassword">
            <span v-if="loading" class="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin inline-block"></span>
            <span v-else>Create Account</span>
          </button>
        </form>

        <p class="text-center text-sm text-gray-500 mt-5 font-medium">
          Already have an account?
          <router-link to="/login" class="text-primary-600 font-bold hover:underline ml-1">Sign in</router-link>
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

const step = ref(1)
const email = ref('')
const otp = ref('')
const password = ref('')
const confirmPassword = ref('')
const showPass = ref(false)
const loading = ref(false)
const error = ref(null)
const success = ref(null)
const debugOtp = ref('')

async function handleRequestOtp() {
  loading.value = true
  error.value = null
  try {
    const res = await authStore.requestOtp(email.value)
    debugOtp.value = res.debug_otp || ''
    success.value = 'Verification code sent! Check your email.'
    step.value = 2
  } catch (e) {
    error.value = e.response?.data?.error || 'Failed to send code. Try again.'
  } finally {
    loading.value = false
  }
}

async function handleVerifyOtp() {
  loading.value = true
  error.value = null
  success.value = null
  try {
    const res = await authStore.verifyOtp(email.value, otp.value)
    if (!res.needs_password) {
      // Already has password (returning user), go to dashboard
      if (res.user?.role === 'admin') router.push('/admin/dashboard')
      else router.push('/dashboard')
    } else {
      success.value = 'Email verified! Now set your password.'
      step.value = 3
    }
  } catch (e) {
    error.value = e.response?.data?.error || 'Invalid code. Please try again.'
  } finally {
    loading.value = false
  }
}

async function handleSetPassword() {
  loading.value = true
  error.value = null
  try {
    const data = await authStore.setPassword(email.value, password.value, confirmPassword.value)
    if (data.user?.role === 'admin') router.push('/admin/dashboard')
    else router.push('/dashboard')
  } catch (e) {
    error.value = e.response?.data?.error || 'Failed to set password.'
  } finally {
    loading.value = false
  }
}
</script>
