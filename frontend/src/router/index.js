import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/Home.vue'
import Resources from '../views/Resources.vue'
import Shipping from '../views/Shipping.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/resources', name: 'resources', component: Resources },
    { path: '/shipping', name: 'shipping', component: Shipping },
  ]
})

export default router
