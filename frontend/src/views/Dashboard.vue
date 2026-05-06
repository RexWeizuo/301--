<template>
  <div class="fade-in space-y-6">
    <div class="mb-8">
      <h1 class="text-4xl font-bold text-gray-900 mb-2">欢迎回来 👋</h1>
      <p class="text-gray-600">今天也是充满希望的一天，继续你的301之旅吧！</p>
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div class="card" style="box-shadow: 6px 6px 0px #ec4899;">
        <div class="flex items-center justify-between mb-4">
          <div class="w-12 h-12 bg-pink-200 flex items-center justify-center" style="border: 2px solid #1a1a2e; border-radius: 12px;">
            <span class="text-2xl">📖</span>
          </div>
          <span class="badge badge-pink">今日</span>
        </div>
        <p class="text-gray-600 text-sm mb-1">新学知识点</p>
        <p class="stat-number gradient-text">{{ dashboard.today_new_count }}</p>
      </div>
      
      <div class="card" style="box-shadow: 6px 6px 0px #06b6d4;">
        <div class="flex items-center justify-between mb-4">
          <div class="w-12 h-12 bg-cyan-200 flex items-center justify-center" style="border: 2px solid #1a1a2e; border-radius: 12px;">
            <span class="text-2xl">🔄</span>
          </div>
          <span class="badge badge-cyan">复习</span>
        </div>
        <p class="text-gray-600 text-sm mb-1">今日复习</p>
        <p class="stat-number gradient-text">{{ dashboard.today_review_count }}</p>
      </div>
      
      <div class="card" style="box-shadow: 6px 6px 0px #8b5cf6;">
        <div class="flex items-center justify-between mb-4">
          <div class="w-12 h-12 bg-purple-200 flex items-center justify-center" style="border: 2px solid #1a1a2e; border-radius: 12px;">
            <span class="text-2xl">✍️</span>
          </div>
          <span class="badge badge-purple">练习</span>
        </div>
        <p class="text-gray-600 text-sm mb-1">今日练习</p>
        <p class="stat-number gradient-text">{{ dashboard.today_question_count }}</p>
      </div>
      
      <div class="card" style="box-shadow: 6px 6px 0px #f59e0b;">
        <div class="flex items-center justify-between mb-4">
          <div class="w-12 h-12 bg-amber-200 flex items-center justify-center" style="border: 2px solid #1a1a2e; border-radius: 12px;">
            <span class="text-2xl">🎯</span>
          </div>
          <span class="badge badge-amber">进度</span>
        </div>
        <p class="text-gray-600 text-sm mb-1">完成进度</p>
        <p class="stat-number gradient-text">{{ dashboard.today_completed_percentage.toFixed(0) }}%</p>
        <div class="progress-bar mt-3">
          <div class="progress-bar-fill" :style="{ width: dashboard.today_completed_percentage + '%' }"></div>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div class="card">
        <div class="flex items-center justify-between mb-6">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-pink-200 flex items-center justify-center" style="border: 2px solid #1a1a2e; border-radius: 10px;">
              <span class="text-xl">⏰</span>
            </div>
            <h3 class="text-xl font-bold text-gray-900">待复习提醒</h3>
          </div>
          <span class="badge badge-rose">{{ dashboard.urgent_reviews.length }} 项</span>
        </div>
        <div v-if="dashboard.urgent_reviews.length === 0" class="text-center py-8">
          <div class="text-6xl mb-4">🎉</div>
          <p class="text-gray-600">暂无紧急复习任务</p>
        </div>
        <div v-else class="space-y-3 max-h-80 overflow-y-auto">
          <div v-for="review in dashboard.urgent_reviews" :key="review.record_id"
               class="p-4 bg-yellow-50 border-2 border-[#1a1a2e] hover:bg-yellow-100 transition-all" style="border-radius: 12px;">
            <div class="flex justify-between items-center">
              <div>
                <p class="font-bold text-gray-900">{{ review.knowledge_point_name }}</p>
                <p class="text-sm text-gray-500 mt-1">已复习 {{ review.review_count }} 次</p>
              </div>
              <span :class="['badge', getMasteryBadge(review.mastery_level)]">
                {{ (review.mastery_level * 100).toFixed(0) }}%
              </span>
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="flex items-center justify-between mb-6">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-red-200 flex items-center justify-center" style="border: 2px solid #1a1a2e; border-radius: 10px;">
              <span class="text-xl">⚠️</span>
            </div>
            <h3 class="text-xl font-bold text-gray-900">薄弱知识点</h3>
          </div>
          <span class="badge badge-rose">{{ dashboard.weak_points.length }} 项</span>
        </div>
        <div v-if="dashboard.weak_points.length === 0" class="text-center py-8">
          <div class="text-6xl mb-4">💪</div>
          <p class="text-gray-600">暂无薄弱知识点，继续保持！</p>
        </div>
        <div v-else class="space-y-3 max-h-80 overflow-y-auto">
          <router-link v-for="point in dashboard.weak_points" :key="point.knowledge_point_id"
                       :to="`/syllabus/${getSubjectByKpId(point.knowledge_point_id)}`"
                       class="block p-4 bg-cyan-50 border-2 border-[#1a1a2e] hover:bg-cyan-100 transition-all" style="border-radius: 12px;">
            <div class="flex justify-between items-center">
              <span class="font-bold text-red-700 hover:text-red-600">{{ point.name }}</span>
              <span class="badge badge-rose">{{ (point.mastery_level * 100).toFixed(0) }}%</span>
            </div>
          </router-link>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="flex items-center gap-3 mb-6">
        <div class="w-10 h-10 bg-amber-200 flex items-center justify-center" style="border: 2px solid #1a1a2e; border-radius: 10px;">
          <span class="text-xl">📈</span>
        </div>
        <h3 class="text-xl font-bold text-gray-900">科目进度</h3>
      </div>
      <div class="space-y-5">
        <div v-for="subject in subjects" :key="subject.id" class="p-4 bg-purple-50 border-2 border-[#1a1a2e]" style="border-radius: 12px;">
          <div class="flex justify-between items-center mb-3">
            <div class="flex items-center gap-3">
              <span class="text-2xl">{{ subject.icon }}</span>
              <h4 class="font-bold text-gray-900">{{ subject.name }}</h4>
              <span class="badge badge-pink">{{ subject.score }}分</span>
            </div>
            <span class="text-sm text-gray-600">{{ subject.chapterCount }} 个章节</span>
          </div>
          <div class="progress-bar">
            <div class="progress-bar-fill" :style="{ width: getProgress(subject.id) + '%' }"></div>
          </div>
          <p class="text-sm text-gray-500 mt-2">完成进度: {{ getProgress(subject.id).toFixed(0) }}%</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const dashboard = ref({
  today_new_count: 0, today_review_count: 0, today_question_count: 0,
  today_completed_percentage: 0, subject_progress: [], urgent_reviews: [], weak_points: []
})
const subjects = ref([])

const subjectIcons = { advanced_math: '📐', linear_algebra: '📊', probability: '🎲' }
const subjectNames = { advanced_math: '高等数学', linear_algebra: '线性代数', probability: '概率论与数理统计' }

const getProgress = (id) => {
  const sp = dashboard.value.subject_progress.find(s => s.subject_id === id)
  if (!sp || !sp.chapters?.length) return 0
  return sp.chapters.reduce((a, c) => a + c.completion_percentage, 0) / sp.chapters.length
}

const getMasteryBadge = (m) => m >= 0.9 ? 'badge-purple' : m >= 0.7 ? 'badge-pink' : m >= 0.5 ? 'badge-amber' : 'badge-rose'

const getSubjectByKpId = (kpId) => {
  if (kpId.startsWith('am_')) return 'advanced_math'
  if (kpId.startsWith('la_')) return 'linear_algebra'
  return 'probability'
}

onMounted(async () => {
  try {
    const [d, s] = await Promise.all([
      axios.get('/api/study/dashboard'),
      axios.get('/api/subjects')
    ])
    dashboard.value = d.data
    subjects.value = s.data.subjects.map(subj => ({
      ...subj,
      icon: subjectIcons[subj.id] || '📘',
      name: subjectNames[subj.id] || subj.name
    }))
  } catch (e) { console.error(e) }
})
</script>
