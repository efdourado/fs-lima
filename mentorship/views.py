from .models import Mentor, Mentee, Availability, Meeting, Task, Upload

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import constants

from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from datetime import datetime, timedelta

from .auth import validate_token

@login_required
def mentorship(request):
    if request.method == 'GET':
        mentors = Mentor.objects.filter(user=request.user)
        mentees = Mentee.objects.filter(user=request.user)

        stages_flat = [i[1] for i in Mentee.stages]
        qty_stages = []

        for i, j in Mentee.stages:
            qty_stages.append(Mentee.objects.filter(stage = i).filter(user = request.user).count())

            
        return render(request, 'mentorship.html', {'stages': Mentee.stages, 'mentors': mentors, 'mentees': mentees, 'stages_flat': stages_flat, 'qty_stages': qty_stages})
        
    elif request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        stage = request.POST.get('stage')
        mentor = request.POST.get('mentor')

        instance = Mentee(name=name, image=image, stage=stage, mentor_id=mentor, user=request.user)
        instance.save()

        messages.add_message(request, constants.SUCCESS, 'Mentee created successfully!')
        return redirect('mentorship')

@login_required
def meetings(request):
    if request.method == 'GET':
        meetings = Meeting.objects.filter(date__mentor=request.user)
        return render(request, 'meetings.html', { 'meetings': meetings })

    else:
        date = request.POST.get('date')

        date = datetime.strptime(date, '%Y-%m-%dT%H:%M')

        existing_slots = Availability.objects.filter(
            start_time__gte=(date - timedelta(minutes=50)),
            start_time__lte=(date + timedelta(minutes=50))
        )

        if existing_slots.exists():
            messages.add_message(request, constants.ERROR, 'You already have a scheduled meeting at this time.')
            return redirect('meetings')

        new_slot = Availability(
            start_time=date,
            mentor=request.user
        )
        new_slot.save()

        messages.add_message(request, constants.SUCCESS, 'Time slot successfully made available.')
        return redirect('meetings')

def auth(request):
    if request.method == 'GET':
        return render(request, 'auth_mentee.html')
    else:
        token = request.POST.get('token')

        if not Mentee.objects.filter(token=token).exists():
            messages.add_message(request, constants.ERROR, 'Invalid token')
            return redirect('auth_mentee')
        
        response = redirect('choose_day')
        response.set_cookie('auth_token', token, max_age=3600)
        return response

def choose_day(request):
    if not validate_token(request.COOKIES.get('auth_token')):
        return redirect('auth_mentee')

    if request.method == 'GET':
        mentee = validate_token(request.COOKIES.get('auth_token'))

        existing_slots = Availability.objects.filter(
            start_time__gte=datetime.now(),
            is_booked=False,
            mentor=mentee.user
        ).values_list('start_time', flat=True)

        available_dates = []
        seen_dates = set()

        for slot in existing_slots:
            date_obj = slot.date()
            formatted_date = date_obj.strftime('%m-%d-%Y')
            
            if formatted_date not in seen_dates:
                seen_dates.add(formatted_date)
                available_dates.append({
                    'month': date_obj.strftime('%B'),
                    'weekday': date_obj.strftime('%A'),
                    'full_date': formatted_date
                })

        return render(request, 'choose_day.html', {'available_dates': available_dates})

def book_meeting(request):
    if not validate_token(request.COOKIES.get('auth_token')):
        return redirect('auth_mentee')

    mentee=validate_token(request.COOKIES.get('auth_token'))

    if request.method == 'GET':
        date = request.GET.get("date")
        date = datetime.strptime(date, '%m-%d-%Y')

        available_dates = Availability.objects.filter(
            start_time__gte=date,
            start_time__lt=date + timedelta(days=1),
            is_booked=False,
            mentor=mentee.user
        )
        return render(request, 'book_meeting.html', {'available_dates': available_dates, 'tags': Meeting.tag_choices})
    
    else:
        date_id = request.POST.get('date')
        tag = request.POST.get('tag')
        description = request.POST.get("description")

        #TODO: Realizar validações

        # add ATOMICIDADE

        meeting = Meeting( 
            date_id=date_id,
            mentee=mentee,
            tag=tag,
            description=description
        )
        meeting.save()

        date = Availability.objects.get(id=date_id)
        date.is_booked = True
        date.save()

        messages.add_message(request, constants.SUCCESS, 'Meeting booked successfully.')
        return redirect('choose_day')

def task(request, id):
    mentee = Mentee.objects.get(id=id)
    if mentee.user != request.user:
        raise Http404()
    
    if request.method == 'GET':
        tasks = Task.objects.filter(mentee=mentee)
        videos = Upload.objects.filter(mentee=mentee)
        
        return render(request, 'task.html', {'mentee': mentee, 'tasks': tasks, 'videos': videos})

    else:
        task = request.POST.get('task')

        task = Task(
            mentee=mentee,
            task=task,
        )
        task.save()
        return redirect(f'/mentorship/task/{id}')

def upload(request, id):
    mentee = Mentee.objects.get(id=id)
    if mentee.user != request.user:
        raise Http404()
    
    video = request.FILES.get('video')
    upload = Upload(
        mentee=mentee,
        video=video
    )
    upload.save()
    return redirect(f'/mentorship/task/{mentee.id}')

def task_mentee(request):
    mentee = validate_token(request.COOKIES.get('auth_token'))
    if not mentee:
        return redirect('auth_mentee')
    
    if request.method == 'GET':
        videos = Upload.objects.filter(mentee=mentee)
        tasks = Task.objects.filter(mentee=mentee)
        return render(request, 'task_mentee.html', {'mentee': mentee, 'videos': videos, 'tasks': tasks})

@csrf_exempt
def task_change(request, id):
    mentee = valida_token(request.COOKIES.get('auth_token'))
    if not mentee:
        return redirect('auth_mentee')

    task = Task.objects.get(id=id)
    if mentee != task.mentee:
        raise Http404()

    task.done = not task.done
    task.save()

    return HttpResponse('teste')