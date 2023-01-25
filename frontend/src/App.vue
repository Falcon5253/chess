<template>
  <div id="app">
    <MenuField />
    <GameView />
  </div>
</template>

<script>
import GameView from './components/GameView.vue'
import MenuField from './components/MenuField.vue'


function getCookie(cName) {
      const name = cName + "=";
      const cDecoded = decodeURIComponent(document.cookie);
      const cArr = cDecoded .split('; ');
      let res;
      cArr.forEach(val => {
          if (val.indexOf(name) === 0) res = val.substring(name.length);
      })
      return res;
}


export default {
  name: 'App',
  components: {
    GameView, MenuField
  },
  mounted() {
    let token = getCookie('token')
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
