const URL = 'https://backend.loca.lt/lti'


export async function isUserRegistered(userIdLms: string) {
  const result = await fetch(`${URL}/check_user/${userIdLms}`).then(res => res.json())
  return result
}
