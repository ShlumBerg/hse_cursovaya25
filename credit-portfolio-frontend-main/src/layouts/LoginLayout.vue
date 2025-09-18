<template>
    <div class="flex flex-col justify-center items-center h-screen">
        <NCard
            style="width: 50%;"
        >
            <h2 class="text-center font-semibold">
                Вход в систему
            </h2>

            <n-form ref="formRef" size="small" :model="form" :rules="formRules" class="w-full">
                <n-form-item path="username"  label="Логин">
                    <NInput size="small" v-model:value="form.username" placeholder="Введите логин" class="w-full" @keydown.enter.prevent="submit" />
                </n-form-item>
                <n-form-item path="password" label="Пароль">
                    <NInput type="password" size="small" v-model:value="form.password" placeholder="Введите пароль" class="w-full" @keydown.enter.prevent="submit" />
                </n-form-item>
                <div class="flex justify-center">
                    <n-button type="info" size="small" @click="submit">
                        Войти
                    </n-button>
                </div>
            </n-form>
        </NCard>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import {
    NForm, NFormItem, NInput, NCard, NButton,
    type FormRules, type FormItemRule, type FormValidationError,
    useMessage,
} from 'naive-ui';
import { useUserStore } from '@/stores/user-store'

const router = useRouter();

const messgae = useMessage();

const userStore = useUserStore();

const formRef = ref();

const form = ref({
    username: null,
    password: null,
})

const formRules: FormRules = {
    username: {
        required: true,
        validator(rule: FormItemRule, value: string) {
            if (!value) {
                return new Error('Введите значение')
            }
            return true
        },
    },
    password: {
        required: true,
        validator(rule: FormItemRule, value: string) {
            if (!value) {
                return new Error('Введите значение')
            }
            return true
        },
    },
}


async function submit(e: Event) {
    e.preventDefault()

    formRef.value?.validate(async (errors: Array<FormValidationError> | undefined) => {
        if (!errors) {
            await userStore.login(form.value.username, form.value.password)
            if (userStore.isAuthenticated) router.push('/')
            else {
                messgae.error('При входе в систему произошла ошибка! Проверьте корректность введенных данных.')
            }
        }
    })
}

</script>


<style lang="css" scoped>
  .page {
    padding: 1rem;
  }
</style>