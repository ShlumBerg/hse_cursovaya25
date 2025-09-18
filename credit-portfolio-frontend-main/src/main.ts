import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import { useUserStore } from '@/stores/user-store'

const app = createApp(App)

const pinia = createPinia()

const userStore = useUserStore(pinia)

userStore.initializeStore().then(() => {
    app.use(pinia)
    app.use(router)
    app.mount('#app')
})
