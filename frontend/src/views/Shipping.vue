<script setup>
import { ref, onMounted } from 'vue';
import Plotly from 'plotly.js-dist';

const plotlyChart3 = ref(null);
const plotlyChart4 = ref(null);

const data2 = [{
  x: [1,2,3,4],
  y: [3,5,2,6],
  type:"scatter"
}]

const data3 = [{
  x: [1,2,3,4],
  y: [21,25,24,22],
  type:"scatter"
}]

onMounted(() => {
  Plotly.newPlot(plotlyChart3.value, data2, {title: "Total Mass of Ore Shipped"}, {responsive: true});
  Plotly.newPlot(plotlyChart4.value, data3, {title: "Total Mass of Oil Shipped"}, {responsive: true});
  makeChart();
});

function makeChart() {
  data2[0]['x'].push(data2[0]['x'].length+1);
  data2[0]['y'].push((Math.random()-0.5) * Math.random() * 5 + data2[0]['y'][data2[0]['y'].length-1]);
  Plotly.redraw(plotlyChart3.value);

  data3[0]['x'].push(data3[0]['x'].length+1);
  data3[0]['y'].push((Math.random()-0.5) * Math.random() * 5 + data3[0]['y'][data3[0]['y'].length-1]);
  Plotly.redraw(plotlyChart4.value);

  if (data2[0]['y'][data2[0]['y'].length-1] > 10) {
    add_notif({ title: 'Not Enough Empty Containers!', message: 'TUAS PORT will not have enough Empty Containers in the next two months! Obtain more.'});
  }

  if (data3[0]['y'][data3[0]['y'].length-1] > 25) {
    add_notif({ title: 'Influx of Ships Imminent!', message: 'Throughput is predicted to increase by 20% next month. Ready additional manpower.'});
  }
  setTimeout(makeChart, 10000);
}

function add_notif(s) { // localStorage notifications: { title:str, message:str }
  let n = localStorage.getItem("notifications");
  let notifs = n ? JSON.parse(n) : [];
  notifs.push(s);
  localStorage.setItem("notifications", JSON.stringify(notifs));
}

</script>
<template>
  <div class="backBtn">
    <RouterLink to="/"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0"/><span class="material-symbols-outlined">home</span></RouterLink>
  </div>
  <h1>Shipping Trends</h1>
  <div id="row-2">
    <div class="col_double">
      <div ref="plotlyChart3"></div>
      </div>

    <div class="col_double">
      <div ref="plotlyChart4"></div>
    </div>
  </div>
</template>
<style>
#row-2 {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  gap: 20px;
}


.col_double {
  flex-grow: 2;
}

h1 {
  font-family: Arial, Helvetica, sans-serif;
  font-size: 5em;
  text-align: center;
}

h3 {
  font-family: Arial, Helvetica, sans-serif;
  font-size: 1.5em;
  text-align: center;
}

h4 {
  font-family: Arial, Helvetica, sans-serif;
  font-size: 1.1em;
  margin-top: 0px;
}
</style>