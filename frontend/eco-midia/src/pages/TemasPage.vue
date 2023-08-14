<template>
  <q-page class="column">
    <div class="filter flex items-center justify-center q-pa-md">
      <span class="text1">Visualize por</span>
      <DropdownButton style="width:186px" class="btn1" :my-store="chartStore">
      </DropdownButton>
      <span  class="text1">definido por</span>
      <DropdownButton2  class="btn1" :my-store="chartStore">
      </DropdownButton2>
      <span v-if="chartStore.menuSelectedIndex2 == 1" class="text1">de</span>
      <span v-if=" chartStore.menuSelectedIndex2 == 0" class="text1">das últimas</span>
      <div >
        <q-btn-dropdown v-if=" chartStore.menuSelectedIndex2 == 1"  class="btn1" :label="calendarStore.getPeriodo">

          <DatePicker :calendarStore="calendarStore"></DatePicker>

        </q-btn-dropdown>
      </div>
      <DropdownButton3 v-if="chartStore.menuSelectedIndex2 == 0" class="btn1" :my-store="chartStore">
      </DropdownButton3>

      <q-btn class="btn1" label="Filtrar"  @click="getData()"></q-btn>

    </div>

    <div class="temas">
      <span class="header">
        TEMAS
      </span>
      <span class="subheader">assuntos que a comunidade discute nas redes</span>
      <q-separator class="q-mt-md" style="background: #6B7280;" size="2px"></q-separator>
      <div class="row q-mt-md subfilter">
        <div class="col-auto">
          <span>REDES SOCIAIS</span>
          <q-checkbox color="black" v-model="item.value" :label="item.name" :disable="item.disable" v-for="item in social"
            :key="item.name" />
        </div>
        <div class="col"></div>
        <div class="col-auto">
          <span>GRÁFICO</span>
          <q-radio color="black" :name="item.name" v-model="tipo.selected" :val="item.value" :label="item.label"
            v-for="item in tipo.options" :key="item.name" />
        </div>
      </div>
      <q-separator class="q-mt-md" style="background: #6B7280;" size="2px"></q-separator>
      <!-- <div class="" style="margin-top: 40px;">
        <masonry-wall class="q-pt-xl" :items="statusStore.entities" :ssr-columns="1" :column-width="300" :gap="16">
        <template #default="{ item }">
          <div class="twittertree flex flex-center" :style="`height: ${relativeHeight(statusStore.entities,item)}px; width: 100%;`">
            <span class="treetext">
              {{ item.entities__name }}
            </span>
          </div>
        </template>
      </masonry-wall>

      </div> -->

      <div class="" style="margin-top: 40px;">
        <masonry-wall v-if="tipo.selected == 'arvore'" class="q-pt-xl" :items="statusStore.entities" :ssr-columns="1"
          :column-width="300" :gap="16">
          <template #default="{ item }">
            <div class="twittertree flex flex-center"
              :style="`height: ${relativeHeight(statusStore.entities, item)}px; width: 100%;`">
              <span class="treetext">
                {{ item.entities__name }}
              </span>
            </div>
          </template>
        </masonry-wall>


        <table v-if="tipo.selected == 'tabela'" style="width:100%">
          <tr>
            <th class="q-pb-md" style="width:70%"></th>
            <th class="q-pb-md" v-for="item in socialMedias" :key="item.name"><q-icon class="col-auto" size="24px"
                :name="item.icon" :style="'color:' + item.color"></q-icon></th>
          </tr>
          <tr v-for="item in statusStore.entities" :key="item.entities__name">
            <td class="q-py-xs q-px-md">{{ item.entities__name }}</td>
            <td style="text-align: center;" class="q-py-xs q-px-md">{{ item.total }}</td>
            <td style="text-align: center;" class="q-py-xs q-px-md">---</td>
            <td style="text-align: center;" class="q-py-xs q-px-md">---</td>
          </tr>

        </table>

        <div v-if="tipo.selected == 'barras'">
          <h1>Twitter</h1>
          <div class="row items-end">
            <div class="q-px-sm col" v-for="item in statusStore.entities.slice(0, 8)" :key="item.entities__name">
              <div class="twittertree flex flex-center"
                :style="`height: ${relativeHeight(statusStore.entities, item)}px; width: 100%;`">
                <span class="treetext">

                </span>
              </div>


            </div>
          </div>
          <q-separator class="q-mt-md" style="background: #6B7280;" size="2px"></q-separator>
          <div class="row">
            <div class="q-px-md q-mt-sm col" v-for="item in statusStore.entities.slice(0, 8)" :key="item.entities__name">
              <span class="barraheader">{{ item.entities__name }}</span>
              <div class="barravalue q-py-md">{{ item.total }}</div>


            </div>
          </div>
        </div>





      </div>


    </div>



  </q-page>
</template>

<script setup lang="ts">
import MasonryWall from '@yeger/vue-masonry-wall'
import { Todo, Meta } from 'components/models';
import ExampleComponent from 'components/ExampleComponent.vue';
import { ref } from 'vue';
import DropdownButton from 'src/components/DropdownButton.vue';
import DropdownButton2 from 'src/components/DropdownButton2.vue';
import DropdownButton3 from 'src/components/DropdownButton3.vue';
import axios from "axios";
import { storeToRefs } from "pinia";
import { onMounted } from "vue";
import Tweet from "vue-tweet";
import DatePicker from 'components/DatePicker.vue';

import {
  useSearchStore,
  useSourceStore,
  useCalendarStore,
  useChartStore,
  useTweetStore,
  useStatusStore,
} from 'src/stores/store';
const calendarStore = useCalendarStore('agora');

const chartStore = useChartStore('ordem');
const statusStore = useStatusStore();

const socialMedias = [
  { name: 'Twitter', icon: 'fab fa-twitter', color: '#489BE9' },
  // { name: 'Facebook', icon: 'fab fa-facebook', color: '#1877F2' },
  // { name: 'Instagram', icon: 'fab fa-instagram', color: '#DE3F6D' },
]


function relativeHeight(array,elem){
  const max = 300
  const high = array[0].total
  return (elem.total/high)*max

}

async function getData() {
  const proxyurl = 'https://portal.extensao.ufrj.br/php/proxy.php?url='
  const baseurl = 'http://34.95.230.124:10001'
  let filters = `?type=${chartStore.menuSelected.value}&datetype=${chartStore.menuSelected2.value}`
  if (chartStore.menuSelectedIndex2 == 1)
    filters = `${filters}&start=${calendarStore.getFromIso}&end=${calendarStore.getToIso}`
    
  let url = proxyurl + encodeURIComponent(`${baseurl}/tweet${filters}`)
  url = proxyurl + encodeURIComponent(`${baseurl}/entities${filters}&n=12`)
  await axios
    .get(url)
    .then(response => {
      var resp = response.data
      statusStore.entities = resp.data != null ? resp.data : []
    })

}

getData()

const filter = ref('')
const pagination = ref({
  page: 1,
  rowsPerPage: 3
})
const social = ref([
  { name: 'Twitter', value: true, disable: false },
  { name: 'Facebook', value: false, disable: true },
  { name: 'Instagram', value: false, disable: true },
]
)

const tipo = ref({
  selected: 'arvore',
  options: [
    { name: 'mapa de árvore', value: 'arvore', label: 'MAPA DE ÁRVORE' },
    { name: 'tabela', value: 'tabela', label: 'TABELA' },
    { name: 'barras', value: 'barras', label: 'BARRAS' },
  ]
}
)

</script>

<style scoped>
.text1 {
  font-family: 'Roboto';
  font-style: normal;
  font-weight: 500;
  font-size: 24px;
  line-height: 24px;
  letter-spacing: 0.02em;
  color: #A81815;
}

.btn1 {
  font-family: 'Oswald';
  font-style: normal;
  font-weight: 700;
  font-size: 24px;
  line-height: 24px;
  letter-spacing: 0.02em;
  color: #A81815;
  margin-left: 16px;
  margin-right: 16px;
  font-weight: bold;
  background-color: #F9FAFB;
  border: 1px solid #E5E7EB;
  border-radius: 8px;
}

.filter {
  margin: 40px 40px 0px 40px;
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: 16px;
}

.posts {
  background: #FFFFFF;
  margin: 40px 16px 0px 16px;
  padding: 54px;

  border: 1px solid #E5E7EB;
  border-radius: 16px;
}

.header {
  font-family: 'Oswald';
  font-style: normal;
  font-weight: 800;
  font-size: 70px;
  line-height: 80px;

  color: #00487D;
}

.subheader {
  font-family: 'Roboto';
  font-style: normal;
  font-weight: 400;
  font-size: 32px;
  line-height: 40px;

  color: #333333;
}

.maps {
  margin: 116px 122px 0px 122px;
  padding: 42px 132px 42px 132px;
  background: #00365D;
  border-radius: 16px;
}

.maps>span {
  font-family: 'Oswald';
  font-style: normal;
  font-weight: 500;
  font-size: 36px;
  line-height: 54px;
  text-transform: uppercase;
  color: #FFFFFF;
}

.maps>button {

  margin-left: 60px;
  background: #FFFFFF;
  border-radius: 8px;
  font-family: 'Oswald';
  font-style: normal;
  font-weight: 700;
  font-size: 20px;
  line-height: 32px;
  color: #00365D;
}

.temas {
  margin: 40px 16px 0px 16px;
  padding: 54px;
}

.listbox {
  padding: 25px 25px 40px 25px;

  background: #FFFFFF;

  border: 2px solid #E5E7EB;
  border-radius: 8px;
}

.listbox>.item {
  font-family: 'Roboto';
  font-style: normal;
  font-weight: 400;
  font-size: 24px;
  line-height: 32px;
  /* identical to box height, or 133% */

  letter-spacing: 0.02em;

  /* Preto/03 */

  color: #000000;
}

.header2 {
  font-family: 'Oswald';
  font-style: normal;
  font-weight: 600;
  font-size: 32px;
  line-height: 40px;
  /* identical to box height, or 125% */


  /* Preto/03 */

  color: #000000;
}

.hashtag {
  padding-bottom: 40px;
}

.hashtag>.header {
  font-family: 'Roboto';
  font-style: normal;
  font-weight: 500;
  font-size: 24px;
  line-height: 32px;
  /* identical to box height, or 133% */

  letter-spacing: 0.02em;
  text-transform: uppercase;

  /* Preto/03 */

  color: #000000;
}

.hashtag>.count {
  font-family: 'Roboto';
  font-style: normal;
  font-weight: 700;
  font-size: 16px;
  line-height: 24px;
  /* identical to box height, or 150% */

  letter-spacing: 0.02em;

  /* Preto/03 */

  color: #000000;
}

.imagens {
  background: #A81815;
  margin: 40px 16px 0px 16px;
  padding: 54px;

  border: 1px solid #E5E7EB;
  border-radius: 16px;
}

.imagens>.header {
  color: white;
}

.imagens>.subheader {
  color: white;
}

.btn {
  margin-top: 72px;
  width: 240px;
  height: 57px;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  padding: 16px 24px;
  gap: 16px;

  background: #FFFFFF;
  border-radius: 8px;

  font-family: 'Oswald';
  font-style: normal;
  font-weight: 700;
  font-size: 20px;
  line-height: 32px;
  /* identical to box height, or 160% */


  /* Vermelho/02 */

  color: #A81815;
}

.listbox>span {
  font-family: 'Roboto';
  font-style: normal;
  font-weight: 400;
  font-size: 20px;
  line-height: 30px;


  color: #333333;

}

.listbox>.title {
  padding-top: 35px;
  font-family: 'Oswald';
  font-style: normal;
  font-weight: 700;
  font-size: 22px;
  line-height: 32px;
  /* or 145% */

  text-transform: uppercase;

  /* Preto/01 */

  color: #333333;
}

.listbox>.excerpt {
  padding-top: 35px;

  font-family: 'Roboto';
  font-style: normal;
  font-weight: 400;
  font-size: 20px;
  line-height: 30px;
  /* or 150% */


  /* Preto/01 */

  color: #333333;
}

.listbox>.button {
  margin-top: 35px;
  font-family: 'Oswald';
  font-style: normal;
  font-weight: 500;
  font-size: 18px;
  line-height: 24px;
  /* identical to box height, or 133% */


  /* Vermelho/02 */

  color: #A81815;
}

div#OuterDiv {
  height: 100%;
  width: 100%;
  overflow: auto;
}

div#InnerDiv {
  position: relative;
  /* Guessing this is/was used for absolute positioning inside this div */
  overflow: auto;
  width: 300px;
  margin: 0 auto;
  height: auto !important;
  /* real browsers */
  height: 100%;
  /* IE6: treaded as min-height*/
  min-height: 100%;
  /* real browsers */
  background: transparent url('http://i.imgur.com/avej9.png') repeat scroll left top;
}

div#Content {
  padding: 7px;
  color: #000;
  /* height: 1080px; */
  margin: 10px 10px 0 0;
  background: transparent url('http://i.imgur.com/at996.png') repeat scroll left top;
}

.twittertree{
  background: #1DA1F2;
border-radius: 8px;
}

.twittertree>span{
  font-family: 'Roboto';
font-style: normal;
font-weight: 700;
font-size: 20px;
line-height: 32px;
/* identical to box height, or 160% */

letter-spacing: 0.02em;

/* Branco */

color: #FFFFFF;
}


.twittertree {
  background: #1DA1F2;
  border-radius: 8px;
}

.twittertree>span {
  font-family: 'Roboto';
  font-style: normal;
  font-weight: 700;
  font-size: 20px;
  line-height: 32px;
  /* identical to box height, or 160% */

  letter-spacing: 0.02em;

  /* Branco */

  color: #FFFFFF;
}

.subfilter {
  font-family: 'Oswald';
  font-style: normal;
  font-weight: 700;
  font-size: 16px;
  line-height: 24px;
  /* identical to box height, or 150% */

  text-transform: uppercase;

  /* Preto/03 */

  color: #000000;
}

tr:nth-child(even) {
  background: #FFFFFF;
}

tr:nth-child(odd) {
  background: #E5E7EB;
}

tr:first-child {
  background: transparent;
  opacity: 1;
}

td {
  color: #000000 !important;
}

table {
  font-family: 'Roboto';
  font-style: normal;
  font-weight: 700;
  font-size: 24px;
  line-height: 32px;
  /* identical to box height, or 133% */

  letter-spacing: 0.02em;

  /* Preto/03 */

  color: #000000;

}

.barraheader {
  overflow-wrap: break-word;
  font-family: 'Roboto';
  font-style: normal;
  font-weight: 700;
  font-size: 16px;
  line-height: 24px;
  /* or 150% */

  letter-spacing: 0.02em;

  /* Preto/03 */

  color: #000000;

}

.barravalue {
  font-family: 'Roboto';
  font-style: normal;
  font-weight: 700;
  font-size: 24px;
  line-height: 32px;
  /* identical to box height, or 133% */

  letter-spacing: 0.02em;

  /* Preto/03 */

  color: #000000;
}

h1{
  font-family: 'Oswald';
font-style: normal;
font-weight: 700;
font-size: 40px;
line-height: 40px;
/* identical to box height, or 100% */


/* Preto/03 */

color: #000000;
}

</style>
