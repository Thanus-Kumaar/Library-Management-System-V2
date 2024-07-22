import { createApp } from "vue";
import App from "./App.vue";
import mainPage from "./components/MainPage.vue";
import Navbar from "./components/Navbar.vue";
import Login from "./components/LoginPage.vue";
import router from "./router.js";

createApp(App)
  .component("main-page", mainPage)
  .component("Navbar", Navbar)
  .component("Login", Login)
  .mount("#app");
