<template>
  <div class="fade-in">
    <div class="mb-8">
      <router-link to="/questions" class="text-pink-600 hover:text-pink-700 flex items-center gap-2 mb-4 font-bold">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path></svg>
        返回习题列表
      </router-link>
      <h1 class="text-3xl font-bold text-gray-900">答题练习</h1>
    </div>

    <div v-if="loading" class="card text-center py-16">
      <div class="pulse inline-block text-6xl mb-4">⏳</div>
      <p class="text-gray-600">加载中...</p>
    </div>

    <div v-else-if="!question" class="card text-center py-16">
      <div class="text-8xl mb-6">📭</div>
      <p class="text-gray-600 text-lg">题目不存在</p>
    </div>

    <div v-else class="space-y-6">
      <div class="card">
        <div class="flex items-center justify-between mb-6">
          <span class="badge badge-pink">难度 {{ question.difficulty }}</span>
          <span class="text-sm text-gray-500 font-bold">题目 #{{ question.id }}</span>
        </div>
        
        <h2 class="text-xl font-bold text-gray-900 mb-6">{{ question.question }}</h2>
        
        <div class="space-y-3 mb-6">
          <div v-for="(opt, idx) in question.options" :key="idx"
               @click="selectedAnswer = String.fromCharCode(65 + idx)"
               :class="['option-card', { 
                 'selected': selectedAnswer === String.fromCharCode(65 + idx),
                 'correct': showAnswer && String.fromCharCode(65 + idx) === question.answer,
                 'wrong': showAnswer && selectedAnswer === String.fromCharCode(65 + idx) && selectedAnswer !== question.answer
               }]">
            <span class="w-8 h-8 flex items-center justify-center text-sm font-bold"
                  :class="getOptionClass(idx)">
              {{ String.fromCharCode(65 + idx) }}
            </span>
            <span class="flex-1 font-medium">{{ opt }}</span>
          </div>
        </div>

        <div class="flex gap-3">
          <button @click="submitAnswer" :class="['btn', selectedAnswer ? 'btn-primary' : 'btn-secondary']" :disabled="!selectedAnswer || showAnswer">
            {{ showAnswer ? '已提交' : '提交答案' }}
          </button>
          <button v-if="showAnswer" @click="nextQuestion" class="btn btn-primary">下一题</button>
        </div>

        <div v-if="showAnswer" class="mt-6 p-4 border-2 border-[#1a1a2e]" :class="isCorrect ? 'bg-green-100' : 'bg-red-100'" style="border-radius: 12px;">
          <div class="flex items-center gap-2 mb-2">
            <span class="text-2xl">{{ isCorrect ? '✅' : '❌' }}</span>
            <span class="font-bold" :class="isCorrect ? 'text-green-800' : 'text-red-800'">
              {{ isCorrect ? '回答正确！' : '回答错误' }}
            </span>
          </div>
          <p class="text-sm mb-1"><span class="font-bold">正确答案：</span>{{ question.answer }}</p>
          <p v-if="question.explanation" class="text-sm mt-2"><span class="font-bold">解析：</span>{{ question.explanation }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const question = ref(null)
const selectedAnswer = ref('')
const showAnswer = ref(false)
const loading = ref(true)

const isCorrect = computed(() => showAnswer.value && selectedAnswer.value === question.value?.answer)

const getOptionClass = (idx) => {
  const letter = String.fromCharCode(65 + idx)
  if (!showAnswer.value) {
    return selectedAnswer.value === letter ? 'bg-pink-300 text-gray-900' : 'bg-gray-200 text-gray-700'
  }
  if (letter === question.value.answer) return 'bg-green-300 text-green-900'
  if (selectedAnswer.value === letter) return 'bg-red-300 text-red-900'
  return 'bg-gray-200 text-gray-700'
}

const submitAnswer = async () => {
  if (!selectedAnswer.value || showAnswer.value) return
  showAnswer.value = true
}

const nextQuestion = () => {
  router.push('/questions')
}

onMounted(async () => {
  try {
    const res = await axios.get(`/api/questions/${route.params.questionId}`)
    question.value = res.data
  } catch (e) { console.error(e) } finally { loading.value = false }
})
</script>

<style scoped>
.option-card {
  display: flex; align-items: center; gap: 0.75rem;
  padding: 0.75rem 1rem;
  cursor: pointer; transition: all 0.2s ease;
  border: 2px solid #1a1a2e;
  border-radius: 12px;
  background-color: #fefce8;
}
.option-card:hover { background-color: #fef9c3; }
.option-card.selected { border-color: #ec4899; background-color: #fce7f3; }
.option-card.correct { border-color: #22c55e; background-color: #dcfce7; }
.option-card.wrong { border-color: #ef4444; background-color: #fee2e2; }
</style>
