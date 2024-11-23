import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import CrawlerPage from '../views/CrawlerPage.vue'

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
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 