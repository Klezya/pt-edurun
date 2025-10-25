const router = require('express').Router()
const path = require('path')

// Requiring Ltijs
const lti = require('ltijs').Provider

// Grading route
router.post('/grade', async (req, res) => {
  try {
    const idtoken = res.locals.token // IdToken
    const score = req.body.grade // User numeric score sent in the body
    // Creating Grade object
    const gradeObj = {
      userId: idtoken.user,
      scoreGiven: score,
      scoreMaximum: 100,
      activityProgress: 'Completed',
      gradingProgress: 'FullyGraded'
    }
    console.log('IdToken info:', idtoken.platformContext.endpoint)
    // Selecting linetItem ID
    let lineItemId = idtoken.platformContext.endpoint.lineitem // Attempting to retrieve it from idtoken
    if (!lineItemId) {
      const response = await lti.Grade.getLineItems(idtoken, { resourceLinkId: true })
      const lineItems = response.lineItems
      if (lineItems.length === 0) {
        // Creating line item if there is none
        console.log('Creating new line item')
        const newLineItem = {
          scoreMaximum: 100,
          label: 'Grade',
          tag: 'grade',
          resourceLinkId: idtoken.platformContext.resource.id
        }
        const lineItem = await lti.Grade.createLineItem(idtoken, newLineItem)
        lineItemId = lineItem.id
      } else lineItemId = lineItems[0].id
    }
    console.log('Using line item id: ', lineItemId)
    // Sending Grade
    const responseGrade = await lti.Grade.submitScore(idtoken, lineItemId, gradeObj)
    return res.send(responseGrade)
  } catch (err) {
    console.log(err.message)
    return res.status(500).send({ err: err.message })
  }
})

// Names and Roles route
router.get('/members', async (req, res) => {
  try {
    const result = await lti.NamesAndRoles.getMembers(res.locals.token)
    if (result) return res.send(result.members)
    return res.sendStatus(500)
  } catch (err) {
    console.log(err.message)
    return res.status(500).send(err.message)
  }
})

// Deep linking route
router.post('/deeplink', async (req, res) => {
  try {
    const resource = req.body

    const items = {
      type: 'ltiResourceLink',
      title: resource.name,
      custom: {
        value: resource.value
      }
    }
    const form = await lti.DeepLinking.createDeepLinkingForm(res.locals.token, items, { message: 'Successfully Registered' })
    if (form) return res.send(form)
    return res.sendStatus(500)
  } catch (err) {
    console.log(err.message)
    return res.status(500).send(err.message)
  }
})

// Return available deep linking resources
router.get('/resources', async (req, res) => {
  const resources = [
    {
      name: 'Resource1',
      value: 'value1'
    },
    {
      name: 'Resource2',
      value: 'value2'
    },
    {
      name: 'Resource3',
      value: 'value3'
    }
  ]
  return res.send(resources)
})


router.get('/info/user', async (req, res) => {
  const info = { }
  const userContext = res.locals.context
  const usertoken = res.locals.token.userInfo

  if (usertoken) {
    if (usertoken.name) info.name = usertoken.name
  }

  if (userContext.user) info.userId = userContext.user
  if (userContext.roles) info.roles = userContext.roles
  return res.send(info)
})

router.get('/info/course', async (req, res) => {
  const info = { }
  const courseInfo = res.locals.context.context

  if (courseInfo){
    info.id = courseInfo.id
    info.label = courseInfo.label
    info.title = courseInfo.title
  } 
  return res.send(info)
})

router.get('/info/platform', async (req, res) => {
  const info = { }
  const platformInfo = res.locals.token.platformInfo

  if (platformInfo) {
    info.guid = platformInfo.guid
    info.name = platformInfo.name
    info.version = platformInfo.version
    info.product_family_code = platformInfo.product_family_code
  }
  
  return res.send(info)
})

router.get('/info/assignment', async (req, res) => {
  idtoken = res.locals.token

  console.log(idtoken.platformContext)

  return res.send(idtoken.platformContext.endpoint.lineitem)
})

// Wildcard route to deal with redirecting to React routes
//router.get('*', (req, res) => res.sendFile(path.join(__dirname, '../public/index.html')))

module.exports = router
