import Vue from 'vue'
import App from './App.vue'
import Vuex from 'vuex'

Vue.use(Vuex)

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
    }
  },
  actions: {
    CHECK_AUTHENTICATION(context) {
      context.commit('checkAuthentication');
    },
    SET_TOKEN(context, token) {
      context.commit('setToken', token);
    }
  }
})

Vue.config.productionTip = false

Vue.prototype.$api = process.env.VUE_APP_API_URL

new Vue({
  render: h => h(App),
  store,
}).$mount('#app')
