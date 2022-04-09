# Square 1 - Setting up basic authentication

This is using the sql lite db, update your settings.py to connect to postgres if you wish. If you are getting an error:
~~~
?: (staticfiles.W004) The directory 'F:\Work\sandbox\test1\build/static' in the STATICFILES_DIRS setting does not exist.
~~~
or something similiar, replace the / with a \\ for the path to build static in proj/settings.py
~~~ python
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "build\\static"), # your static/ files folder
]

~~~
## Make migrations
should not be needed, but if your migrations show changes there may be an issue
~~~
python manage.py makemigrations
~~~
Run the migrations (this WILL be needed)
~~~
python manage.py migrate
~~~

## Create users
Either create a super user (and follow prompts)
~~~
python manage.py createsuperuser
~~~
Then navigate to http://localhost:8000/admin/ and add your users

-Or- add a [fixtures file](https://github.com/john-winko/template_django_react/blob/Basic_Authentication/app/fixtures/data.json) to app/fixtures/ (will have to create folder) then run
~~~
python manage.py loaddata data.json
~~~
*** Note: if you are making your own migrations your OS may use the wrong UTF encoding and will fail to load data. Fix will be to open the fixture file in notepad and resave using UTF-8 (NOT UTF-8 with BOM)

## Add views to app/views.py

imports
~~~ python
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
~~~

login (does not handle disabled accounts or trying a login attempt after being authenticated)
~~~ python
@api_view(['POST'])
def log_in(request):
    username = request.data['username']
    password = request.data['password']
    user = authenticate(username=username, password=password)
    if user is not None:    
        try:
            # access the base request, not DRF request (starts a login session for user)   
            login(request._request, user)
        except Exception as e:
            print(str(e))
        # Don't send everything from user, only what app needs to use for state
        return JsonResponse({"username":user.username})             
    else:
        return HttpResponse('no user!')
~~~

Who Am I? (testing if user is authentiated via request)
~~~ python
@api_view(["GET"])
def who_am_i(request):
    if request.user.is_authenticated:
        return JsonResponse({"user":request.user.username})
    return JsonResponse({"user":None})
~~~

Logging out
~~~ python
@api_view(['POST'])
def log_out(request):
    logout(request)
    return HttpResponse('Logged you out!')
~~~


## Update app/urls.py
~~~ python
urlpatterns = [
    path('', views.send_the_homepage),
    path('login/', views.log_in),
    path('whoami/', views.who_am_i),
    path('logout/', views.log_out)
]
~~~

## Fix manifest.json error in public/index.html
delete/comment out for now
~~~ html
<link rel="manifest" href="%PUBLIC_URL%/manifest.json" />
~~~

## Add some styling for forms in src/App.css
keep everything center aligned and keep form dimensions inside of a bounded area
~~~ css
.App {
  text-align: center;
  display: flex;
  justify-content: center;  
}

form {
  display: flex;
  flex-direction: column;
  justify-content: center;  
  width: 160px;
}
~~~

## Add src/utils/utils.js for doing api requests
(will have to create folder/file)

~~~ jsx
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
~~~

# Update react frontend src/App.js
~~~ jsx
import { useEffect, useState } from 'react';
import './App.css';
import utils from './utils/utils.js'

function App() {

  const [user, setUser] = useState(null)

  useEffect(()=> {
    utils.whoAmI()
  },[user])

  const handleFormSubmit = (evt) => {
    evt.preventDefault()
    let username = evt.target.elements.username.value
    let password = evt.target.elements.password.value
    utils.logIn(username, password, setUser)
  }

  return (
    <div className="App">
      <form onSubmit={handleFormSubmit}>
        {user && <p>Current logged in user: {user}</p>}
        <label forName="">Username</label>
        <input name='username' type={"text"}/>
        <label forName="">Password</label>
        <input name='password' type={"text"}/>
        <button type='submit' name='submit' value={"login"}>Login</button>
      </form>
    </div>
  );
}

export default App;
~~~