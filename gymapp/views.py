from django.shortcuts import render

# Create your views here.


def index(request):

    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def subscribe(request):
    return render(request, 'subscribe.html')
    pass

def services(request):
    return render(request, 'services.html')
    pass

def team(request):
    return render(request, 'team.html')
    pass

def create_account(request):
    if request.method == "GET":
        return render(request, 'create_account.html')