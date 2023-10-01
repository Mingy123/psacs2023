import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/Home.vue'
import Resources from '../views/Resources.vue'
import Shipping from '../views/Shipping.vue'
import Map from '../views/Map.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/resources', name: 'Resource Availability', component: Resources },
    { path: '/shipping', name: 'Shipping Trends', component: Shipping },
    { path: '/map', name: 'World Map', component: Map },
  ]
})

export default router
