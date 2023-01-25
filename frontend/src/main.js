import Vue from 'vue'
import App from './App.vue'
import Vuex from 'vuex'
import VueRouter from 'vue-router'


import LoginView from '@/components/pages/LoginView.vue'
import MainView from '@/components/pages/MainView.vue'
import RegisterView from '@/components/pages/RegisterView.vue'




Vue.use(Vuex)
Vue.use(VueRouter)


const routes = [
  { path: '/login', component:  LoginView},
  { path: '/register', component:  RegisterView},
  { path: '/', component: MainView },
]


const router = new VueRouter({
  routes,
})





const store = new Vuex.Store({
  state: {
    isAuthenticated: false,
    authToken: undefined
  },
  getters: {
    isAuthenticated(state) {
      return state.isAuthenticated;
    },
    token(state) {
      return state.authToken;
    }
  },
  mutations: {
    checkAuthentication (state) {
      if (state.authToken != undefined) {
        state.isAuthenticated = true;
      }
      else {
        state.isAuthenticated = false;
      }
    },
    setToken (state, token ) {
      state.authToken = token;
    },
    toggleIsAuthenticated(state) {
      state.isAuthenticated = !state.isAuthenticated;
    }
  },
  actions: {
    CHECK_AUTHENTICATION(context) {
      context.commit('checkAuthentication');
    },
    SET_TOKEN(context, token) {
      context.commit('setToken', token);
    },
    TOGGLE_IS_AUTHENTICATED(context) {
      context.commit('toggleIsAuthenticated');
    }
  }
})



Vue.config.productionTip = false

Vue.prototype.$api = process.env.VUE_APP_API_URL

new Vue({
  render: h => h(App),
  store,
  router,
}).$mount('#app')
