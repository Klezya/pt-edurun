import configs from "@/core/configs"

export async function getCourseIdByLmsId(courseIdLms: string): Promise<{ id: number } | { error: string }> {
  const result = await fetch(`${configs.apiBaseUrl}/lti/course/${courseIdLms}`).then(res => res.json())
  return result
}