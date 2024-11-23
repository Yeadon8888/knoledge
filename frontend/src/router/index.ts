import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import CrawlerPage from '../views/CrawlerPage.vue'
import FusionPage from '../views/FusionPage.vue'

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
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 