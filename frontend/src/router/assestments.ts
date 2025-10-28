import InterpreteEvaluacion from '@/features/assestment/code_running/interprete_evaluacion.vue'
import InterpreteTarea from '@/features/assestment/code_running/interprete_tarea.vue'
import TareasListEstudiante from '@/features/assestment/student/tareas_list.vue'
import ActividadesListDocente from '@/features/assestment/teacher/list_activity/activity_list.vue'
import ActividadDetalles from '@/features/assestment/teacher/list_activity/activity_view.vue'
import ActividadEditar from '@/features/assestment/teacher/edit_activity/activity_edit.vue'
import SeleccionarEvaluacion from '@/features/assestment/teacher/deeplinks/select_evaluacion.vue'
import CreateEvaluacion from '@/features/assestment/teacher/create_activity/create_activity.vue'

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
        component: TareasListEstudiante,
    },
    { 
        path: '/estudiante/tarea/:id', 
        name: 'entorno-tarea', 
        component: InterpreteTarea, 
        props: true 
    },
    { 
        path: '/estudiante/evaluacion/:id', 
        name: 'entorno-evaluacion', 
        component: InterpreteEvaluacion, 
        props: true 
    },
]

export const teacherRoutes = [
    { 
        path: '/docente/listar_actividades', 
        name: 'actividades-docente', 
        component: ActividadesListDocente,
    },
    { 
        path: '/docente/actividad/:tipo/:id', 
        name: 'actividad-detalles', 
        component: ActividadDetalles,
        props: true
    },
    { 
        path: '/docente/actividad/:tipo/:id/editar', 
        name: 'actividad-editar', 
        component: ActividadEditar,
        props: true
    },
    { 
        path: '/docente/seleccionar_evaluacion', 
        name: 'seleccionar-evaluacion', 
        component: SeleccionarEvaluacion,
    },
    { 
        path: '/docente/crear_actividad', 
        name: 'crear-actividad', 
        component: CreateEvaluacion,
    }
]