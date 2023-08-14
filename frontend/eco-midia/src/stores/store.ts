import { defineStore } from 'pinia';
import { date } from 'quasar';
import { start } from 'repl';
import { DateRangeModel } from 'src/components/models';

export const useUserStore = defineStore('user', {
  state: () => ({
    logged: false,
    user: '',
    password: '',
    submitResult: true,
  }),
  getters: {},
  actions: {
    login() {
      if(this.user == 'db' && this.password == 'db'){
        this.logged = true
        this.submitResult = true
        console.log(this.logged)
        console.log('login')
        this.router.push({name:'agora'})
        return true
      }
      else{
        this.submitResult = false;
        return false
      }
    },
  },
});

export const useCalendarStore = (id: string) =>
  defineStore(`calendar/${id}`, {
    state: () => ({
      range: {start:new Date(2023,0,1), end:new Date()} as DateRangeModel,
    }),
    getters: {
      getFrom: (state) => date.formatDate(state.range.start, 'DD-MM-YYYY'),
      getTo: (state) => date.formatDate(state.range.end, 'DD-MM-YYYY'),
      getFromIso: (state) => date.formatDate(state.range.start, 'YYYY-MM-DD'),
      getToIso: (state) => date.formatDate(state.range.end, 'YYYY-MM-DD'),
      getPeriodo: (state) => `${state.getFrom} até ${state.getTo}`,
    },
    actions: {
    },
  })();

export const useChartStore = (id: string) =>
  defineStore(`chart/${id}`, {
    state: () => ({
      menu: [
        { id: 0, label: 'TEMPO',value: 'time', description:'Ordem cronológica, segundo o registro das publicações nas redes sociais' },
        { id: 1, label: 'FREQUÊNCIA',value: 'frequency', description:'Para garantir a visibilidade dos perfis com menores atividades nas redes' },
        { id: 2, label: 'INTERAÇÃO',value: 'engagement', description:'A partir da quantidade de ações de usuários, como curtidas, comentários e compartilhamentos' },
      ],
      menu2: [
        { id: 0, label: 'HORAS', value: 'relative', },
        { id: 1, label: 'PERÍODO',value: 'range', },
      ],
      menu3: [
        { id: 0, label: '3 HORAS', value: '3', },
        { id: 1, label: '6 HORAS',  value: '6'},
        { id: 2, label: '12 HORAS',  value: '12'},
      ],
      menuSelectedIndex: 0,
      menuSelectedIndex2: 1,
      menuSelectedIndex3: 2,
    }),
    getters: {
      menuSelected: (state) => state.menu[state.menuSelectedIndex],
      menuSelected2: (state) => state.menu2[state.menuSelectedIndex2],
      menuSelected3: (state) => state.menu3[state.menuSelectedIndex3],
    },
    actions: {
      changePreSelect(index: number) {
        this.menuSelectedIndex = index;
      },
      changePreSelect2(index: number) {
        this.menuSelectedIndex2 = index;
      },
      changePreSelect3(index: number) {
        this.menuSelectedIndex3 = index;
      },
      populate(labels: Array<string>) {
        this.menu = [];
        for (let i = 0; i < labels.length; i++)
          this.menu = this.menu.concat({ id: i, label: labels[i] });
      },
    },
  })();

export const useTabsStore = defineStore('tabs', {
  state: () => ({
    tabs: [
      { id: 0, name: 'agora', label: 'Acontecendo agora', to: '/' },
      // { id: 1, name: 'partidos', label: 'Partidos', to: '/partidos' },
      // { id: 2, name: 'projetos', label: 'Projetos', to: '/projetos' },
      { id: 2, name: 'talkwalker', label: 'Talkwalker', to: '/talkwalker' },
    ],
    selected: '',
  }),
  getters: {},
  actions: {
    select(name: string) {
      this.selected = name;
    },
  },
});

export const useSearchStore = (id: string) =>
  defineStore(`searchAgora/${id}`, {
    state: () => ({
      text: '',
      label: '',
    }),
    getters: {
      getText: (state) =>
        state.text ? `&search_simple_query_string=${state.text}` : '',
    },
  })();

export const useResultStore = (id: string) =>
  defineStore(`tweetStore/${id}`, {
    state: () => ({
      showResults: false,
      results: [],
    }),
    actions: {
      populate(input) {
        this.results = [];
        for (let i = 0; i < input.length; i++) {
          const e = input[i];
          const img = e.images.length ? e.images[0].url : '';
          const projetos = e.topic_set.map((elem) => elem.name);
          this.results = this.results.concat({
            title: e.title,
            content: e.content,
            image: img,
            root_url: e.root_url,
            author: e.author.name,
            author_img: e.author.image_url,
            engagement: e.engagement,
            reach: e.reach,
            projetos: projetos,
            pageviews: e.source_extended_attributes_alexa_pageviews,
            url:e.url
          });
        }
      },
    },
  })();
export const useTweetStore = (id: string) =>
  defineStore(`tweetStore/${id}`, {
    state: () => ({
      showTweets: false,
      tweets: [
        '1530240085807054848',
        '1602080433658896385',
        '1599752993250967552',
        '1601903673092751363',
        '1530240085807054848',
        '1530240085807054848',
        '1530240085807054848',
        '1530240085807054848',
      ],
    }),
  })();

export const useAgoraStore = defineStore('agoraStore', {
  state: () => ({
    tuites: 0,
    hashtags: 0,
    mencoes: 0,
    links: 0,
    projetos: 0,
    rts: true,
  }),
  getters: {
    text1: (state) =>
      `Neste período, estamos monitorando <strong>${state.tuites}</strong> tuítes e <strong>${state.hashtags}</strong> hashtags relacionados a <strong>${state.projetos}</strong> projetos em tramitação no Congresso.`,
    text2: (state) =>
      `Foram mencionados <strong>${state.mencoes}</strong> usuários e <strong>${state.links}</strong> links foram compartilhados até agora.`,
    withRt: (state) => (state.rts ? '' : '&rt__isnull=false'),
  },
  actions: {},
});

export const useSourceStore = (id: string) =>
  defineStore(`sourceStore/${id}`, {
    state: () => ({
      sources: [
        { id: 0, name: 'parlamentares', label: 'parlamentares', value: ['Câmara%20dos%20Deputados%202019','Senadores'] },
        { id: 1, name: 'senadores', label: 'senadores', value: ['Senadores'] },
        {
          id: 2,
          name: 'deputados',
          label: 'deputados',
          value: ['Câmara%20dos%20Deputados%202019'],
        },
      ],
      selected: 0,
    }),
    getters: {
      getIsSelected: (state) => {
        return (currentId: number) => state.selected == currentId;
      },
      getSelected: (state) => state.sources[state.selected],
      getSourceList: (state) =>
        state.getSelected.value.length
          ? `&source_list__in=${state.getSelected.value.join('__')}`
          : '',
    },
    actions: {
      select(id: number) {
        this.selected = id;
      },
      populate(input) {
        this.sources = [{ id: 0, name: 'todos', label: 'todos', value: [] }];
        let id = 1;
        for (let i = 0; i < input.length; i++) {
          if (
            input[i].key.includes('_') &&
            !input[i].key.includes('SOCIALMEDIA')
          )
            continue;
          if (input[i].key === 'SOCIALMEDIA') continue;
          this.sources = this.sources.concat({
            id: id,
            name: input[i].key,
            label: input[i].key,
            value: [input[i].key],
          });
          this.sources[0].value = this.sources[0].value.concat(input[i].key);
          id++;
        }
      },
    },
  })();

export const useDropDownStore = (id: string) => defineStore(`dropDownStore/${id}`,{
  state: () => ({
    list: [],
    selected: [],
    label:'',
  }),
  getters: { getUrl: (state) => state.selected.length
    ? `&topic__in=${state.selected.join('__')}`
    : '',
  },
  actions: {
    populate(input) {
      this.list = input.map( (e) => e.key);
    },
  },
})();

export const useTalkWalkerSore = defineStore('talkWalkerStpre', {
  state: () => ({
    resultados: 0,
    projetos:0
  }),
  getters: {
    text1: (state) =>
      `Neste período, estamos monitorando <strong>${state.resultados}</strong> resultados relacionados a <strong>${state.projetos}</strong> projetos em tramitação no Congresso.`,

  },
  actions: {},
});

export const useStatusStore = defineStore('statusStore', {
  state: () => ({
    tweetsId: [],
    hashtags: [],
    images: [],
    status: [],
    links: [],
    entities:[],
  }),
  getters: {
    text1: (state) =>
      `Neste período, estamos monitorando <strong>${state.resultados}</strong> resultados relacionados a <strong>${state.projetos}</strong> projetos em tramitação no Congresso.`,
  },
  actions: {},
});