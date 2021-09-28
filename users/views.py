from django.shortcuts import render

# Create your views here.
def login(request):
    context ={
        "title": "Geekshop - Autorisation"
    }
    return render(request, 'users/login.html', context)

def register(request):
    context ={
        "title": "Geekshop - Registration"
    }
    return render(request, 'users/register.html', context)