<template>

  <DatePicker  v-model.range="range"  expanded  locale="pt-br" />

</template>

<script setup>

import { storeToRefs } from "pinia";
import {  DatePicker } from 'v-calendar';
import 'v-calendar/dist/style.css';

const props = defineProps(['calendarStore']);
const {range} = storeToRefs(props.calendarStore);

</script>

<style >

.vc-container{
  background: #FFFFFF;
/* Vermelho/02 */

border: 1px solid #A81815;
border-radius: 8px;

--vc-nav-title-colo: red;
}

.vc-nav-header>button{
  background-color: transparent !important;
}
.vc-nav-items>button{
  background-color: transparent !important;
  color:#A81815

}

.vc-nav-items>button.is-active{
  background-color: transparent !important;
  color:#A81815

}


.on-left{
  margin-right:0px
}
.on-right{
  margin-left:0px
}

.vc-day-content {
  color: #A81815;
  font-family: 'Inter';
font-style: normal;
font-weight: 600;
font-size: 13px;
line-height: 20px;
}

.vc-highlight{
  background-color: #ffa1a1!important;
  border-width: 0px!important;
}

.vc-weekday{
  color:#a8171562;
}

.vc-title{
  font-family: 'Roboto';
font-style: normal;
font-weight: 600;
font-size: 13px;
line-height: 20px;
/* identical to box height, or 154% */

display: flex;
align-items: flex-end;
text-align: center;

/* Vermelho/02 */

color: #A81815;
}

button.vc-title{
  background-color: transparent;
}
button.vc-title>span{
    color: #A81815;
  
}



button.vc-arrow.vc-prev{
  background-color: transparent;
  color: #A81815;

}
button.vc-arrow.vc-next{
  background-color: transparent;
  color: #A81815;

}

</style>
