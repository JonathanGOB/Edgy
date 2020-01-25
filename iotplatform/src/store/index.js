import Vue from 'vue'
import Vuex from 'vuex'
import User from "../models/User";
import axios from "axios"
import VuexPersistence from 'vuex-persist'

const vuexLocalStorage = new VuexPersistence({
    storage: window.localStorage
});

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        token: null,
        user: null,
        url: axios.defaults.baseURL = 'http://localhost:5000'
    },
    getters: {
        user: (state) => state.user,
        token:(state) => state.token,
    },

    mutations: {
        setToken: (state, token) => {
            state.token = token;
            axios.defaults.headers.common['Authorization'] = 'Bearer ' + token;
        },

        setUser: (state, user) => {
            state.user = user;
        },

        removeToken: (state, token) => {
            state.token = token;
            delete axios.defaults.headers.common["Authorization"];
        },
    },
    actions: {
        auth({commit}, email, password) {
            return new Promise((resolve, reject) => {
                User.login(email, password).then(response => {
                    const token = response.data.data.access_token
                    commit('setToken', token)

                    const user = response.data.data.user
                    commit('setUser', user)
                    return true
                }).catch(error => {
                    reject(error)
                }).finally(() => {
                    this.loading = false;
                });
            })
        },

        logout({commit, getters}) {
            axios.defaults.headers.common['Authorization'] = 'Bearer ' + getters.token;
            return new Promise((resolve, reject) => {
                User.logout().then(() => {
                    const token = null;
                    commit('removeToken', token);

                    const user = null;
                    commit('setUser', user)
                }).then(() => {
                    resolve()
                }).catch(error => {
                    reject(error);
                })
            })
        },

    },
    modules: {},
    plugins: [vuexLocalStorage.plugin]
})
