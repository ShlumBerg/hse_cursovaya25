import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user-store'

import MainLayout from '@/layouts/MainLayout.vue'
import LoginLayout from '@/layouts/LoginLayout.vue'
import HomeView from '@/views/HomeView.vue'
import FizLitsaView from '@/views/FizLitsaView.vue'
import FizLitsaCreditsView from '@/views/FizLitsaCreditsView.vue'
import YurLitsaView from '@/views/YurLitsaView.vue'
import YurLitsaCreditsView from '@/views/YurLitsaCreditsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginLayout,
      meta: {
        title: 'Вход в систему',
      },
    },
    {
      path: '/',
      component: MainLayout,
      children: [
        {
          path: '/',
          name: 'home',
          component: HomeView,
          meta: {
            requireLogin: true,
            title: 'Главная',
          },
        },
        {
          path: '/fiz-litsa',
          name: 'fiz-litsa',
          component: FizLitsaView,
          meta: {
            requireLogin: true,
            title: 'Физические лица',
          },
        },
        {
          path: '/fiz-litsa-credits',
          name: 'fiz-litsa-credits',
          component: FizLitsaCreditsView,
          meta: {
            requireLogin: true,
            title: 'Кредиты физическим лицам',
          },
        },
        {
          path: '/yur-litsa',
          name: 'yur-litsa',
          component: YurLitsaView,
          meta: {
            requireLogin: true,
            title: 'Юридические лица',
          },
        },
        {
          path: '/yur-litsa-credits',
          name: 'yur-litsa-credits',
          component: YurLitsaCreditsView,
          meta: {
            requireLogin: true,
            title: 'Кредиты юридическим лицам',
          },
        },
      ]
    }
    
  ],
})

router.beforeEach((to, from, next) => {
    const userStore = useUserStore()
    
    document.title = to?.meta?.title as string

    if (to.matched.some((record) => record.meta.requireLogin) && !userStore.isAuthenticated) {
        next({name: 'login'})
    } else if (to.name == 'login' && userStore.isAuthenticated) {
        next('/')
    } else {
        next()
    }
})

export default router
