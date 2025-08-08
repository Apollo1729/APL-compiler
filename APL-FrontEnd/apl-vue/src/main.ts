import { createApp } from "vue";
import VueToast from "vue-toast-notification";
import 'vue-toast-notification/dist/theme-sugar.css';
import App from "./App.vue";
import './style.css'

const app = createApp(App);

app.use(VueToast);
app.mount("#app");
