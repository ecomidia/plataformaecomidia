<template>
  <q-page class="column">
    <div class="filter flex items-center justify-center q-pa-md">
      <span class="text1">Visualize por</span>
      <DropdownButton style="width:186px" class="btn1" :my-store="chartStore">
      </DropdownButton>
      <span class="text1">definido por</span>
      <DropdownButton2 class="btn1" :my-store="chartStore">
      </DropdownButton2>
      <span v-if="chartStore.menuSelectedIndex2 == 1" class="text1">de</span>
      <span v-if="chartStore.menuSelectedIndex2 == 0" class="text1">das últimas</span>
      <div>
        <q-btn-dropdown v-if="chartStore.menuSelectedIndex2 == 1" class="btn1" :label="calendarStore.getPeriodo">

          <DatePicker :calendarStore="calendarStore"></DatePicker>

        </q-btn-dropdown>
      </div>
      <DropdownButton3 v-if="chartStore.menuSelectedIndex2 == 0" class="btn1" :my-store="chartStore">
      </DropdownButton3>

      <q-btn class="btn1" label="Filtrar" @click="getData()"></q-btn>

    </div>

    <div class="posts">
      <span class="header">
        POSTS
      </span>
      <span class="subheader">Democratizando vozes</span>
      <q-separator style="background: #6B7280;" size="2px"></q-separator>
      <div class="q-pa-md">
        <q-table grid flat bordered :rows="statusStore.tweetsId" hide-header v-model:pagination="pagination">
          <template v-slot:item="props">
            <div class="q-pa-xs col-xs-12 col-sm-6 col-md-4">
              <Tweet :tweet-id="props.row" />
            </div>
          </template>
        </q-table>
      </div>
    </div>

    <div class="maps flex flex-center">
      <span>
        Saiba como os dados são mapeados
      </span>
      <q-btn label="clique aqui"></q-btn>
    </div>

    <div class="temas">
      <span class="header">
        TEMAS
      </span>
      <span class="subheader">assuntos que a comunidade discute nas redes</span>
      <q-separator style="background: #6B7280;" size="2px"></q-separator>

      <div class="row" style="margin-top: 40px;">
        <div class=" col-4 q-px-md" v-for="item in socialMedias" :key="item.name">
          <div class="listbox">
            <div class="row q-pb-md justify-between">
              <span class="col-auto header2"> {{ item.name }}</span>
              <q-icon class="col-auto" size="24px" :name="item.icon" :style="'color:' + item.color"></q-icon>
            </div>
            <div class="item" v-for="item in statusStore.entities" :key="item.entities__name">{{ item.entities__name }}
            </div>
          </div>
        </div>

      </div>

    </div>

    <div class="temas">
      <span class="header">
        HASHTAGS
      </span>
      <span class="subheader">Elos de perspectivas diversas</span>
      <q-separator style="background: #6B7280;" size="2px"></q-separator>

      <div class="row" style="margin-top: 40px;">
        <div class=" col-4 q-px-md" v-for="item in socialMedias" :key="item.name">
          <div class="listbox">
            <div class="row q-pb-md justify-between">
              <span class="col-auto header2"> {{ item.name }}</span>
              <q-icon class="col-auto" size="24px" :name="item.icon" :style="'color:' + item.color"></q-icon>
            </div>
            <div class="hashtag" v-for="item in statusStore.hashtags" :key="item">
              <div class="header">#{{ item.hashtags }}</div>
              <div class="count">{{ item.total }} tweets</div>
            </div>
          </div>
        </div>

      </div>

    </div>

    <div class="imagens">
      <span class="header">
        IMAGENS
      </span>
      <span class="subheader">Mosaico da comunidade</span>
      <q-separator style="background: white;" size="2px"></q-separator>
      <masonry-wall class="q-pt-xl" :items="statusStore.images?.slice(0, 8)" :ssr-columns="1" :column-width="300" :gap="16">
        <template #default="{ item }">
          <q-img id="InnerDiv" fit="contain" :src="item.photos__media_url"></q-img>
        </template>
      </masonry-wall>

      <div class="flex flex-center">
        <q-btn class="btn" label="Ver Mais"></q-btn>

      </div>
    </div>


    <div class="temas">
      <span class="header">
        LINKS
      </span>
      <span class="subheader">que os movimentos compartilham</span>
      <q-separator style="background: #6B7280;" size="2px"></q-separator>

      <div class="row" style="margin-top: 40px;">
        <div class=" col-4 q-px-md" v-for="item in statusStore.links" :key="item.title">
          <div class="listbox">
            <span class=""> Publicado por <strong>{{ item.user__screen_name }}</strong> </span>
            <div class="title">{{ item.urls__meta_title }}</div>
            <div class="excerpt">{{ item.urls__meta_content }}</div>
            <q-btn class="button" flat :href="item.urls__expanded_url" target="_blank" label="acessar link"></q-btn>
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


async function getData() {
  const proxyurl = 'https://portal.extensao.ufrj.br/php/proxy.php?url='
  const baseurl = 'http://34.95.230.124:10001'
  let filters = `?type=${chartStore.menuSelected.value}&datetype=${chartStore.menuSelected2.value}`
  if (chartStore.menuSelectedIndex2 == 1)
    filters = `${filters}&start=${calendarStore.getFromIso}&end=${calendarStore.getToIso}`
    
  let url = proxyurl + encodeURIComponent(`${baseurl}/tweet${filters}`)
  console.log(url)
  await axios
    .get(url)
    .then(response => {
      var resp = response.data
      statusStore.tweetsId = resp.data != null ?  resp.data.map(x => x.id) : []
    })
  url = proxyurl + encodeURIComponent(`${baseurl}/hashtags${filters}`)
  await axios
    .get(url)
    .then(response => {
      var resp = response.data
      statusStore.hashtags = resp.data != null ? resp.data : []
    })
  url = proxyurl + encodeURIComponent(`${baseurl}/images${filters}`)
  await axios
    .get(url)
    .then(response => {
      var resp = response.data
      statusStore.images = resp.data != null ? resp.data : []
    })
  url = proxyurl + encodeURIComponent(`${baseurl}/links${filters}`)
  await axios
    .get(url)
    .then(response => {
      var resp = response.data
      statusStore.links = resp.data != null ? resp.data : []
    })
  url = proxyurl + encodeURIComponent(`${baseurl}/entities${filters}`)
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
</style>
