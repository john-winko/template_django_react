from django.http import HttpResponse

# Create your views here.
def send_the_homepage(request):
    theIndex = open('build/index.html').read()
    return HttpResponse(theIndex)