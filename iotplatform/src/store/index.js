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
    },
    getters: {
        user: (state) => state.user,
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
        auth({commit}, {email, password}) {
            User().login(email, password).then(response => {
                const token = response.access_token
                commit('setToken', token)

                const user = response.user
                commit('setUser', user)
                return true
            }).catch(error => {
                return error;
            })
        },

      logout({commit}) {
        User().logout().then(() => {
          const token = null
          commit('removeToken', token)

          const user = null
          commit('setUser', user)
          return true
        }).catch(error => {
          return error;
        })
      },

    },
    modules: {},
    plugins: [vuexLocalStorage.plugin]
})
