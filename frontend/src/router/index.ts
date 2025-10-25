import { createRouter, createWebHistory } from "vue-router";

import { assestmentsRoutes, studentRoutes, teacherRoutes } from "./assestments";
import Home from '@/Home.vue';

const routes = [
    { path: '/', component: Home, name: 'home' },
    ...assestmentsRoutes,
    ...studentRoutes,
    ...teacherRoutes
]

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;