import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomePage
    },
    {
      path: '/chat',
      name: 'chat',
      component: () => import('../views/ChatPage.vue')
    },
    {
      path: '/crawler',
      name: 'crawler',
      component: () => import('../views/CrawlerPage.vue')
    },
    {
      path: '/fusion',
      name: 'fusion',
      component: () => import('../views/FusionPage.vue')
    },
    {
      path: '/mindmap',
      name: 'mindmap',
      component: () => import('../views/MindmapPage.vue')
    },
    {
      path: '/search',
      name: 'search',
      component: () => import('../views/SearchPage.vue')
    }
  ]
})

export default router