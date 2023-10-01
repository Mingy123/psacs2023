<script setup>
import { onMounted, ref } from 'vue';
import Plotly from 'plotly.js-dist';

const capacity_data = {
  x: ['Reefer', 'DG', 'Total'],
  y: [58, 45, 72],
  name: 'Used',
  type: 'bar'
}

const total_capacity = {
  x: ['Reefer', 'DG', 'Total'],
  y: [100-58, 100-45, 100-72],
  name: 'Remaining',
  type: 'bar'
};

var cap_data = [capacity_data, total_capacity]
const plotlyChart2 = ref(null);
const plotlyChart5 = ref(null);
//  static data as we dont have real access to reefer/dg data
onMounted(() => {
  Plotly.newPlot(plotlyChart2.value, cap_data, {barmode: 'stack', title: "Resources at TUAS PORT"}, {responsive: true});
  const demo_data = [{
      x: [1,2,3,4,5,6,7,8,9],
      y: [78, 66, 53, 36, 42, 68, 33, 56, 46],
      type: 'scatter',
      mode: 'lines',
      name: "Reefer Use",
      line: {
        color: 'rgb(55, 128, 191)',
        width: 2
      }
    },
    {
      x: [9, 10, 11, 12],
      y: [46, 55, 69, 77],
      type: 'scatter',
      mode: 'lines',
      name: "Reefer Use (Prediction)",
      line: {
        color: 'rgb(219, 64, 82)',
        width: 3
      }
    },
    {
      x: [1,2,3,4,5,6,7,8,9],
      y: [33, 36, 45, 34, 31, 40, 33, 37, 38],
      type: 'scatter',
      mode: 'lines',
      name: "DG Use",
      line: {
        color: 'rgb(255, 204, 102)',
        width: 2
      }
    },
    {
      x: [9, 10, 11, 12],
      y: [38, 40, 36, 35],
      type: 'scatter',
      mode: 'lines',
      name: "DG Use (Prediction)",
      line: {
        color: 'rgb(255, 153, 0)',
        width: 3
      }
    }]
  Plotly.newPlot(plotlyChart5.value, demo_data, {
    title: "Resource use %",
    shapes: [
    {
        type: 'line',
        yref: 'paper',
        x0: 9,
        y0: 0,
        x1: 9,
        y1: 1,
        line:{
            color: 'rgb(0, 0, 0)',
            width: 3,
            dash:'dot'
        }
    }
    ]
  }, {responsive: true});
})
</script>

<template>
  <div class="backBtn">
    <RouterLink to="/"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0"/><span class="material-symbols-outlined">home</span></RouterLink>
  </div>
  <div id="row-1">
    <div class="col_single">
      <h3>Resources (current)</h3>
      <div ref="plotlyChart2"></div>
    </div>
    <div class="col_single">
      <h3>Resrouces (forecast)</h3>
      <div ref="plotlyChart5"></div>
    </div>
  </div>
</template>

<style scoped>
#row-1 {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  gap: 20px;
  margin: 0 5%;
  width: 90%;
}
.col_single {
  flex-grow: 1;
  width: 200px;
}
</style>