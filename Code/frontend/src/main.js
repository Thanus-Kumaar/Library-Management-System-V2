import { compile, createApp } from "vue";
import { createWebHistory, createRouter } from 'vue-router';

import App from "./App.vue";
import MainPage from "./components/MainPage.vue";
import Navbar from "./components/Navbar.vue";
import Login from "./components/LoginPage.vue";
import AdminHome from "./components/adminHome.vue";
import UserHome from "./components/userHome.vue";
import ReadBooks from "./components/readBooks.vue";
import ManageSections from "./components/manageSections.vue";
import ManageBooks from "./components/manageBooks.vue";
import SearchBooks from "./components/searchBooks.vue";
import UserBooks from "./components/userBooks.vue";
import ManageIssueRevoke from "./components/manageIssueRevoke.vue";
import ErrorPage from "./components/errorPage.vue";

import authPlugin from "./auth/authPlugin";

const routes = [
  { path: '/', component: MainPage },
  { path: '/login', component: Login },
  { path: '/admin-home', component: AdminHome },
  { path: '/user-home', component: UserHome },
  { path: '/read-books', component: ReadBooks },
  { path: '/manage-sections', component: ManageSections },
  { path: '/manage-books', component: ManageBooks },
  { path: '/search-books', component: SearchBooks },
  { path: '/user-books', component: UserBooks },
  { path: '/manage-issue-revoke', component: ManageIssueRevoke },
  { path: '/error-page', component: ErrorPage},
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

const app = createApp(App)
app.use(router)
app.use(authPlugin)
app.component("Navbar", Navbar)
app.mount("#app");
