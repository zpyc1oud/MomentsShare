import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

// Vant 样式
import 'vant/lib/index.css'

// 全局样式 (放在 Vant 样式后面以便覆盖)
import './assets/styles/global.scss'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
