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
    salio_pantalla_completa: boolean
    cambios_ventana: number
    tiempo_inactividad_segundos: number
    ejecuciones_codigo?: number
    ejecuciones_tests?: number
    tiempo_total_segundos?: number
    timestamp: string
  }
  fecha_entrega?: string
}