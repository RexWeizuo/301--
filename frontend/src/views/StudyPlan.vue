<template>
  <div class="fade-in space-y-6">
    <div class="mb-8">
      <h1 class="text-4xl font-bold text-gray-900 mb-2">学习规划 📅</h1>
      <p class="text-gray-600">科学规划，高效备考，距离成功更进一步</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="card text-center" style="box-shadow: 6px 6px 0px #ef4444;">
        <div class="w-16 h-16 bg-red-200 flex items-center justify-center mx-auto mb-4" style="border: 2px solid #1a1a2e; border-radius: 16px;"><span class="text-3xl">⏰</span></div>
        <p class="text-gray-500 text-sm mb-2">距离考试还有</p>
        <p class="stat-number text-red-600">{{ daysToExam }}</p>
        <p class="text-gray-500 mt-2">天</p>
      </div>
      <div class="card text-center" style="box-shadow: 6px 6px 0px #8b5cf6;">
        <div class="w-16 h-16 bg-purple-200 flex items-center justify-center mx-auto mb-4" style="border: 2px solid #1a1a2e; border-radius: 16px;"><span class="text-3xl">📚</span></div>
        <p class="text-gray-500 text-sm mb-2">本周学习天数</p>
        <p class="stat-number text-purple-600">{{ weeklyStats.study_days || 0 }}</p>
        <p class="text-gray-500 mt-2">天</p>
      </div>
      <div class="card text-center" style="box-shadow: 6px 6px 0px #f59e0b;">
        <div class="w-16 h-16 bg-amber-200 flex items-center justify-center mx-auto mb-4" style="border: 2px solid #1a1a2e; border-radius: 16px;"><span class="text-3xl">🎯</span></div>
        <p class="text-gray-500 text-sm mb-2">考试日期</p>
        <p class="text-xl font-bold text-amber-600">2026-12-19</p>
        <p class="text-gray-500 mt-2">301</p>
      </div>
    </div>

    <div class="card">
      <div class="flex items-center gap-3 mb-8">
        <div class="w-12 h-12 bg-cyan-200 flex items-center justify-center" style="border: 2px solid #1a1a2e; border-radius: 12px;"><span class="text-2xl">📊</span></div>
        <h3 class="text-2xl font-bold text-gray-900">本周学习统计</h3>
      </div>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
        <div class="p-6 bg-pink-100 text-center border-2 border-[#1a1a2e]" style="border-radius: 16px;">
          <p class="text-sm text-gray-600 mb-2">学习天数</p>
          <p class="text-4xl font-bold text-pink-600">{{ weeklyStats.study_days || 0 }}</p>
        </div>
        <div class="p-6 bg-cyan-100 text-center border-2 border-[#1a1a2e]" style="border-radius: 16px;">
          <p class="text-sm text-gray-600 mb-2">学习时长</p>
          <p class="text-4xl font-bold text-cyan-600">{{ ((weeklyStats.total_time_spent || 0) / 60).toFixed(0) }}</p>
          <p class="text-sm text-gray-500">分钟</p>
        </div>
        <div class="p-6 bg-purple-100 text-center border-2 border-[#1a1a2e]" style="border-radius: 16px;">
          <p class="text-sm text-gray-600 mb-2">新学知识点</p>
          <p class="text-4xl font-bold text-purple-600">{{ weeklyStats.new_knowledge_points || 0 }}</p>
        </div>
        <div class="p-6 bg-amber-100 text-center border-2 border-[#1a1a2e]" style="border-radius: 16px;">
          <p class="text-sm text-gray-600 mb-2">复习知识点</p>
          <p class="text-4xl font-bold text-amber-600">{{ weeklyStats.reviewed_knowledge_points || 0 }}</p>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="flex items-center justify-between mb-8">
        <div class="flex items-center gap-3">
          <div class="w-12 h-12 bg-amber-200 flex items-center justify-center" style="border: 2px solid #1a1a2e; border-radius: 12px;"><span class="text-2xl">🔄</span></div>
          <div>
            <h3 class="text-2xl font-bold text-gray-900">遗忘曲线复习提醒</h3>
            <p class="text-gray-600">基于艾宾浩斯遗忘曲线智能安排</p>
          </div>
        </div>
        <span v-if="todayReviews.length > 0" class="badge badge-rose">{{ todayReviews.length }} 项待复习</span>
      </div>
      <div v-if="todayReviews.length === 0" class="text-center py-12">
        <div class="text-8xl mb-6">🎉</div>
        <p class="text-gray-600 text-lg mb-2">今天没有需要复习的内容</p>
        <p class="text-gray-500">继续保持，学习状态很好！</p>
      </div>
      <div v-else class="space-y-4 max-h-96 overflow-y-auto">
        <div v-for="review in todayReviews" :key="review.record_id" class="p-6 border-2 border-[#1a1a2e] transition-all" :class="getUrgencyClass(review.urgency)" style="border-radius: 16px;">
          <div class="flex justify-between items-center">
            <div class="flex-1">
              <p class="text-xl font-bold text-gray-900 mb-2">{{ review.knowledge_point_name }}</p>
              <p class="text-gray-600">已复习 {{ review.review_count }} 次</p>
            </div>
            <div class="flex items-center gap-6">
              <div class="text-right">
                <p class="text-sm text-gray-500 mb-1">掌握度</p>
                <p :class="['text-2xl font-bold', getMasteryColor(review.mastery_level)]">{{ (review.mastery_level * 100).toFixed(0) }}%</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="flex items-center gap-3 mb-8">
        <div class="w-12 h-12 bg-yellow-200 flex items-center justify-center" style="border: 2px solid #1a1a2e; border-radius: 12px;"><span class="text-2xl">💡</span></div>
        <div>
          <h3 class="text-2xl font-bold text-gray-900">备考建议</h3>
          <p class="text-gray-600">针对性学习建议</p>
        </div>
      </div>
      <div class="space-y-4">
        <div class="p-4 bg-pink-100 border-2 border-[#1a1a2e]" style="border-radius: 12px;">
          <h4 class="font-bold text-gray-900 mb-2">📐 高等数学（90分）</h4>
          <p class="text-sm text-gray-700">占总分60%，是考试重点。建议优先学习一元函数微积分和多元函数积分学，掌握基本计算方法和定理应用。</p>
        </div>
        <div class="p-4 bg-cyan-100 border-2 border-[#1a1a2e]" style="border-radius: 12px;">
          <h4 class="font-bold text-gray-900 mb-2">📊 线性代数（30分）</h4>
          <p class="text-sm text-gray-700">注重矩阵运算、向量空间、特征值与特征向量等核心概念的理解，重点掌握线性方程组求解和矩阵对角化。</p>
        </div>
        <div class="p-4 bg-amber-100 border-2 border-[#1a1a2e]" style="border-radius: 12px;">
          <h4 class="font-bold text-gray-900 mb-2">🎲 概率论与数理统计（30分）</h4>
          <p class="text-sm text-gray-700">重点理解随机变量及其分布、多维随机变量、参数估计等核心内容，注意公式的灵活运用。</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const examDate = new Date('2026-12-19')
const daysToExam = ref(Math.ceil((examDate - new Date()) / (1000 * 60 * 60 * 24)))
const weeklyStats = ref({})
const todayReviews = ref([])

const getUrgencyClass = (u) => u === 'overdue' ? 'bg-red-100' : u === 'due_today' ? 'bg-amber-100' : 'bg-yellow-50'
const getMasteryColor = (m) => m >= 0.9 ? 'text-purple-600' : m >= 0.7 ? 'text-pink-600' : m >= 0.5 ? 'text-amber-600' : 'text-red-600'

onMounted(async () => {
  try {
    const [w, r] = await Promise.all([
      axios.get('/api/study/weekly-stats'),
      axios.get('/api/study/today-reviews')
    ])
    weeklyStats.value = w.data
    todayReviews.value = r.data
  } catch (e) { console.error(e) }
})
</script>
