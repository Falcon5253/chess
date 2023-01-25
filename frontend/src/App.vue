<template>
  <div id="app">
    <MenuField />
    <GameView />
  </div>
</template>

<script>
import GameView from './components/GameView.vue'
import MenuField from './components/MenuField.vue'

import Cookies from 'js-cookie'

export default {
  name: 'App',
  components: {
    GameView, MenuField
  },
  mounted() {
    let token = Cookies.get('token')
    if (token != undefined) {
      this.$store.dispatch('SET_TOKEN', token)
    }
    this.$store.dispatch('CHECK_AUTHENTICATION')
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
  display: flex;
}
</style>
