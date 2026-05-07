import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import './style.css'

import App from './App.vue'
import Dashboard from './views/Dashboard.vue'
import Syllabus from './views/Syllabus.vue'
import SyllabusDetail from './views/SyllabusDetail.vue'
import ChapterDetail from './views/ChapterDetail.vue'
import Questions from './views/Questions.vue'
import QuestionPractice from './views/QuestionPractice.vue'
import StudyPlan from './views/StudyPlan.vue'
import CuiSubjects from './views/CuiSubjects.vue'

const routes = [
  { path: '/', component: Dashboard },
  { path: '/syllabus', component: Syllabus },
  { path: '/syllabus/:subjectId', component: SyllabusDetail },
  { path: '/syllabus/:subjectId/chapters/:chapterId', component: ChapterDetail },
  { path: '/cui', component: CuiSubjects },
  { path: '/cui/:subjectId', component: SyllabusDetail },
  { path: '/cui/:subjectId/chapters/:chapterId', component: ChapterDetail },
  { path: '/questions', component: Questions },
  { path: '/questions/practice/:questionId', component: QuestionPractice },
  { path: '/plan', component: StudyPlan }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')
