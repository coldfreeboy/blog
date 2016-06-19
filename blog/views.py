from django.shortcuts import render,HttpResponse

# Create your views here.

def home(request):
    return render(request,"home.html")

def login(request,tag):
    if tag == "log_in":
        msg = "log_in"
    if tag == "log_up":
        msg = "log_up"

    return HttpResponse("<h1>"+msg+"</h1>")


