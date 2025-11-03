import { actividadesGuard, evaluacionGuard } from './assestments.guards'


export const assestmentsRoutes = [
    {
        path: '/actividades',
        name: 'actividades',
        component: { template: '<div></div>' },
        beforeEnter: actividadesGuard
    },
    {
        path: '/evaluacion/:id',
        name: 'evaluacion',
        component: { template: '<div></div>' },
        beforeEnter: evaluacionGuard
    }
]

export const studentRoutes = [
    { 
        path: '/estudiante/listar_tareas', 
        name: 'tareas-estudiante', 
        component: () => import('@/features/assestment/student/tareas_list.vue'),
    },
    { 
        path: '/estudiante/tarea/:id', 
        name: 'entorno-tarea', 
        component: () => import('@/features/assestment/code_running/interprete_tarea.vue'), 
        props: true 
    },
    { 
        path: '/estudiante/evaluacion/:id', 
        name: 'entorno-evaluacion', 
        component: () => import('@/features/assestment/code_running/interprete_evaluacion.vue'), 
        props: true 
    },
]

export const teacherRoutes = [
    { 
        path: '/docente/listar_actividades', 
        name: 'actividades-docente', 
        component: () => import('@/features/assestment/teacher/list_activity/activity_list.vue'),
    },
    { 
        path: '/docente/actividad/:tipo/:id', 
        name: 'actividad-detalles', 
        component: () => import('@/features/assestment/teacher/list_activity/activity_view.vue'),
        props: true
    },
    { 
        path: '/docente/actividad/:tipo/:id/editar', 
        name: 'actividad-editar', 
        component: () => import('@/features/assestment/teacher/edit_activity/activity_edit.vue'),
        props: true
    },
    { 
        path: '/docente/seleccionar_evaluacion', 
        name: 'seleccionar-evaluacion', 
        component: () => import('@/features/assestment/teacher/deeplinks/select_evaluacion.vue'),
    },
    { 
        path: '/docente/crear_actividad', 
        name: 'crear-actividad', 
        component: () => import('@/features/assestment/teacher/create_activity/create_activity.vue'),
    }
]