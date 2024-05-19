from django.shortcuts import render
from django.http import HttpResponseNotFound

# Create your views here.
def documentation(request):
    code = request.GET.get("code")
    if code != "teacher":
        return HttpResponseNotFound("<h1>404 - Page not found</h1>")
    return render(request, "api/docs.html")