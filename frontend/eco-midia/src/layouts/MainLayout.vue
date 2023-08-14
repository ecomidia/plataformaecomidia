<template>
  <q-layout view="lHh Lpr lFf">

    <MyHeader></MyHeader>


    <q-page-container class="maxwidth">
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import MyHeader from 'src/components/MyHeader.vue';


import { ref } from 'vue';




</script>
