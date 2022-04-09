from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view

# Create your views here.
def send_the_homepage(request):
    theIndex = open('build/index.html').read()
    return HttpResponse(theIndex)

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
    
@api_view(["GET"])
def who_am_i(request):
    if request.user.is_authenticated:
        return JsonResponse({"user":request.user.username})
    return JsonResponse({"user":None})

@api_view(['POST'])
def log_out(request):
    logout(request)
    return HttpResponse('Logged you out!')