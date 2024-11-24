import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import MindMapPage from '../views/MindMapPage.vue'
import ChatPage from '../views/ChatPage.vue'
import CrawlerPage from '../views/CrawlerPage.vue'
import FusionPage from '../views/FusionPage.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'home',
    component: HomePage
  },
  {
    path: '/mindmap',
    name: 'mindmap',
    component: MindMapPage
  },
  {
    path: '/chat',
    name: 'chat',
    component: ChatPage
  },
  {
    path: '/crawler',
    name: 'crawler',
    component: CrawlerPage
  },
  {
    path: '/fusion',
    name: 'fusion',
    component: FusionPage
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router