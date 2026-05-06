<template>
  <div class="min-h-screen" style="background-color: #fefce8; background-image: radial-gradient(circle at 20% 50%, rgba(236,72,153,0.06) 0%, transparent 50%), radial-gradient(circle at 80% 20%, rgba(6,182,212,0.06) 0%, transparent 50%), radial-gradient(circle at 50% 80%, rgba(245,158,11,0.06) 0%, transparent 50%);">
    <nav class="sticky top-0 z-50 bg-white border-b-[3px] border-[#1a1a2e] shadow-[0_4px_0_#1a1a2e]">
      <div class="max-w-7xl mx-auto px-6 lg:px-8">
        <div class="flex justify-between h-16 items-center">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 flex items-center justify-center text-white font-bold text-lg" style="background: #1a1a2e; border: 2px solid #ec4899; border-radius: 12px;">
              301
            </div>
            <span class="text-xl font-bold gradient-text">学习系统</span>
          </div>
          <div class="flex items-center gap-1">
            <router-link
              v-for="item in navItems"
              :key="item.path"
              :to="item.path"
              :class="['nav-link', { 'active': isActive(item.path) }]"
            >
              <span class="text-lg">{{ item.icon }}</span>
              <span>{{ item.name }}</span>
            </router-link>
          </div>
        </div>
      </div>
    </nav>
    <main class="max-w-7xl mx-auto py-8 px-6 lg:px-8">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
const route = useRoute()

const navItems = [
  { path: '/', name: '仪表盘', icon: '📊' },
  { path: '/syllabus', name: '考纲', icon: '📚' },
  { path: '/questions', name: '习题', icon: '✍️' },
  { path: '/plan', name: '规划', icon: '📅' }
]

const isActive = (path) => {
  if (path === '/') return route.path === '/'
  return route.path.startsWith(path)
}
</script>
