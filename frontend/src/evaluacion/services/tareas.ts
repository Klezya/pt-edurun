const URL = 'https://edurunbackend.loca.lt/api'

export async function getTareasByCourseLmsId(courseId: string) {
  const result = await fetch(`${URL}/tareas/${courseId}`).then(res => res.json())
  console.log('Tareas del curso obtenidas:', result)
  return result
}