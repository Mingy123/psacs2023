<script setup>
import { ref, onMounted } from 'vue';
import Plotly from 'plotly.js-dist';

const data = [{
  x: [1,2,3,4],
  y: [10,15,13,17],
  type:"scatter"
}]
const layout = {
  title: "My graph"
}
const plotlyChart1 = ref(null);
const plotlyChart2 = ref(null);
const plotlyChart3 = ref(null);
const n = ref(0)

onMounted(() => {
  Plotly.newPlot(plotlyChart1.value, data, layout, {responsive: true});
  Plotly.newPlot(plotlyChart2.value, data, layout, {responsive: true});
  Plotly.newPlot(plotlyChart3.value, data, layout, {responsive: true});
});

</script>

<template>
<body>
  <h1>The Frontend</h1>
  <button @click="n+=1">{{ n }}</button>
  <p v-if="n == 3">Cool</p>
  <p v-else>Not cool</p>
  <div id="row-1">
    <div class="col">
      <h3>Chart of Data</h3>
      <div ref="plotlyChart1"></div>
    </div>
    <div class="col">
      <h3>Chart of Data</h3>
      <div ref="plotlyChart2"></div>
    </div>
    <div class="col">
      <h3>Chart of Data</h3>
      <div ref="plotlyChart3"></div>
    </div>
  </div>
</body>
</template>

<style scoped>
/* Scoped means only this file */
/* body {
  background-color: aqua;
} */
#row-1 {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
}
.col {
  flex-grow: 1;
}
.col > div {
  width: 100%; /* Adjust the height as needed */
}
</style>