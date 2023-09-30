<script setup>
import { ref, onMounted } from 'vue';
import Plotly from 'plotly.js-dist';

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

const layout = {
  title: "My graph"
}
const plotlyChart1 = ref(null);
const plotlyChart2 = ref(null);
const plotlyChart3 = ref(null);
const plotlyChart4 = ref(null);
const n = ref(0)

const notif_items = ref(null)

onMounted(() => {
  Plotly.newPlot(plotlyChart2.value, cap_data, {barmode: 'stack', title: "Resources at TUAS PORT"}, {responsive: true});
  Plotly.newPlot(plotlyChart3.value, data2, {title: "Total Mass of Ore Shipped"}, {responsive: true});
  Plotly.newPlot(plotlyChart4.value, data3, {title: "Total Mass of Oil Shipped"}, {responsive: true});
  postData("http://127.0.0.1:8080/current_data").then((data) => {
    var plot_data = [{
      x: Object.keys(data),
      y: Object.values(data).map(innerDict => innerDict["Total Container Throughput "]),
      type: 'scatter',
      mode: 'lines',
      name: "Historical Data",
      line: {
        color: 'rgb(55, 128, 191)',
        width: 1
      }
    }]
    Plotly.newPlot(plotlyChart1.value, plot_data, {title: "Total Container Throughput (Thousand TEUs)"}, {responsive: true});
    postData("http://127.0.0.1:8080/forecast").then((data) => {
      // console.log(Objectdata);
      console.log(Object.values(data).map(innerDict => innerDict["0"]));
      plot_data.push({
        x: Object.keys(data),
        y: Object.values(data).map(innerDict => innerDict["0"]),
        type: 'scatter',
        mode: "lines",
        name: "Forecast",
        line: {
          color: 'rgb(219, 64, 82)',
          width: 2
        }
      })
      Plotly.newPlot(plotlyChart1.value, plot_data, {title: "Total Container Throughput (Thousand TEUs)"}, {responsive: true});
    });
  });
  makeChart()  
});


function makeChart() {
  data2[0]['x'].push(data2[0]['x'].length+1);
  data2[0]['y'].push((Math.random()-0.5) * Math.random() * 5 + data2[0]['y'][data2[0]['y'].length-1]);
  Plotly.redraw(plotlyChart3.value);

  data3[0]['x'].push(data3[0]['x'].length+1);
  data3[0]['y'].push((Math.random()-0.5) * Math.random() * 5 + data3[0]['y'][data3[0]['y'].length-1]);
  Plotly.redraw(plotlyChart4.value);

  if (data2[0]['y'][data3[0]['y'].length-1] > 10) {
    notif_items.value.push({ title: 'Not Enough Empty Containers!', message: 'TUAS PORT will not have enough Empty Containers in the next two months! Obtain more.'});
  }

  if (data3[0]['y'][data3[0]['y'].length-1] > 25) {
    notif_items.value.push({ title: 'Influx of Ships Imminent!', message: 'Throughput is predicted to increase by 20% next month. Ready additional manpower.'});
  }
  setTimeout(makeChart, 10000);
}

async function postData(url = "", data = {}) {
  // Default options are marked with *
  const response = await fetch(url, {
    method: "POST", // *GET, POST, PUT, DELETE, etc.
    mode: "cors", // no-cors, *cors, same-origin
    cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
    credentials: "same-origin", // include, *same-origin, omit
    headers: {
      "Content-Type": "application/json",
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    redirect: "follow", // manual, *follow, error
    referrerPolicy: "no-referrer", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
    body: JSON.stringify(data), // body data type must match "Content-Type" header
  });
  return response.json(); // parses JSON response into native JavaScript objects
}
</script>

<template>
<body>
  <h1>The Frontend</h1>
  <!-- <button @click="n+=1">{{ n }}</button>
  <p v-if="n == 3">Cool</p>
  <p v-else>Not cool</p> -->
  <div id="row-1">
    <div class="col_double">
      <h3>Throughput Forecast</h3>
      <div ref="plotlyChart1"></div>
    </div>
    <div class="col_double">
      <h3>Resources</h3>
      <div ref="plotlyChart2"></div>
    </div>
    <div class="col_single scrollable">
      <h3><u>Notifications</u></h3>
      <div v-for="notif_info in notif_items">
        <div class="card">
          <svg class="card_image" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M20 17H22V19H2V17H4V10C4 5.58172 7.58172 2 12 2C16.4183 2 20 5.58172 20 10V17ZM9 21H15V23H9V21Z"/></svg>
          <div class="card_content">
            <h4>{{ notif_info.title }}</h4>
            <p>{{ notif_info.message }}</p>
            <a class="close" href="">Close</a>
          </div>
        </div>
        <hr>
    </div>
    </div>
  </div>
  <h3>Shipping Trends</h3>
  <div id="row-2">
    <div class="col_double">
      <div ref="plotlyChart3"></div>
      </div>

    <div class="col_double">
      <div ref="plotlyChart4"></div>
    </div>
  </div>
</body>
</template>

<style scoped>
/* Scoped means only this file */

body {
  padding-left: 50px;
  padding-right: 50px;
  margin: 0;
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

#row-1 {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  gap: 20px;
}

#row-2 {
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
  background-color: whitesmoke;
  outline-style: solid;
  outline-width: 0px;
  padding: 18px;
}
.card {
  display: flex;
  flex-direction: row;
  align-items: center;
}
.card_image {
  padding-right: 10px;
  max-width: 36px;
  height: auto;
}

.card_content {
  margin: 12px;
}

</style>