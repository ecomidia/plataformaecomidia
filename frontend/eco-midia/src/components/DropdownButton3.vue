<script setup>
import { storeToRefs } from 'pinia';

const props = defineProps(['myStore']);
const { menu3, menuSelected3 } = storeToRefs(props.myStore);
</script>

<template>
  <q-btn-dropdown
    unelevated
    dense
    menu-anchor="bottom end"
    class="dropdown"
    :label="menuSelected3.label"
  >
    <q-list class="mybox">
      <div  v-for="option in menu3" :key="option.id">
        <q-item
        dense
        clickable
        v-close-popup
        @click="props.myStore.changePreSelect3(option.id)"
      >
        <q-item-section class="q-my-sm" style="width:186px">
          <q-item-label class="myheader"  >{{ option.label }}</q-item-label>
          <q-item-label class="mydescription" caption>{{ option.description }}</q-item-label>
        </q-item-section>
      </q-item>
      <q-separator style="background: #A81815;"></q-separator>
      </div>

    </q-list>
  </q-btn-dropdown>
</template>

<style lang="scss" scoped>
.dropdown{
  margin-left: 16px;
  margin-right: 16px;
  font-weight: bold;
  background-color: #F9FAFB;
  border: 1px solid #E5E7EB;
border-radius: 8px;
}

.mybox{
  background: #FFFFFF;
/* Vermelho/02 */

border: 1px solid #A81815;
border-radius: 8px;
}

.myheader{
  font-family: 'Oswald';
font-style: normal;
font-weight: 700;
font-size: 24px;
line-height: 24px;
/* identical to box height, or 100% */

letter-spacing: 0.02em;

/* Vermelho/02 */

color: #A81815;
}

.mydescription{
  font-family: 'Roboto';
font-style: normal;
font-weight: 400;
font-size: 14px;
line-height: 18px;
/* or 129% */


/* Vermelho/02 */

color: #A81815;
}

</style>
