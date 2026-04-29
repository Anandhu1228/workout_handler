import os
import json
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .db_connector import db

# Blank schedule for fresh users
DEFAULT_SCHEDULE = {str(i): [] for i in range(7)}

def get_schedule():
    custom = db.get_full_schedule()
    return custom if custom else DEFAULT_SCHEDULE

def signup(request):
    if User.objects.exists(): return redirect('login')
    if request.method == 'POST':
        user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'], first_name=request.POST['name'])
        login(request, user)
        return redirect('dashboard')
    return render(request, 'signup.html')

def user_login(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            request.session.set_expiry(604800)
            return redirect('dashboard')
    return render(request, 'login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    sched = get_schedule()
    today_index = str(datetime.now().weekday())
    
    context = {
        'name': request.user.first_name,
        'todays_workouts': sched.get(today_index, []),
        'full_schedule': sched,
        'all_logs': db.get_all_logs(),
        'completed': db.has_worked_out_today(datetime.now().strftime('%Y-%m-%d'))
    }
    return render(request, 'dashboard.html', context)

@login_required
def api_log_workout(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        db.log_workout(datetime.now().strftime('%Y-%m-%d'), data['exercise'], data['w_type'], data['w_val'], data['summary'], data['duration'])
        return JsonResponse({'status': 'ok'})

@login_required
def api_edit_log(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        db.edit_log(data['log_id'], data['w_type'], data['w_val'], data['summary'])
        return JsonResponse({'status': 'ok'})

@login_required
def api_get_history(request):
    return JsonResponse({'history': db.get_history(request.GET.get('exercise'))})

@login_required
def api_finish_day(request):
    db.mark_daily_complete(datetime.now().strftime('%Y-%m-%d'), datetime.now().strftime('%H:%M:%S'))
    return JsonResponse({'status': 'ok'})

@login_required
def api_update_schedule(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        db.save_full_schedule(data['schedule'])
        return JsonResponse({'status': 'ok'})

@login_required
def api_upload_audio(request):
    if request.method == 'POST' and request.FILES.get('audio'):
        audio_file = request.FILES['audio']
        if audio_file.size > 10 * 1024 * 1024:
            return JsonResponse({'status': 'error', 'msg': 'File too large. Max 10MB.'})
        
        save_dir = os.path.join(settings.MEDIA_ROOT, 'alarm')
        os.makedirs(save_dir, exist_ok=True)
        file_path = os.path.join(save_dir, 'tone.mp3')
        
        if os.path.exists(file_path):
            os.remove(file_path)
            
        fs = FileSystemStorage(location=save_dir)
        fs.save('tone.mp3', audio_file)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error', 'msg': 'No file uploaded.'})