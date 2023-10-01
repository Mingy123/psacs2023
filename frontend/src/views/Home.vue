<script setup>
import { ref, onMounted } from 'vue';
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

const layout = {
  title: "My graph"
}
const plotlyChart1 = ref(null);
const plotlyChart2 = ref(null);
const plotlyChart3 = ref(null);
const plotlyChart4 = ref(null);
const plotlyChart5 = ref(null);
const n = ref(0)

const notif_items = ref(null)
const admin = ref(false)

onMounted(() => {
  admin.value = (localStorage.isAdmin == 'true')
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
});



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

const sidebarVisible = ref(false)
const notifPopup = ref(false)
function notifClick(event) {
  if (event.target == event.currentTarget) {
    notifPopup.value = false
  }
}
const loginPopup = ref(false)
const loginPassword = ref('')
function loginClick(event) {
  if (event.target == event.currentTarget) {
    loginPopup.value = false
  }
}
function checkLogin() {
  if (loginPassword.value == "rottenlemons") {
    admin.value = true
    localStorage.setItem("isAdmin", true)
  } else {
    admin.value = true
    localStorage.setItem("isAdmin", false)
  }
  loginPassword.value = ''
  loginPopup.value = false
}
</script>

<template>
<body>
  <Transition>
  <div class="sidebar" v-if="sidebarVisible">
    <div class="buttons">
      <div class="sidebarBtn"><RouterLink to="/">Home</RouterLink></div>
      <div class="sidebarBtn"><RouterLink to="/resources">Resource Usage</RouterLink></div>
      <div class="sidebarBtn"><RouterLink to="/shipping">Shipping Trends</RouterLink></div>
    </div>
    <div class="sidebarBottomContainer">
      <div class="sidebarBottom" @click="notifPopup = true">
        <svg fill="#ff4f4f" width="26px" class="notif-icon" viewBox="0 0 448 512">
          <path d="M224 0c-17.7 0-32 14.3-32 32V49.9C119.5 61.4 64 124.2 64 200v33.4c0 45.4-15.5 89.5-43.8 124.9L5.3 377c-5.8 7.2-6.9 17.1-2.9 25.4S14.8 416 24 416H424c9.2 0 17.6-5.3 21.6-13.6s2.9-18.2-2.9-25.4l-14.9-18.6C399.5 322.9 384 278.8 384 233.4V200c0-75.8-55.5-138.6-128-150.1V32c0-17.7-14.3-32-32-32zm0 96h8c57.4 0 104 46.6 104 104v33.4c0 47.9 13.9 94.6 39.7 134.6H72.3C98.1 328 112 281.3 112 233.4V200c0-57.4 46.6-104 104-104h8zm64 352H224 160c0 17 6.7 33.3 18.7 45.3s28.3 18.7 45.3 18.7s33.3-6.7 45.3-18.7s18.7-28.3 18.7-45.3z"/>
        </svg>
        <p>Notifications</p>
      </div>
      <div :key="admin" class="sidebarBottom" @click="loginPopup = true">
        <svg v-if="admin != true" width="26px" viewBox="0 0 448 512"><path d="M144 144v48H304V144c0-44.2-35.8-80-80-80s-80 35.8-80 80zM80 192V144C80 64.5 144.5 0 224 0s144 64.5 144 144v48h16c35.3 0 64 28.7 64 64V448c0 35.3-28.7 64-64 64H64c-35.3 0-64-28.7-64-64V256c0-35.3 28.7-64 64-64H80z"/></svg>
        <svg v-else width="26px" viewBox="0 0 576 512"><path d="M352 144c0-44.2 35.8-80 80-80s80 35.8 80 80v48c0 17.7 14.3 32 32 32s32-14.3 32-32V144C576 64.5 511.5 0 432 0S288 64.5 288 144v48H64c-35.3 0-64 28.7-64 64V448c0 35.3 28.7 64 64 64H384c35.3 0 64-28.7 64-64V256c0-35.3-28.7-64-64-64H352V144z"/></svg>
        <p>Admin Login</p>
      </div>
    </div>
  </div>
  </Transition>
  <div class="content">
    <div class="sidebarIcon" @click="sidebarVisible = !sidebarVisible">
      <svg height="1em" viewBox="0 0 448 512"><path d="M0 96C0 78.3 14.3 64 32 64H416c17.7 0 32 14.3 32 32s-14.3 32-32 32H32C14.3 128 0 113.7 0 96zM0 256c0-17.7 14.3-32 32-32H416c17.7 0 32 14.3 32 32s-14.3 32-32 32H32c-17.7 0-32-14.3-32-32zM448 416c0 17.7-14.3 32-32 32H32c-17.7 0-32-14.3-32-32s14.3-32 32-32H416c17.7 0 32 14.3 32 32z"/></svg>
    </div>
    <h1>The Frontend</h1>
    <div id="row-1">
      <div class="col_single">
        <h3>Throughput Forecast</h3>
        <div ref="plotlyChart1"></div>
      </div>
      <div class="col_single">
        <h3>Resources (current)</h3>
        <div ref="plotlyChart2"></div>
      </div>
      <div class="col_single">
        <h3>Resrouces (forecast)</h3>
        <div ref="plotlyChart5"></div>
      </div>
    </div>
  
  </div>
  <Transition>
  <div @click="notifClick" v-if="notifPopup" class="popup">
    <div class="popup-content">
      <h1>Stuff</h1>
      <h2>Stuff (scrollable)</h2>
      <h1>Stuff</h1>
      <h2>Stuff (scrollable)</h2>
      <h1>Stuff</h1>
      <h2>Stuff (scrollable)</h2>
      <h1>Stuff</h1>
      <h2>Stuff (scrollable)</h2>
      <h1>Stuff</h1>
      <h2>Stuff (scrollable)</h2>
      <h1>Stuff</h1>
      <h2>Stuff (scrollable)</h2>
    </div>
  </div>
  </Transition>
  <Transition>
  <div @click="loginClick" v-if="loginPopup" class="popup">
    <div class="popup-content login-content">
      <p><u>Login to update current data</u></p>
      <input placeholder="password" type="password" v-model="loginPassword" @keyup.enter="checkLogin">
      <button @click="checkLogin">Submit</button>
    </div>
  </div>
  </Transition>
</body>
</template>

<style scoped>
.v-enter-active, .v-leave-active {
  transition: opacity 0.2s ease;
}
.v-enter-from, .v-leave-to {
  opacity: 0;
}

.popup {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}
.popup-content {
  background: white;
  padding: 10px 5vw;
  border-radius: 10px;
  text-align: center;
  overflow-y: auto;
  max-height: 70vh;
  max-width: 80vw;
  scrollbar-width: 0;
  &::-webkit-scrollbar { display: none; }
}

.login-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  & input {
    width: 70%;
    min-width: 25vw;
    padding: 10px;
    border: 1px solid #dcdcdc;
    background-color: hsl(276, 40%, 95%);
    border-radius: 5px;
    margin-bottom: 8px;
    font-size: 16px;
    text-align: center;
    transition: border-color 0.2s ease;
    &:focus {
      outline: none;
      border-color: #0074d9;
    }
  }
  & button {
    background-color: #d8c3a5;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    margin: 4px 8px;
    font-size: 16px;
    transition: filter 0.3s ease;
    &:hover {
      filter: contrast(1.3);
    }
  }
}

.sidebarIcon {
  position: absolute;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 8px;
  width: 2em;
  height: 2em;
  border-radius: 50%;
  background-color: #bbb;
  transition: background-color 0.2s ease;
  &:hover {
    background-color: #999;
    cursor: pointer;
  }
}

.sidebar {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 16px;
  background-color: #d8c3a5;
  &.buttons {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  &.v-enter-active, &.v-leave-active {
    transition: flex 0.2s ease;
    min-width: 0;
  }
  &.v-enter-from, &.v-leave-to {
    flex: 0;
  }
}


.sidebarBtn {
  background-color: hsl(6, 73%, 68%);
  font-size: 24px;
  width: 100%;
  margin: 8px 0;
  padding: 16px 4px;
  text-align: center;
  border-radius: 8px;
  transition: background-color 0.2s ease;
  & a {
    text-decoration: none;
    color: #333;
  }
  &:hover {
    background-color: hsl(6, 63%, 55%);
    cursor: pointer;
    & a {
      color: #ddd;
    }
  }
}

.sidebarBottom {
  margin-top: 12px;
  background-color: #eae7dc;
  display: flex;
  justify-content: space-evenly;
  border-radius: 8px;
  transition: filter 0.1s ease;
  &:hover {
    cursor: pointer;
    filter: brightness(0.9);
  }
  & p {
    font-size: 24px;
    margin: 16px 0px;
  }
}

.content {
  flex: 4;
  overflow-x: auto;
  overflow-y: auto;
}

body {
  display: flex;
  height: 100vh;
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


.row {
  flex-direction: row;
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