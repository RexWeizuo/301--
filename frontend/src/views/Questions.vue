<template>
  <div class="fade-in space-y-6">
    <div class="card">
      <div class="flex items-center gap-3">
        <div class="w-12 h-12 bg-pink-200 flex items-center justify-center" style="border: 2px solid #1a1a2e; border-radius: 12px;"><span class="text-2xl">✍️</span></div>
        <div>
          <h1 class="text-3xl font-bold text-gray-900">习题练习</h1>
          <p class="text-gray-600">按科目和章节分类，系统练习巩固知识</p>
        </div>
      </div>
    </div>

    <div class="flex gap-3 flex-wrap">
      <button v-for="s in subjectList" :key="s.id" @click="activeSubject = activeSubject === s.id ? null : s.id"
        :class="['btn text-sm', activeSubject === s.id ? 'btn-primary' : 'btn-secondary']">
        <span>{{ s.icon }}</span><span>{{ s.name }}</span>
      </button>
    </div>

    <div v-if="loading" class="card text-center py-16">
      <div class="pulse inline-block text-6xl mb-4">⏳</div>
      <p class="text-gray-600">加载中...</p>
    </div>

    <div v-else-if="filteredData.length === 0" class="card text-center py-16">
      <div class="text-8xl mb-6">📭</div>
      <p class="text-gray-600 text-lg mb-4">暂无习题</p>
      <p class="text-gray-500">请先添加习题</p>
    </div>

    <div v-else class="space-y-3">
      <template v-for="subject in filteredData" :key="subject.subject_id">
        <div class="tree-node">
          <div @click="toggleNode('subject', subject.subject_id)" 
               class="tree-item tree-item-level-0"
               :class="{ 'expanded': isNodeExpanded('subject', subject.subject_id) }">
            <div class="tree-icon"><span class="tree-icon-bg">{{ subject.subject_icon }}</span></div>
            <span class="tree-label">{{ subject.subject_name }}</span>
            <span class="tree-badge">{{ countQuestions(subject) }} 题</span>
            <svg class="tree-chevron" :class="{ 'rotated': isNodeExpanded('subject', subject.subject_id) }" 
                 fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
            </svg>
          </div>
          <div v-show="isNodeExpanded('subject', subject.subject_id)" class="tree-children">
            <template v-for="chapter in subject.chapters" :key="chapter.chapter_id">
              <div class="tree-node">
                <div @click="toggleNode('chapter', chapter.chapter_id)" 
                     class="tree-item tree-item-level-1"
                     :class="{ 'expanded': isNodeExpanded('chapter', chapter.chapter_id) }">
                  <div class="tree-icon"><span class="tree-icon-bg">📖</span></div>
                  <span class="tree-label">{{ chapter.chapter_name }}</span>
                  <span class="tree-badge level-1">{{ countChapterQuestions(chapter) }} 题</span>
                  <svg class="tree-chevron" :class="{ 'rotated': isNodeExpanded('chapter', chapter.chapter_id) }" 
                       fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                  </svg>
                </div>
                <div v-show="isNodeExpanded('chapter', chapter.chapter_id)" class="tree-children">
                  <template v-for="kp in chapter.knowledge_points" :key="kp.knowledge_point_id">
                    <div class="tree-node">
                      <div @click="toggleNode('kp', kp.knowledge_point_id)" 
                           class="tree-item tree-item-level-2"
                           :class="{ 'expanded': isNodeExpanded('kp', kp.knowledge_point_id) }">
                        <div class="tree-icon"><span class="tree-icon-bg">📝</span></div>
                        <span class="tree-label">{{ kp.knowledge_point_name }}</span>
                        <span class="tree-badge level-2">{{ kp.questions.length }} 题</span>
                        <div class="tree-actions">
                          <button @click.stop="practiceAll(kp.questions)" 
                                  class="tree-action-btn tree-action-btn-primary">
                            开始练习
                          </button>
                        </div>
                        <svg class="tree-chevron" :class="{ 'rotated': isNodeExpanded('kp', kp.knowledge_point_id) }" 
                             fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                        </svg>
                      </div>
                      <div v-show="isNodeExpanded('kp', kp.knowledge_point_id)" class="tree-children tree-children-questions">
                        <div v-for="q in kp.questions" :key="q.id" class="tree-question-item">
                          <div class="tree-question-content">
                            <div class="tree-question-header">
                              <span class="tree-question-text">{{ q.question }}</span>
                              <span class="badge badge-pink">难度 {{ q.difficulty }}</span>
                            </div>
                            <div class="tree-question-options">
                              <div v-for="opt in q.options" :key="opt" class="tree-option">{{ opt }}</div>
                            </div>
                          </div>
                          <router-link :to="`/questions/practice/${q.id}`" class="tree-question-action-btn">
                            答题
                          </router-link>
                        </div>
                      </div>
                    </div>
                  </template>
                </div>
              </div>
            </template>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const activeSubject = ref(null)
const loading = ref(true)
const treeData = ref([])
const expandedNodes = ref(new Set())

const subjectList = [
  { id: 'advanced_math', name: '高等数学', icon: '📐' },
  { id: 'linear_algebra', name: '线性代数', icon: '📊' },
  { id: 'probability', name: '概率论', icon: '🎲' },
  { id: 'three_calc', name: '三大计算', icon: '🔢' }
]

const filteredData = computed(() => {
  if (!activeSubject.value) return treeData.value
  return treeData.value.filter(s => s.subject_id === activeSubject.value)
})

const countQuestions = (subject) => {
  return subject.chapters.reduce((sum, ch) => {
    return sum + ch.knowledge_points.reduce((s, kp) => s + kp.questions.length, 0)
  }, 0)
}

const countChapterQuestions = (chapter) => {
  return chapter.knowledge_points.reduce((sum, kp) => sum + kp.questions.length, 0)
}

const getNodeKey = (type, id) => `${type}:${id}`

const toggleNode = (type, id) => {
  const key = getNodeKey(type, id)
  const newSet = new Set(expandedNodes.value)
  if (newSet.has(key)) newSet.delete(key)
  else newSet.add(key)
  expandedNodes.value = newSet
}

const isNodeExpanded = (type, id) => expandedNodes.value.has(getNodeKey(type, id))

const practiceAll = (questions) => {
  if (questions.length > 0) router.push(`/questions/practice/${questions[0].id}`)
}

onMounted(async () => {
  try {
    const res = await axios.get('/api/questions/grouped?type=choice')
    treeData.value = res.data.subjects
  } catch (e) { console.error(e) } finally { loading.value = false }
})
</script>

<style scoped>
.tree-node { margin-left: 0; }
.tree-children {
  margin-left: 1.5rem;
  border-left: 3px dashed #1a1a2e;
  padding-left: 1rem;
  margin-top: 0.5rem;
}
.tree-item {
  display: flex; align-items: center; gap: 0.75rem;
  padding: 0.75rem 1rem;
  cursor: pointer; transition: all 0.2s ease; user-select: none;
  border: 2px solid transparent;
  border-radius: 12px;
}
.tree-item:hover { background-color: #fef9c3; border-color: #1a1a2e; }
.tree-item-level-0 { background-color: #fce7f3; border: 2px solid #1a1a2e; }
.tree-item-level-0:hover { background-color: #fbcfe8; }
.tree-item-level-1 { background-color: #cffafe; border: 2px solid #1a1a2e; }
.tree-item-level-1:hover { background-color: #a5f3fc; }
.tree-item-level-2 { background-color: #fef3c7; border: 2px solid #1a1a2e; }
.tree-item-level-2:hover { background-color: #fde68a; }
.tree-icon { flex-shrink: 0; }
.tree-icon-bg {
  display: flex; align-items: center; justify-content: center;
  width: 2rem; height: 2rem; border-radius: 8px; font-size: 1rem;
  background: #1a1a2e; color: white;
}
.tree-label { flex: 1; font-weight: 700; color: #1a1a2e; }
.tree-item-level-0 .tree-label { font-size: 1.125rem; }
.tree-item-level-1 .tree-label { font-size: 1rem; }
.tree-item-level-2 .tree-label { font-size: 0.875rem; }
.tree-badge {
  display: inline-flex; align-items: center; padding: 0.25rem 0.75rem;
  border-radius: 8px; font-size: 0.75rem; font-weight: 700;
  background-color: #ec4899; color: white;
  border: 2px solid #1a1a2e;
}
.tree-badge.level-1 {
  background-color: #06b6d4; color: white;
}
.tree-badge.level-2 {
  background-color: #f59e0b; color: white;
}
.tree-chevron { width: 1.25rem; height: 1.25rem; color: #1a1a2e; transition: transform 0.3s ease; flex-shrink: 0; }
.tree-chevron.rotated { transform: rotate(180deg); }
.tree-actions { display: flex; gap: 0.5rem; }
.tree-action-btn {
  padding: 0.375rem 0.75rem; border-radius: 8px; font-size: 0.75rem;
  font-weight: 700; cursor: pointer; border: 2px solid #1a1a2e;
  background-color: white; color: #1a1a2e; transition: all 0.2s ease;
}
.tree-action-btn:hover {
  background-color: #fef9c3;
}
.tree-action-btn-primary {
  background: #ec4899; color: white; border-color: #1a1a2e;
}
.tree-action-btn-primary:hover {
  box-shadow: 3px 3px 0px #1a1a2e; color: white;
}
.tree-children-questions { margin-top: 0.5rem; }
.tree-question-item {
  display: flex; align-items: flex-start; gap: 0.75rem; padding: 0.75rem;
  margin-bottom: 0.5rem; background-color: #fefce8;
  border-radius: 12px; border: 2px solid #1a1a2e; transition: all 0.2s ease;
}
.tree-question-item:hover { background-color: #fef9c3; }
.tree-question-content { flex: 1; min-width: 0; }
.tree-question-header { display: flex; align-items: flex-start; justify-content: space-between; gap: 1rem; margin-bottom: 0.5rem; }
.tree-question-text { flex: 1; color: #1a1a2e; font-size: 0.875rem; line-height: 1.6; font-weight: 500; }
.tree-question-options { display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.5rem; margin-top: 0.5rem; }
.tree-option {
  padding: 0.375rem 0.75rem; background-color: white;
  border-radius: 8px; font-size: 0.75rem; color: #1a1a2e; border: 1px solid #1a1a2e;
}
.tree-question-action-btn {
  flex-shrink: 0; padding: 0.5rem 1rem;
  background: #ec4899; color: white; border-radius: 8px; font-size: 0.75rem; font-weight: 700;
  text-decoration: none; transition: all 0.2s ease; white-space: nowrap; align-self: center;
  border: 2px solid #1a1a2e;
}
.tree-question-action-btn:hover {
  box-shadow: 3px 3px 0px #1a1a2e; transform: translateY(-1px);
}
</style>
