import { createApp } from "vue";
import App from "./App.vue";
import mainPage from "./components/MainPage.vue";
import Navbar from "./components/Navbar.vue";

createApp(App)
  .component("main-page", mainPage)
  .component("navbar", Navbar)
  .mount("#app");
