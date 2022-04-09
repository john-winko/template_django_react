import axios from "axios"
const myexports = {}

const getCSRFToken = ()=>{
  let csrfToken

  // the browser's cookies for this page are all in one string, separated by semi-colons
  const cookies = document.cookie.split(';')
  for ( let cookie of cookies ) {
      // individual cookies have their key and value separated by an equal sign
      const crumbs = cookie.split('=')
      if ( crumbs[0].trim() === 'csrftoken') {
          csrfToken = crumbs[1]
      }
  }
  return csrfToken
}
axios.defaults.headers.common['X-CSRFToken'] = getCSRFToken()

myexports.logIn = (username, password, setUser) => {
  let params = {
    "username" : username,
    "password" : password
  }
  axios.post('/login/', params).then((response)=>{ 
    if (response.data.username){
      setUser(response.data.username)
    }
  })
}

myexports.logOut = async () => {
  await axios.post("/logout/")
}

myexports.whoAmI = async () => {
  const response = await axios.get("/whoami/")
  console.log("whoami", response.data)
}

export default myexports;