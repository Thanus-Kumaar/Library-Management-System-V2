import { createWebHistory, createRouter } from 'vue-router';
import MainPage from './components/MainPage.vue';
import LoginPage from './components/LoginPage.vue';

const routes = [
  { path: '/', component: MainPage },
  { path: '/login', component: LoginPage },
];

const router = createRouter({
  history: createWebHistory(),
  routes: routes
})

export default router;