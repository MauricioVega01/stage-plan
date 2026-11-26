import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import ViewAuth from '../views/ViewAuth.vue';
import ViewVenue from '../views/ViewVenue.vue';
import ViewAudioPower from '../views/ViewAudioPower.vue';
import ViewAcousticCanvas from '../views/ViewAcousticCanvas.vue';
import ViewReportSummary from '../views/ViewReportSummary.vue';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/recinto',
  },
  {
    path: '/auth',
    name: 'auth',
    component: ViewAuth,
    meta: { stepId: 0, title: 'Consola Técnica & Acceso' },
  },
  {
    path: '/recinto',
    name: 'recinto',
    component: ViewVenue,
    meta: { stepId: 1, title: 'Geometría del Recinto' },
  },
  {
    path: '/equipos',
    name: 'equipos',
    component: ViewAudioPower,
    meta: { stepId: 2, title: 'Equipos de Audio & Energía' },
  },
  {
    path: '/plano-2d',
    name: 'plano-2d',
    component: ViewAcousticCanvas,
    meta: { stepId: 3, title: 'Plano 2D CAD & Acústica' },
  },
  {
    path: '/reporte',
    name: 'reporte',
    component: ViewReportSummary,
    meta: { stepId: 4, title: 'Memoria Técnica & Despacho' },
  },
];

export const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
