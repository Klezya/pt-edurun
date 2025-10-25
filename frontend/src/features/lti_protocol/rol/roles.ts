const Roles = [
  //Canvas roles  
  //{ url: 'http://purl.imsglobal.org/vocab/lis/v2/institution/person#Administrator', rol: 'administrador' },
  { url: 'http://purl.imsglobal.org/vocab/lis/v2/membership#Instructor', rol: 'docente' },
  { url: 'http://purl.imsglobal.org/vocab/lis/v2/membership#Learner', rol: 'estudiante' }
];

export function getRol(url: string[]) {
  for (const u of url) {
    const rolurl = Roles.find(item => item.url === u);
    if (rolurl) return rolurl.rol;
  }
  return null;
}
