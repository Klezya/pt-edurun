export interface EntregaEvaluacionResponse {
  id: number
  id_evaluacion: number
  id_alumno: number
  nota: number
  codigo?: string
  detalles?: {
    intentos_copiar: number
    intentos_pegar: number
    intentos_cortar: number
    cambios_ventana: number
    timestamp: string
  }
  fecha_entrega?: string
}