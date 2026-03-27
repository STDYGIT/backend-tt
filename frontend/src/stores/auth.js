import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('tt_token') || null)
  const user = ref(JSON.parse(localStorage.getItem('tt_user') || 'null'))
  const loading = ref(false)
  const error = ref(null)

  const isLoggedIn = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'admin')

  // ─── Auth core ────────────────────────────────────────────────────────────

  function _setSession(data) {
    token.value = data.access_token
    user.value = data.user
    localStorage.setItem('tt_token', data.access_token)
    localStorage.setItem('tt_user', JSON.stringify(data.user))
  }

  async function login(email, password) {
    loading.value = true
    error.value = null
    try {
      const { data } = await api.post('/api/auth/login', { email, password })
      _setSession(data)
      return data
    } catch (e) {
      error.value = e.response?.data?.error || 'Login failed'
      throw e
    } finally {
      loading.value = false
    }
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('tt_token')
    localStorage.removeItem('tt_user')
  }

  // ─── Registration flow ────────────────────────────────────────────────────

  async function requestOtp(email) {
    loading.value = true
    error.value = null
    try {
      const { data } = await api.post('/api/auth/request-otp', { email })
      return data
    } catch (e) {
      error.value = e.response?.data?.error || 'Failed to send OTP'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function verifyOtp(email, otp) {
    loading.value = true
    error.value = null
    try {
      const { data } = await api.post('/api/auth/verify-otp', { email, otp })
      // Only set session if they don't need to set a password
      if (!data.needs_password) {
        _setSession(data)
      }
      return data
    } catch (e) {
      error.value = e.response?.data?.error || 'Invalid OTP'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function setPassword(email, password, confirm_password) {
    loading.value = true
    error.value = null
    try {
      const { data } = await api.post('/api/auth/set-password', { email, password, confirm_password })
      _setSession(data)
      return data
    } catch (e) {
      error.value = e.response?.data?.error || 'Failed to set password'
      throw e
    } finally {
      loading.value = false
    }
  }

  // ─── Profile ──────────────────────────────────────────────────────────────

  async function fetchProfile() {
    const { data } = await api.get('/api/user/me')
    user.value = data
    localStorage.setItem('tt_user', JSON.stringify(data))
    return data
  }

  async function updateProfile(payload) {
    const { data } = await api.put('/api/user/me', payload)
    user.value = data
    localStorage.setItem('tt_user', JSON.stringify(data))
    return data
  }

  return {
    token, user, loading, error, isLoggedIn, isAdmin,
    login, logout, requestOtp, verifyOtp, setPassword, fetchProfile, updateProfile
  }
})
