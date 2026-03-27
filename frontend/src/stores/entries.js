import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../api'

export const useEntriesStore = defineStore('entries', () => {
  const entries = ref([])
  const currentEntry = ref(null)
  const loading = ref(false)

  async function fetchAll() {
    loading.value = true
    try {
      const { data } = await api.get('/api/entries/')
      entries.value = data
    } finally {
      loading.value = false
    }
  }

  async function fetchOne(id) {
    loading.value = true
    try {
      const { data } = await api.get(`/api/entries/${id}`)
      currentEntry.value = data
      return data
    } finally {
      loading.value = false
    }
  }

  async function submit(formData) {
    const { data } = await api.post('/api/entries/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    entries.value.unshift(data)
    return data
  }

  async function saveLocation(id, payload) {
    const { data } = await api.post(`/api/entries/${id}/location`, payload)
    currentEntry.value = data
    updateLocalEntry(data)
    return data
  }

  async function schedulePickup(id, slotId) {
    const { data } = await api.post(`/api/entries/${id}/schedule`, { slot_id: slotId })
    currentEntry.value = data
    updateLocalEntry(data)
    return data
  }

  async function fetchSlots(id) {
    const { data } = await api.get(`/api/entries/${id}/slots`)
    return data
  }

  function updateLocalEntry(entry) {
    const idx = entries.value.findIndex(e => e.id === entry.id)
    if (idx !== -1) entries.value[idx] = entry
  }

  return { entries, currentEntry, loading, fetchAll, fetchOne, submit, saveLocation, schedulePickup, fetchSlots }
})
