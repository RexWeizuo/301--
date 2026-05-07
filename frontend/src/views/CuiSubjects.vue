<template>
  <div class="fade-in">
    <div class="mb-8">
      <h1 class="text-4xl font-bold text-gray-900 mb-2">小崔说数 🔢</h1>
      <p class="text-gray-600">三大计算专项带练——极限、导数、积分</p>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <router-link v-for="subject in subjects" :key="subject.id" :to="`/cui/${subject.id}`" class="card group cursor-pointer" :style="{ boxShadow: `6px 6px 0px ${subjectColors[subject.id] || '#10b981'}` }">
        <div class="flex items-start justify-between mb-6">
          <div class="text-5xl">{{ getSubjectIcon(subject.id) }}</div>
          <span class="badge badge-pink">专项</span>
        </div>
        <h3 class="text-2xl font-bold text-gray-900 mb-2 group-hover:text-green-600 transition-colors">{{ subject.name }}</h3>
        <p class="text-gray-500 mb-4">共 {{ subject.chapters.length }} 个章节</p>
        <div class="flex items-center text-green-600 text-sm font-bold">
          <span>进入学习</span>
          <svg class="w-4 h-4 ml-2 group-hover:translate-x-2 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
          </svg>
        </div>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
const subjects = ref([])
const subjectIcons = { three_calc: '🔢' }
const subjectColors = { three_calc: '#10b981' }
const getSubjectIcon = (id) => subjectIcons[id] || '📘'

onMounted(async () => {
  try {
    const r = await axios.get('/api/subjects')
    // Only show three_calc subject
    subjects.value = r.data.subjects.filter(s => s.id === 'three_calc')
  } catch (e) { console.error(e) }
})
</script>
