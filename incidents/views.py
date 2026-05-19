from django.shortcuts import render, redirect
# from django.http import HttpResponse
from .models import Incident

# Create your views here.

def home(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        
        # Basic validation — never trust raw user input
        if title and description:
            Incident.objects.create(
                title=title,
                description=description
            )
        return redirect('home') # Post/Redirect/Get pattern
    
    # GET request: load all incidents from DB
    incidents = Incident.objects.all()
    return render(request, 'incidents/home.html', {'incidents': incidents})