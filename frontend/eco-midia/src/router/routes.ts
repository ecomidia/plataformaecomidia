import { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '',name:'home', component: () => import('pages/IndexPage.vue') },
      { path: 'posts',name:'posts', component: () => import('pages/PostsPage.vue') },
      { path: 'temas',name:'temas', component: () => import('pages/TemasPage.vue') },
      { path: 'hashtags',name:'hashtags', component: () => import('pages/HashtagsPage.vue') },
      { path: 'imagens',name:'imagens', component: () => import('pages/ImagesPage.vue') },
      { path: 'nexo',name:'nexo', component: () => import('pages/LinksPage.vue') },
      { path: 'SOBRE',name:'SOBRE', component: () => import('pages/SobrePage.vue') },
    ],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
