import Vue from 'vue'
import App from './App.vue'
import Vuex from 'vuex'
import VueRouter from 'vue-router'
import Cookies from 'js-cookie'
import Pusher from 'pusher-js';

import LoginView from '@/components/pages/LoginView.vue'
import MainView from '@/components/pages/MainView.vue'
import RegisterView from '@/components/pages/RegisterView.vue'
import FriendList from '@/components/pages/FriendsList.vue'


const pusher = new Pusher('ee05f77136a92920f7e1', {
  cluster: 'eu'
});
Vue.use(Vuex)
Vue.use(VueRouter)


const routes = [
  { path: '/', component: MainView },
  { path: '/:id(\\d+)', component: MainView },
  { path: '/login', component:  LoginView},
  { path: '/register', component:  RegisterView},
  { path: '/friends', component: FriendList },
]


const router = new VueRouter({
  routes,
})

const api = process.env.VUE_APP_API_URL;



const store = new Vuex.Store({
  state: {
    isAuthenticated: false,
    authToken: undefined,
    games: [],
    profile: {},
    currentGame: {},
  },
  getters: {
    isAuthenticated(state) {
      return state.isAuthenticated;
    },
    profile(state) {
      return state.profile;
    },
    token(state) {
      return state.authToken;
    },
    games(state) {
      return state.games;
    },
    getGame(state) {
      return state.currentGame;
    },
  },
  mutations: {
    checkAuthentication (state) {
      if (state.authToken != undefined) {
        state.isAuthenticated = true;
        fetch(api + 'profile/', {
            method: 'get',
            headers: {
              'Authorization': `Bearer ${state.authToken}` 
            },
        })
        .then((res) => {
            if (res.ok) {
                return res.json();
            }
            else {
                throw new Error("Not 2xx response", {cause: res});
            }
        })
        .then((data) => {
          state.profile = data;
        })
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
    },
    getGames(state) {
      const token = Cookies.get('token');
      fetch(api + 'games/', {
          method: 'get',
          headers: {
            'Authorization': `Bearer ${token}` 
          },
      })
      .then((res) => {
          if (res.ok) {
              return res.json();
          }
          else {
              throw new Error("Not 2xx response", {cause: res});
          }
      })
      .then((data) => {
          state.games = data;
      })
    },
    sendTurn(state, data) {
      var formData = new FormData();
      for (let key in data) {
          formData.append(key, data[key]);
      }

      fetch(api + 'games/', {
          method: 'post',
          body: formData,
          headers: {
            'Authorization': `Bearer ${state.authToken}` 
          },
      })
      .then((res) => {
          if (res.ok) {
              return res.json();
          }
          else {
              throw new Error("Not 2xx response", {cause: res});
          }
      })
    },
    updateGame(state, data) {
      let game = state.games.find((game) => game.id == data.id);
      let index = state.games.indexOf(game);
      state.games[index] = data;
      state.currentGame = data;
      console.log(data);
    },
    setCurrentGame(state, id) {
      state.currentGame = state.games.find(game => game.id == id);
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
    },
    GET_GAMES(context) {
      context.commit('getGames');
    },
    SET_CURRENT_GAME(context, id) {
      context.commit('setCurrentGame', id)
    },
    SEND_TURN(context, data) {
      context.commit('sendTurn', data);
    },
    UPDATE_GAME(context, data) {
      context.commit('updateGame', data)
    }
  }
})



Vue.config.productionTip = api;

Vue.prototype.$api = api;
Vue.prototype.$pusher = pusher;

new Vue({
  render: h => h(App),
  store,
  router,
}).$mount('#app')
