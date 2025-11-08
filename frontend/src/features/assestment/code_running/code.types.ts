export interface EntregaEvaluacionData {
    id_evaluacion: number
    id_alumno: string
    nota: number
    codigo?: string
    detalles?: Record<string, any>
}