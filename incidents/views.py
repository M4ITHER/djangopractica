from django.shortcuts import render, redirect, get_object_or_404
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


def update_incident(request, id):
    incident = get_object_or_404(Incident, id=id)

    if request.method == 'POST':
        incident.title = request.POST['title']
        incident.description = request.POST['description']
        incident.save()

        return redirect('home')

    return render(request, 'incidents/update.html', {
        'incidents': incident
    })


def delete_incident(request, id):

    incident = get_object_or_404(Incident, id=id)

    if request.method == 'POST':
        incident.delete()
        return redirect('home')

    return render(request, 'incidents/confirm_delete.html', {
        'incident': incident
    })


def view_incident(request, id):

    incident = get_object_or_404(Incident, id=id)

    return render(request, 'incidents/detail.html', {
        'incident': incident
    })


def create_incident(request):

    if request.method == 'POST':

        title = request.POST['title']
        description = request.POST['description']

        Incident.objects.create(
            title=title,
            description=description
        )

        return redirect('home')

    return render(request, 'incidents/create.html')