import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import CrawlerPage from '../views/CrawlerPage.vue'
import FusionPage from '../views/FusionPage.vue'
import MindMapPage from '../views/MindMapPage.vue'
import SearchPage from '../views/SearchPage.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'HomePage',
    component: HomePage
  },
  {
    path: '/crawler',
    name: 'CrawlerPage',
    component: CrawlerPage
  },
  {
    path: '/fusion',
    name: 'FusionPage',
    component: FusionPage
  },
  {
    path: '/search',
    name: 'SearchPage',
    component: SearchPage
  },
  {
    path: '/mindmap',
    name: 'MindMapPage',
    component: MindMapPage
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router