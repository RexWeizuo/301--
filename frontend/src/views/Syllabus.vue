<template>
  <div class="fade-in">
    <div class="mb-8">
      <h1 class="text-4xl font-bold text-gray-900 mb-2">考纲 📚</h1>
      <p class="text-gray-600">301三科全面覆盖，系统学习助你成功上岸</p>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <router-link v-for="subject in subjects" :key="subject.id" :to="`/syllabus/${subject.id}`" class="card group cursor-pointer" :style="{ boxShadow: `6px 6px 0px ${subjectColors[subject.id] || '#1a1a2e'}` }">
        <div class="flex items-start justify-between mb-6">
          <div class="text-5xl">{{ getSubjectIcon(subject.id) }}</div>
          <span class="badge badge-pink">{{ subject.score }}分</span>
        </div>
        <h3 class="text-2xl font-bold text-gray-900 mb-2 group-hover:text-pink-600 transition-colors">{{ subject.name }}</h3>
        <p class="text-gray-500 mb-4">共 {{ subject.chapters.length }} 个章节</p>
        <div class="flex items-center text-pink-600 text-sm font-bold">
          <span>查看考纲</span>
          <svg class="w-4 h-4 ml-2 group-hover:translate-x-2 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
          </svg>
        </div>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
const subjects = ref([])
const subjectIcons = { advanced_math: '📐', linear_algebra: '📊', probability: '🎲', three_calc: '🔢' }
const subjectColors = { advanced_math: '#ec4899', linear_algebra: '#06b6d4', probability: '#f59e0b', three_calc: '#10b981' }
const getSubjectIcon = (id) => subjectIcons[id] || '📘'
onMounted(async () => {
  try { 
    const r = await axios.get('/api/subjects'); 
    subjects.value = r.data.subjects.filter(s => s.id !== 'three_calc')
  } catch (e) { console.error(e) }
})
</script>
