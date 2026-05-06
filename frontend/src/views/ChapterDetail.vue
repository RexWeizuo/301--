<template>
  <div class="fade-in">
    <div class="mb-8">
      <router-link :to="`/syllabus/${subjectId}`" class="text-pink-600 hover:text-pink-700 flex items-center gap-2 mb-4 font-bold">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path></svg>
        返回章节列表
      </router-link>
      <h1 class="text-3xl font-bold text-gray-900 mb-2">{{ chapterName }}</h1>
      <p class="text-gray-600">本章共 {{ knowledgePoints.length }} 个知识点</p>
    </div>

    <div class="space-y-6">
      <div v-for="(kp, idx) in knowledgePoints" :key="kp.id" class="card" :style="{ boxShadow: `6px 6px 0px ${idx % 2 === 0 ? '#ec4899' : '#06b6d4'}` }">
        <div class="flex items-start justify-between mb-4">
          <div class="flex items-center gap-3">
            <span class="w-8 h-8 bg-amber-200 flex items-center justify-center text-sm font-bold text-gray-900" style="border: 2px solid #1a1a2e; border-radius: 8px;">{{ idx + 1 }}</span>
            <h3 class="text-xl font-bold text-gray-900">{{ kp.name }}</h3>
          </div>
          <span class="badge badge-pink">知识点</span>
        </div>
        
        <div v-if="kp.content" class="mt-4 p-4 bg-yellow-50 border-2 border-[#1a1a2e]" style="border-radius: 12px;">
          <div class="prose max-w-none" v-html="kp.content"></div>
        </div>
        
        <div v-else class="mt-4 p-4 bg-yellow-50 border-2 border-[#1a1a2e] text-center" style="border-radius: 12px;">
          <p class="text-gray-500 text-sm">暂无详细内容</p>
        </div>

        <div class="mt-4 flex items-center justify-between">
          <button @click="markLearned(kp.id)" :class="['btn text-sm', kp.learned ? 'btn-primary' : 'btn-secondary']">
            {{ kp.learned ? '已学习' : '标记已学习' }}
          </button>
          <router-link :to="`/questions`" class="btn btn-secondary text-sm">
            查看相关习题
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
const route = useRoute()
const subjectId = computed(() => route.params.subjectId)
const chapterId = computed(() => route.params.chapterId)
const knowledgePoints = ref([])
const chapterName = ref('')

onMounted(async () => {
  try {
    const subjectsRes = await axios.get('/api/subjects')
    const subj = subjectsRes.data.subjects.find(s => s.id === subjectId.value)
    if (subj) {
      const ch = subj.chapters.find(c => c.id === chapterId.value)
      if (ch) chapterName.value = ch.name
    }
    const kpRes = await axios.get(`/api/knowledge-points/by-chapter/${chapterId.value}`)
    knowledgePoints.value = kpRes.data.map(kp => ({ ...kp, learned: false }))
  } catch (e) { console.error(e) }
})

const markLearned = async (kpId) => {
  const kp = knowledgePoints.value.find(k => k.id === kpId)
  if (kp) kp.learned = !kp.learned
  try {
    await axios.post('/api/study/records', {
      knowledge_point_id: kpId,
      action_type: 'learn',
      time_spent: 5,
      correct_rate: 1
    })
  } catch (e) { console.error(e) }
}
</script>
