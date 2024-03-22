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

def profile(request):
    user = request.user
    return render(request, 'profile.html')



def create_account(request):
    if request.method == "GET":
        return render(request, 'create_account.html')
    elif request.method == "POST":
        # Get form data from POST request
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone_number = request.POST.get("phone_number")   



from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

# def login(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
        
#         user = authenticate(request, email=email, password=password)
#         if user is not None:
#             login(request, user)
#             # Redirect to the appropriate page after login
#             # For example, if you want to redirect to the profile page:
#             return redirect('profile')
#         else:
#             # Handle invalid login credentials
#             return render(request, 'login.html', {'error': 'Invalid email or password'})

#     return render(request, 'login.html')



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .models import Membership

from datetime import datetime, timedelta
from .models import Membership

@login_required 
def subscribe(request, membership=None):
        # Set the start date to the current date
        start_date = datetime.now().date()

        # Find the duration based on the selected membership plan
        for duration, plan in Membership.DURATION_CHOICES:
            if plan == membership:
                break
        else:
            # Handle invalid membership plan (optional)
            print(membership)
            return render(request, 'subscribe.html')

        # Create a new membership record
        Membership.objects.create(member=request.user, duration=duration, start_date=start_date)

        # Redirect the user to a success page or membership confirmation page
        return redirect('profile')


