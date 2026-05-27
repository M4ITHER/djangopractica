from django.shortcuts import render, redirect, get_object_or_404
# from django.http import HttpResponse
from .models import Incident
from django.contrib.auth.decorators import login_required
from .forms import IncidentForm
from accounts.models import UserProfile
from django.http import HttpResponseForbidden
from django.contrib import messages

# Create your views here.

@login_required
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
        return redirect('incidents:home') # Post/Redirect/Get pattern
    
    # GET request: load all incidents from DB
    incidents = Incident.objects.all()
    return render(request, 'incidents/home.html', {'incidents': incidents})

@login_required
def update_incident(request, id):
    profile = UserProfile.objects.get(user=request.user)
    if not profile.is_admin():
        return HttpResponseForbidden('Only admins can update incidents.')

    incident = get_object_or_404(Incident, id=id)

    if request.method == 'POST':
        incident.title = request.POST['title']
        incident.description = request.POST['description']
        incident.save()
        messages.success(
            request,
            'Incident updated successfully.'
        )

        return redirect('incidents:home')

    return render(request, 'incidents/update.html', {
        'incidents': incident
    })

@login_required
def delete_incident(request, id):
    profile = UserProfile.objects.get(user=request.user)
    if not profile.is_admin():
        return HttpResponseForbidden('Only admins can delete incidents.')

    incident = get_object_or_404(Incident, id=id)

    if request.method == 'POST':
        incident.delete()
        messages.success(
            request,
            'Incident deleted successfully.'
        )
        return redirect('incidents:home')

    return render(request, 'incidents/confirm_delete.html', {
        'incident': incident
    })

@login_required
def view_incident(request, id):

    incident = get_object_or_404(Incident, id=id, pk=pk)

    return render(request, 'incidents/detail.html', {
        'incident': incident
    })

@login_required
def create_incident(request):
    form = IncidentForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        incident = form.save(commit=False)
        incident.reported_by = request.user
        incident.save()
        messages.success(
            request, 
            'Incident created successfully.'
            )
        return redirect('incidents:home')

    return render(request, 'incidents/create.html', {'form': form})