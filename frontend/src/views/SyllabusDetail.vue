<template>
  <div class="fade-in">
    <div class="mb-8">
      <router-link to="/syllabus" class="text-pink-600 hover:text-pink-700 flex items-center gap-2 mb-4 font-bold">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path></svg>
        返回考纲
      </router-link>
      <h1 class="text-4xl font-bold text-gray-900 mb-2">{{ subjectIcon }} {{ subjectName }}</h1>
      <p class="text-gray-600">共 {{ chapters.length }} 个章节，点击章节查看知识点详情</p>
    </div>
    <div class="space-y-4">
      <router-link v-for="chapter in chapters" :key="chapter.id" 
                   :to="`/syllabus/${subjectId}/chapters/${chapter.id}`"
                   class="card group cursor-pointer flex items-center justify-between">
        <div class="flex items-center gap-4">
          <div class="w-12 h-12 bg-cyan-200 flex items-center justify-center text-xl font-bold text-gray-900" style="border: 2px solid #1a1a2e; border-radius: 12px;">
            {{ getChapterIndex(chapter.name) }}
          </div>
          <div>
            <h3 class="text-lg font-bold text-gray-900 group-hover:text-pink-600 transition-colors">{{ chapter.name }}</h3>
            <p class="text-sm text-gray-500 mt-1">{{ getChapterKpCount(chapter.id) }} 个知识点</p>
          </div>
        </div>
        <svg class="w-6 h-6 text-gray-400 group-hover:translate-x-2 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
        </svg>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
const route = useRoute()
const subjectId = computed(() => route.params.subjectId)
const chapters = ref([])
const subjectName = ref('')
const subjectIcon = ref('📘')

const subjectIcons = { advanced_math: '📐', linear_algebra: '📊', probability: '🎲' }
const chapterKpCounts = ref({})

const getChapterIndex = (name) => {
  const match = name.match(/^([一二三四五六七八九十]+)/)
  return match ? match[1] : ''
}

const getChapterKpCount = (id) => chapterKpCounts.value[id] || 0

onMounted(async () => {
  try {
    const r = await axios.get('/api/subjects')
    const subj = r.data.subjects.find(s => s.id === subjectId.value)
    if (subj) {
      chapters.value = subj.chapters
      subjectName.value = subj.name
      subjectIcon.value = subjectIcons[subjectId.value] || '📘'
    }
  } catch (e) { console.error(e) }
})
</script>
