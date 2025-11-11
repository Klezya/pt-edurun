require('dotenv').config()
const routes = require('./src/routes')

const lti = require('ltijs').Provider

const frontendUrl = process.env.FRONTEND_URL

// Setup
lti.setup(process.env.LTI_KEY,
  {
    url: process.env.MONGO_URL
  }, {
    //staticPath: path.join(__dirname, '../frontend/dist'), // Path to static files
    ltiaas: true,
    cookies: {
      secure: true, // Set secure to true if the testing platform is in a different domain and https is being used
      sameSite: 'None' // Set sameSite to 'None' if the testing platform is in a different domain and https is being used
    },
    devMode: true // Set DevMode to true if the testing platform is in a different domain and https is not being used
  })

// When receiving successful LTI launch redirects to app
lti.onConnect(async (token, req, res) => {
  
  const ltik = res.locals.ltik;
  const type = req.query.type;
  return res.sendFile(path.join(__dirname, '../public/index.html'));
  const redirectUrl = `${frontendUrl}/?ltik=${ltik}`;
  
  if (!type) {
    if (token.platformContext?.custom.value === undefined) {
      const redirectUrl = `${frontendUrl}/?ltik=${ltik}`;
      return res.redirect(redirectUrl);
    }
    
    const evaluacionId = token.platformContext.custom.value;
    const redirectUrl = `${frontendUrl}/estudiante/evaluacion/${evaluacionId}/?ltik=${ltik}`;
    return res.redirect(redirectUrl);  
  }

  if (type === 'review') {
    const user_id = req.query.user_id;
    const assessment_id = req.query.assessment_id;
    const redirectUrl = `${frontendUrl}/docente/review/?ltik=${ltik}&user_id=${user_id}&assessment_id=${assessment_id}`;
    return res.redirect(redirectUrl);
  }

  return res.redirect(redirectUrl);
})

// When receiving deep linking request redirects to deep screen
lti.onDeepLinking(async (token, req, res) => {
  deeplinkLtik = res.locals.ltik
  return lti.redirect(res, `${frontendUrl}/docente/seleccionar_evaluacion/?ltik=${deeplinkLtik}`)
})

// Setting up routes
lti.app.use(routes)

// Setup function
const setup = async () => {
  await lti.deploy({ port: process.env.PORT })

  await lti.deletePlatform('https://sandbox.moodledemo.net', 'Trymqct0j6KtREn')
  await lti.deletePlatform('https://edurundev.milaulas.com', 'taxkx5XEIY7b9VK')
  await lti.deletePlatform('https://172.19.202.187', '10000000000007')
  /**
   * Register platform
   */
  await lti.registerPlatform({
    url: 'https://edurundev.milaulas.com',
    name: 'edurundev',
    clientId: 'FZMAosXXMgnvVgP',
    authenticationEndpoint: 'https://edurundev.milaulas.com/mod/lti/auth.php',
    accesstokenEndpoint: 'https://edurundev.milaulas.com/mod/lti/token.php',
    authConfig: { method: 'JWK_SET', key: 'https://edurundev.milaulas.com/mod/lti/certs.php' }
  })
   await lti.registerPlatform({
    url: 'https://172.19.202.187',
    name: 'canvas',
    clientId: '10000000000007',
    authenticationEndpoint: 'https://172.19.202.187/api/lti/authorize_redirect',
    accesstokenEndpoint: 'https://172.19.202.187/login/oauth2/token',
    authConfig: { method: 'JWK_SET', key: 'https://172.19.202.187/api/lti/security/jwks' }
  })
}

setup()
