import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../api'

export const useCategoriesStore = defineStore('categories', () => {
  const categories = ref([])
  const loading = ref(false)

  async function fetch() {
    loading.value = true
    try {
      const { data } = await api.get('/api/categories/')
      categories.value = data
    } finally {
      loading.value = false
    }
  }

  return { categories, loading, fetch }
})
