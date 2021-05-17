from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
  return HttpResponse("<marquee><h1>Django By MAngya</h1></marquee><h1>Welcome My First Django Learning Project</h1>")
