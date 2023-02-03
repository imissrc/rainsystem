<template>
  <div id="app">
    <router-view />
  </div>
</template>
<script>

export default {
  name: 'App'
}
</script>
<style>
html,body,#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
  overflow: hidden;
  /*background: url("assets/bg.jpg") repeat;*/
  background-size: cover;
}
</style>
