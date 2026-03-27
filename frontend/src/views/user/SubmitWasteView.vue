<template>
  <div class="bg-gray-50 min-h-screen pb-safe">
    <div class="bg-white px-4 pt-12 pb-4 shadow-sm sticky top-0 z-10 flex items-center justify-between border-b border-gray-100">
      <button @click="$router.push('/dashboard')" class="p-2 -ml-2 text-gray-600 hover:bg-gray-100 rounded-full transition-colors">
        <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 19l-7-7 7-7" /></svg>
      </button>
      <h1 class="text-lg font-bold tracking-tight text-gray-900">Add Recyclables</h1>
      <div class="w-10"></div>
    </div>

    <form @submit.prevent="submit" class="p-5 space-y-6 max-w-5xl w-full mx-auto mt-2">
      <!-- Image Upload -->
      <div>
        <label class="label text-gray-700">Photo of items</label>
        <div 
          class="h-44 rounded-2xl border-2 border-dashed flex flex-col items-center justify-center relative overflow-hidden transition-colors"
          :class="imagePreview ? 'border-primary-500 bg-primary-50/50' : 'border-gray-300 bg-white hover:bg-gray-50 cursor-pointer'"
          @click="triggerFileInput"
        >
          <img v-if="imagePreview" :src="imagePreview" class="absolute inset-0 w-full h-full object-cover" />
          <div v-if="imagePreview" class="absolute inset-0 bg-black/40 flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity">
            <span class="text-white font-semibold flexItems-center gap-2">
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
              Retake photo
            </span>
          </div>
          
          <div v-if="!imagePreview" class="text-center text-gray-500">
            <div class="w-14 h-14 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-3 text-gray-400">
               <svg class="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
            </div>
            <p class="font-semibold text-sm text-gray-700">Tap to take photo</p>
            <p class="text-xs mt-1">or select from gallery</p>
          </div>
          
          <input type="file" ref="fileInput" accept="image/*" class="hidden" @change="onFileChange" capture="environment">
        </div>
      </div>

      <!-- Category -->
      <div class="card shadow-sm border border-gray-100">
        <label class="label text-gray-700">Category</label>
        <select v-model="formData.category_id" class="input bg-gray-50 border-gray-200 mb-4" required>
          <option value="" disabled>Select category...</option>
          <option v-for="c in categoriesStore.categories" :key="c.id" :value="c.id">
            {{ c.icon }} {{ c.name }}
          </option>
        </select>

        <div v-if="selectedCategory?.subtypes?.length">
          <label class="label text-gray-700 mb-2">Item Type & Estimated Rate</label>
          <div class="flex flex-wrap gap-2 mb-3">
            <button
              v-for="s in selectedCategory.subtypes"
              :key="s.id"
              type="button"
              @click="formData.subtype_id = s.id"
              class="px-4 py-2 rounded-xl text-xs font-semibold border transition-colors flex flex-col items-start min-w-[100px]"
              :class="formData.subtype_id === s.id ? 'bg-primary-500 border-primary-500 text-white shadow-sm' : 'bg-white border-gray-200 text-gray-600 hover:border-gray-300 hover:bg-gray-50'"
            >
              <span>{{ s.name }}</span>
              <span v-if="s.rate_per_unit > 0 && s.name.toLowerCase() !== 'other'" class="text-[10px] mt-0.5 font-normal" :class="formData.subtype_id === s.id ? 'text-primary-100' : 'text-primary-600'">
                 ₹{{ s.rate_per_unit }} / {{ s.unit }}
              </span>
            </button>
          </div>
        </div>

        <input 
          v-if="isOtherSubtype" 
          v-model="formData.subtype_other" 
          type="text" 
          class="input bg-gray-50 border-gray-200 mt-2" 
          placeholder="Please specify item type..." 
          required
        >
      </div>

      <!-- Details -->
      <div class="card shadow-sm border border-gray-100">
        <div class="mb-4">
          <label class="label text-gray-700">Description</label>
          <textarea v-model="formData.description" rows="3" class="textarea bg-gray-50 border-gray-200" placeholder="Roughly how many items? Any other notes?"></textarea>
        </div>

        <div class="grid grid-cols-2 gap-3 pb-1">
          <div>
            <label class="label text-gray-700">Condition</label>
            <select v-model="formData.condition" class="input bg-gray-50 border-gray-200 text-sm py-2.5">
              <option value="">Select...</option>
              <option value="Intact">Whole/Intact</option>
              <option value="Broken">Broken/Pieces</option>
              <option value="Mixed">Mixed condition</option>
            </select>
          </div>
          <div>
            <label class="label text-gray-700">Age/Usage</label>
            <select v-model="formData.age_usage" class="input bg-gray-50 border-gray-200 text-sm py-2.5">
              <option value="">Select...</option>
              <option value="Recently used">Recent</option>
              <option value="Very old/Rusty">Very old/Rusty</option>
            </select>
          </div>
        </div>
      </div>

      <button type="submit" class="btn-primary w-full py-4 text-base shadow-lg shadow-primary-500/20" :disabled="loading || !canSubmit">
        <span v-if="loading" class="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
        <span v-else>Submit for Verification</span>
      </button>

      <div class="h-8"></div>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useCategoriesStore } from '../../stores/categories'
import { useEntriesStore } from '../../stores/entries'

const router = useRouter()
const route = useRoute()
const categoriesStore = useCategoriesStore()
const entriesStore = useEntriesStore()

const fileInput = ref(null)
const imageFile = ref(null)
const imagePreview = ref(null)
const loading = ref(false)

const formData = reactive({
  category_id: route.query.category_id ? Number(route.query.category_id) : '',
  subtype_id: '',
  subtype_other: '',
  description: '',
  condition: '',
  age_usage: ''
})

onMounted(() => {
  if (categoriesStore.categories.length === 0) categoriesStore.fetch()
})

const selectedCategory = computed(() => {
  return categoriesStore.categories.find(c => c.id === formData.category_id)
})

const isOtherSubtype = computed(() => {
  if (!selectedCategory.value) return false
  const subtype = selectedCategory.value.subtypes.find(s => s.id === formData.subtype_id)
  return subtype?.name.toLowerCase() === 'other'
})

const canSubmit = computed(() => {
  return formData.category_id && imageFile.value && (isOtherSubtype.value ? formData.subtype_other.trim() : true)
})

function triggerFileInput() {
  fileInput.value.click()
}

function onFileChange(e) {
  const file = e.target.files[0]
  if (file && file.type.startsWith('image/')) {
    imageFile.value = file
    const reader = new FileReader()
    reader.onload = e => imagePreview.value = e.target.result
    reader.readAsDataURL(file)
  } else if (file) {
    alert('Please capture or select a valid image file.')
    e.target.value = '' // reset
  }
}

async function submit() {
  if (!canSubmit.value) return
  loading.value = true

  try {
    const data = new FormData()
    if (imageFile.value) data.append('image', imageFile.value)
    data.append('category_id', formData.category_id)
    if (formData.subtype_id) data.append('subtype_id', formData.subtype_id)
    if (isOtherSubtype.value) data.append('subtype_other', formData.subtype_other)
    if (formData.description) data.append('description', formData.description)
    if (formData.condition) data.append('condition', formData.condition)
    if (formData.age_usage) data.append('age_usage', formData.age_usage)

    const res = await entriesStore.submit(data)
    router.replace(`/entry/${res.id}`)
  } catch (e) {
    console.error(e)
    alert('Failed to submit entry')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.pb-safe { padding-bottom: env(safe-area-inset-bottom, 2rem); }
</style>
