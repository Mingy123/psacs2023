<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <RouterView />
  <div id="snackbar">Snackbar</div>
</template>

<style>
body {
  margin: 0;
  padding: 0;
  background-color: #eae7dc;
}

.backBtn {
  position: absolute;
  left: 0;
  top: 0;
  right: 0;
  bottom: 0;
  margin: 8px 0 0 8px;
}

#snackbar {
  visibility: hidden;
  min-width: 250px;
  margin-left: -125px;
  background-color: hsl(45, 2%, 25%);
  color: #fff;
  text-align: center;
  border-radius: 2px;
  padding: 16px;
  position: fixed;
  z-index: 1;
  left: 50%;
  bottom: 30px;
} 
  
#snackbar.show {
  visibility: visible;
  -webkit-animation: fadein 0.2s, fadeout 0.2s 2.3s;
  animation: fadein 0.2s, fadeout 0.2s 2.3s;
} 
  
@-webkit-keyframes fadein {
  from {bottom: 0; opacity: 0;}
  to {bottom: 30px; opacity: 1;}
}

@keyframes fadein {
  from {bottom: 0; opacity: 0;}
  to {bottom: 30px; opacity: 1;}
}

@-webkit-keyframes fadeout {
  from {bottom: 30px; opacity: 1;}
  to {bottom: 0; opacity: 0;}
}

@keyframes fadeout {
  from {bottom: 30px; opacity: 1;}
  to {bottom: 0; opacity: 0;}
}
</style>