<template>
  <q-header  class="">
    <q-toolbar class="q-ma-md flex flex-center">
      <div class="gt-sm ">
        <q-btn
          text-color="white"
          flat
          v-for="link in links"
          :key="link.label"
          :label="link.label"
          :to="link.hash"
          class="text-no-wrap header q-mx-md"
        >
        </q-btn>
      </div>
      <div class="lt-md">
        <q-btn class="q-mr-xl" color="white" flat round dense icon="menu">
          <q-menu class="bg-blue text-white" auto-close>
            <q-list>
              <q-item
                clickable
                flat
                v-for="link in links"
                :key="link.label"
                :to="link.hash"
                class="text-no-wrap btn"
              >
                <q-item-section>
                  {{ link.label }}
                </q-item-section>
              </q-item>
            </q-list>
          </q-menu>
        </q-btn>
      </div>
    </q-toolbar>
  </q-header>
</template>

<script setup>
import { ref } from 'vue';

const links = ref([
  { label: 'INÍCIO', hash: '/' },
  { label: 'POSTS', hash: '/posts' },
  { label: 'TEMAS', hash: '/temas' },
  { label: 'HASHTAGS', hash: '/hashtags' },
  { label: 'IMAGENS', hash: '/imagens' },
  { label: 'NEXO', hash: '/nexo' },
  { label: 'SOBRE', hash: '/sobre' },
]);
</script>

<style scoped>
.header{
  font-family: 'Oswald';
font-style: normal;
font-weight: 600;
font-size: 24px;
line-height: 28px;
/* identical to box height, or 117% */


/* Branco */

color: #FFFFFF;
}
</style>
