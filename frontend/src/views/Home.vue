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

const notif_items = ref(
  [{ title: 'Not Enough Empty Containers!', 
  message: 'TUAS PORT will not have enough Empty Containers in the next two months! Obtain more.'}, 
  { title: 'Influx of Ships Imminent!', 
  message: 'Throughput is predicted to increase by 20% next month. Ready additional manpower.'}])

onMounted(() => {
  Plotly.newPlot(plotlyChart1.value, data, {title: "Total Container Throughput (Thousand TEUs)"}, {responsive: true});
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
    <div class="col_double">
      <h3>Chart of Data</h3>
      <div ref="plotlyChart1"></div>
    </div>
    <div class="col_double">
      <h3>Chart of Data</h3>
      <div ref="plotlyChart2"></div>
    </div>
    <div class="col_single scrollable">
      <div class="card" v-for="notif_info in notif_items">
        <svg class="card_image" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M20 17H22V19H2V17H4V10C4 5.58172 7.58172 2 12 2C16.4183 2 20 5.58172 20 10V17ZM9 21H15V23H9V21Z"/></svg>
        <div class="card_content">
          <h3>{{ notif_info.title }}</h3>
          <p>{{ notif_info.message }}</p>
          <a class="close" href=""><u>close</u></a>
        </div>
     </div>
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
  gap: 20px;
}
.col_double {
  flex-grow: 2;
}
.col_single {
  flex-grow: 1;
  width: 200px;
}
.scrollable {
  overflow-x: hidden;
  overflow-y: auto;
  outline-style: solid;
}
.card {
  display: flex;
  flex-direction: row;
  padding: 10px;
  align-items: center;
}
.card_image {
  padding-right: 10px;
  max-width: 36px;
  height: auto;
}

</style>