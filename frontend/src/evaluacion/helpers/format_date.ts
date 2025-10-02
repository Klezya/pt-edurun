export function formatDate(fecha: string): string {
  try {
    const d = new Date(fecha)
    return new Intl.DateTimeFormat('es-CL', {
      dateStyle: 'medium',
      timeStyle: 'short',
    }).format(d)
  } catch {
    return fecha
  }
}