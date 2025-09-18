import { defineStore } from 'pinia'
import { client } from '@/api/client.gen';
import { authTokenLoginCreate, authTokenLogoutCreate, authUsersMeRetrieve, type CurrentUser } from '@/api'

interface State {
    user?: CurrentUser;
    isAuthenticated: boolean
    loginErrors: string[]
}

export const useUserStore = defineStore('userStore', {
    state: (): State => ({
        user: undefined,
        isAuthenticated: false,
        loginErrors: []
    }),

    actions: {
        async initializeStore() {
            const token = localStorage.getItem('token')
            if (token) {
                this._set_authorization_header(token)
                await this._set_user()
            }
            if (!this.isAuthenticated) this._clear()
        },

        async login(username: string, password: string) {
            this._clear()

            await authTokenLoginCreate({
                body: {
                    username,
                    password,
                },
                throwOnError: true,
            })
                .then((response) => {
                    const token = response?.data?.auth_token
                    this._set_authorization_header(token)
                })
                .then(async () => {
                    await this._set_user()
                })
                .catch((error) => {
                    if (error.response) {
                        for (const errMsg in error.response.data) {
                            this.loginErrors = []
                            this.loginErrors.push(`${errMsg}: ${error.response.data[errMsg]}`)
                        }
                        console.error(JSON.stringify(error.response.data))
                    } else if (error.message) {
                        console.error(JSON.stringify(error.message))
                    } else {
                        console.error(JSON.stringify(error))
                    }
                })
        },

        async logout() {
            await authTokenLogoutCreate({
                throwOnError: true,
            })
                .catch((error) => {
                console.error(error)
            })
            this._clear()
        },

        _set_authorization_header(token: string) {
            client.instance.defaults.headers.common['Authorization'] = 'Token ' + token
            localStorage.setItem('token', token)
        },

        async _set_user() {
            await authUsersMeRetrieve({
                throwOnError: true,
            })
                .then((response) => {
                    this.user = response.data
                    this.isAuthenticated = true
                })
                .catch((error) => {
                    console.error(error)
                })
        },

        _clear() {
            client.instance.defaults.headers.common['Authorization'] = ''
            localStorage.clear()
            this.user = undefined
            this.isAuthenticated = false
            this.loginErrors = []
        }
    }
})
