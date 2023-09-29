<script setup>
import { ref } from 'vue';

const n = ref(0)
</script>

<template>
<body>
  <h1>Hello there</h1>
  <button @click="n+=1">{{ n }}</button>
  <p v-if="n == 3">Cool</p>
  <p v-else>Not cool</p>
</body>
</template>

<style scoped>
/* Scoped means only this file */
body {
  background-color: aqua;
}
</style>