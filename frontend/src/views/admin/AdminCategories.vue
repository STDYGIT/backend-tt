<template>
  <div>
    <div class="mb-8 flex flex-col sm:flex-row sm:items-end justify-between gap-4">
      <div>
        <h1 class="text-3xl font-extrabold text-gray-900 tracking-tight">Waste Categories</h1>
        <p class="text-gray-500 mt-2 font-medium">Manage categories and their subtypes</p>
      </div>
      <button @click="openModal()" class="btn-primary py-2.5 px-5 shadow-md shadow-primary-500/20">
         + Add Category
      </button>
    </div>

    <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="i in 6" :key="i" class="h-48 bg-gray-200 animate-pulse rounded-2xl"></div>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 stagger">
      <!-- Category Card -->
      <div v-for="cat in categories" :key="cat.id" class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-shadow animate-fadeInUp">
        <div class="p-5 border-b border-gray-100 flex items-center justify-between" :style="{ backgroundColor: cat.color + '10' }">
          <div class="flex items-center gap-3">
            <div class="w-12 h-12 rounded-xl flex items-center justify-center text-2xl shadow-sm" :style="{ backgroundColor: 'white', color: cat.color }">
              {{ cat.icon }}
            </div>
            <div>
              <h3 class="font-bold text-gray-900 text-lg">{{ cat.name }}</h3>
              <span v-if="!cat.is_active" class="badge bg-red-100 text-red-700 mt-1">Inactive</span>
            </div>
          </div>
          <button @click="openModal(cat)" class="p-2 text-gray-400 hover:text-primary-600 transition-colors bg-white rounded-lg shadow-sm">
            ✏️
          </button>
        </div>
        
        <div class="p-5">
           <div class="flex items-center justify-between mb-3">
             <h4 class="text-xs font-bold uppercase tracking-wider text-gray-500">Subtypes ({{ cat.subtypes.length }})</h4>
             <button @click="openSubtypeModal(cat)" class="text-[10px] font-bold text-primary-600 bg-primary-50 px-2 py-1 rounded hover:bg-primary-100 transition-colors">+ Add</button>
           </div>
           
           <div class="flex flex-col gap-2 max-h-48 overflow-y-auto pr-2 scrollbar-thin">
             <div v-for="sub in cat.subtypes" :key="sub.id" class="px-3 py-2 text-sm font-medium text-gray-700 bg-gray-50 rounded-lg border border-gray-200 flex items-center justify-between group cursor-pointer hover:bg-white transition-colors" @click="openSubtypeModal(cat, sub)">
                <div>
                   <div>{{ sub.name }}</div>
                   <div class="text-[10px] text-gray-500 mt-0.5">₹{{ sub.rate_per_unit || 0 }} / {{ sub.unit || 'kg' }}</div>
                </div>
                <button @click.stop="deleteSubtype(sub.id)" class="opacity-0 group-hover:opacity-100 hover:text-red-500 text-gray-400 transition-opacity">×</button>
             </div>
             <p v-if="!cat.subtypes.length" class="text-xs text-gray-400 italic">No subtypes defined.</p>
           </div>
        </div>
      </div>
    </div>

    <!-- Category Modal -->
    <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm">
      <div class="bg-white w-full max-w-md rounded-2xl shadow-xl flex flex-col max-h-[90vh]">
        <div class="p-6 border-b border-gray-100 flex justify-between items-center">
          <h2 class="text-lg font-bold">{{ formData.id ? 'Edit Category' : 'New Category' }}</h2>
          <button @click="showModal = false" class="text-gray-400 hover:text-gray-600">×</button>
        </div>
        
        <form @submit.prevent="saveCategory" class="p-6 space-y-4 overflow-y-auto">
          <div>
            <label class="label">Category Name</label>
            <input v-model="formData.name" type="text" class="input bg-gray-50 border-gray-100" required>
          </div>
          <div class="grid grid-cols-2 gap-4">
             <div>
              <label class="label">Emoji Icon</label>
              <input v-model="formData.icon" type="text" class="input bg-gray-50 border-gray-100 text-center text-xl" required>
             </div>
             <div>
              <label class="label">Theme Color</label>
              <input v-model="formData.color" type="color" class="w-full h-12 p-1 rounded-xl cursor-pointer bg-gray-50 border border-gray-100" required>
             </div>
          </div>
          <div class="flex items-center gap-3 mt-4" v-if="formData.id">
            <input type="checkbox" v-model="formData.is_active" id="is_active" class="w-4 h-4 rounded text-primary-600">
            <label for="is_active" class="text-sm font-semibold text-gray-700">Category Active</label>
          </div>
          
          <div class="pt-4 flex gap-3">
             <button type="button" @click="showModal = false" class="btn-ghost flex-1">Cancel</button>
             <button type="submit" class="btn-primary flex-1 shadow-md shadow-primary-500/20" :disabled="saving">
               {{ saving ? 'Saving...' : 'Save' }}
             </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Subtype Modal -->
    <div v-if="showSubtypeModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm">
      <div class="bg-white w-full max-w-sm rounded-2xl shadow-xl flex flex-col max-h-[90vh]">
        <div class="p-6 border-b border-gray-100 flex justify-between items-center">
          <h2 class="text-lg font-bold">{{ subtypeForm.id ? 'Edit Subtype' : 'New Subtype' }}</h2>
          <button @click="showSubtypeModal = false" class="text-gray-400 hover:text-gray-600">×</button>
        </div>
        
        <form @submit.prevent="saveSubtype" class="p-6 space-y-4 overflow-y-auto">
          <div>
            <label class="label">Subtype Name</label>
            <input v-model="subtypeForm.name" type="text" class="input bg-gray-50 border-gray-100" required placeholder="e.g. Iron/Steel">
          </div>
          <div class="grid grid-cols-2 gap-4">
             <div>
              <label class="label">Rate (₹)</label>
              <input v-model.number="subtypeForm.rate_per_unit" type="number" step="0.5" min="0" class="input bg-gray-50 border-gray-100" required>
             </div>
             <div>
              <label class="label">Unit</label>
              <select v-model="subtypeForm.unit" class="input bg-gray-50 border-gray-100" required>
                 <option value="kg">kg</option>
                 <option value="piece">piece</option>
                 <option value="liter">liter</option>
              </select>
             </div>
          </div>
          <div class="flex items-center gap-3 mt-4" v-if="subtypeForm.id">
            <input type="checkbox" v-model="subtypeForm.is_active" id="sub_is_active" class="w-4 h-4 rounded text-primary-600">
            <label for="sub_is_active" class="text-sm font-semibold text-gray-700">Subtype Active</label>
          </div>
          
          <div class="pt-4 flex gap-3">
             <button type="button" @click="showSubtypeModal = false" class="btn-ghost flex-1">Cancel</button>
             <button type="submit" class="btn-primary flex-1 shadow-md shadow-primary-500/20" :disabled="saving">
               {{ saving ? 'Saving...' : 'Save' }}
             </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api'

const categories = ref([])
const loading = ref(true)
const showModal = ref(false)
const showSubtypeModal = ref(false)
const saving = ref(false)

const formData = ref({ id: null, name: '', icon: '♻️', color: '#4CAF71', is_active: true })
const subtypeForm = ref({ id: null, category_id: null, name: '', rate_per_unit: 0.0, unit: 'kg', is_active: true })

async function fetch() {
  loading.value = true
  try {
    const { data } = await api.get('/api/admin/categories')
    categories.value = data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

onMounted(() => fetch())

function openModal(cat = null) {
  if (cat) {
    formData.value = { ...cat }
  } else {
    formData.value = { id: null, name: '', icon: '♻️', color: '#4CAF71', is_active: true }
  }
  showModal.value = true
}

async function saveCategory() {
  saving.value = true
  try {
    if (formData.value.id) {
      await api.put(`/api/admin/categories/${formData.value.id}`, formData.value)
    } else {
      await api.post('/api/admin/categories', formData.value)
    }
    showModal.value = false
    fetch()
  } catch (e) {
    alert('Failed to save')
  } finally {
    saving.value = false
  }
}

function openSubtypeModal(cat, sub = null) {
  if (sub) {
    subtypeForm.value = { ...sub, category_id: cat.id }
  } else {
    subtypeForm.value = { id: null, category_id: cat.id, name: '', rate_per_unit: 0.0, unit: 'kg', is_active: true }
  }
  showSubtypeModal.value = true
}

async function saveSubtype() {
  saving.value = true
  try {
    if (subtypeForm.value.id) {
      await api.put(`/api/admin/subtypes/${subtypeForm.value.id}`, subtypeForm.value)
    } else {
      await api.post(`/api/admin/categories/${subtypeForm.value.category_id}/subtypes`, subtypeForm.value)
    }
    showSubtypeModal.value = false
    fetch()
  } catch (e) {
    alert('Failed to save subtype')
  } finally {
    saving.value = false
  }
}

function deleteSubtype(id) {
  if (!confirm('Deactivate this subtype?')) return
  api.delete(`/api/admin/subtypes/${id}`)
    .then(() => fetch())
    .catch(() => alert('Failed to delete'))
}
</script>

<style scoped>
.scrollbar-thin::-webkit-scrollbar { width: 4px; }
.scrollbar-thin::-webkit-scrollbar-track { background: transparent; }
.scrollbar-thin::-webkit-scrollbar-thumb { background: #e5e7eb; border-radius: 4px; }
</style>
