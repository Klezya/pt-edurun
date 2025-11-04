<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getMembers } from './members.service'

const members = ref<any>(null)
const loading = ref(true)
const error = ref<string | null>(null)

onMounted(async () => {
  try {
    members.value = await getMembers()
  } catch (e: any) {
    error.value = e.message || 'Error desconocido'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="members-container">
    <h2>Members</h2>
    
    <div v-if="loading" class="loading">
      Cargando...
    </div>
    
    <div v-else-if="error" class="error">
      Error: {{ error }}
    </div>
    
    <div v-else-if="members" class="members-result">
      <pre>{{ JSON.stringify(members, null, 2) }}</pre>
    </div>
  </div>
</template>

<style scoped>
.members-container {
  padding: 20px;
}

h2 {
  margin-bottom: 20px;
}

.loading {
  color: #666;
}

.error {
  color: red;
  padding: 10px;
  background-color: #ffebee;
  border-radius: 4px;
}

.members-result {
  background-color: #f5f5f5;
  padding: 15px;
  border-radius: 4px;
  overflow-x: auto;
}

pre {
  margin: 0;
  font-family: 'Courier New', monospace;
  font-size: 14px;
}
</style>
