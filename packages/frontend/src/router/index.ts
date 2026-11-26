import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/recinto',
  },
  {
    path: '/auth',
    name: 'auth',
    component: () => import('../views/ViewAuth.vue'),
    meta: { stepId: 0, title: 'Consola Técnica & Acceso' },
  },
  {
    path: '/recinto',
    name: 'recinto',
    component: () => import('../views/ViewVenue.vue'),
    meta: { stepId: 1, title: 'Geometría del Recinto' },
  },
  {
    path: '/equipos',
    name: 'equipos',
    component: () => import('../views/ViewAudioPower.vue'),
    meta: { stepId: 2, title: 'Equipos de Audio & Energía' },
  },
  {
    path: '/plano-2d',
    name: 'plano-2d',
    component: () => import('../views/ViewAcousticCanvas.vue'),
    meta: { stepId: 3, title: 'Plano 2D CAD & Acústica' },
  },
  {
    path: '/reporte',
    name: 'reporte',
    component: () => import('../views/ViewReportSummary.vue'),
    meta: { stepId: 4, title: 'Memoria Técnica & Despacho' },
  },
];

export const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
