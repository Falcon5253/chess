<template>
  <div id="app">
    <MenuField />
    <GameView />
  </div>
</template>

<script>
import GameView from './components/GameView.vue'
import MenuField from './components/MenuField.vue'

export default {
  name: 'App',
  components: {
    GameView, MenuField
  },
  mounted() {
    console.log(this.$store.state.count);
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
