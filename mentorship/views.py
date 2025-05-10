from django.shortcuts import render, redirect
from .models import Mentee, Mentor
from django.contrib import messages
from django.contrib.messages import constants

def mentorship(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'GET':
        mentors = Mentor.objects.filter(user=request.user)
        mentees = Mentee.objects.filter(user=request.user)
        return render(request, 'mentorship.html', {'stages': Mentee.stages, 'mentors': mentors, 'mentees': mentees})
        
    elif request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        stage = request.POST.get('stage')
        mentor = request.POST.get('mentor')
        instance = Mentee(name=name, image=image, stage=stage, mentor_id=mentor, user=request.user)
        instance.save()

        messages.add_message(request, constants.SUCCESS, 'Mentee created successfully!')
        return redirect('mentorship')