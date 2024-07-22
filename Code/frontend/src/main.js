import { createApp } from "vue";
import { createWebHistory, createRouter } from 'vue-router';

import App from "./App.vue";
import MainPage from "./components/MainPage.vue";
import Navbar from "./components/Navbar.vue";
import Login from "./components/LoginPage.vue";
import AdminHome from "./components/adminHome.vue";
import UserHome from "./components/userHome.vue";


const router = createRouter({
  history: createWebHistory(),
  routes : [
    { path: '/', component: MainPage },
    { path: '/about', component: Login },
  ]
})

const app = createApp(App)
app.component("MainPage", MainPage)
app.component("Navbar", Navbar)
app.component("Login", Login)
app.component("AdminHome", AdminHome)
app.component("UserHome", UserHome)
app.mount("#app");
