from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import date
from .models import Task, Habit, HabitCheck
from .forms import RegisterForm



def task_cards(request):
    tasks_all = Task.objects.all()
    task_for_timer = Task.objects.filter(is_done=False, deadline__isnull=False).first()
    seconds_left = None

    paginator = Paginator(tasks_all, 30)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    if task_for_timer and task_for_timer.deadline:
        now = timezone.now()
        diff = (task_for_timer.deadline - now).total_seconds()
        seconds_left = int(diff) if diff > 0 else 0


    return render(request, "task_cards.html", {
        "page_obj": page_obj, 
        "seconds_left": seconds_left,
        "task": task_for_timer
    })

def add_task(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        deadline = request.POST.get("deadline")
        if title:
            Task.objects.create(title=title,description=description, deadline=deadline)

    return redirect("/")

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('/')
 

def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.is_done = not task.is_done
    task.save()
    return redirect('/')
 
def habits_page(request):
    habits = Habit.objects.all()
    today = date.today()
    current_week = today.isocalendar()[1]
    current_year = today.year
 
    if today.weekday() == 0:
        for habit in habits:
            if habit.last_reset < today:
                habit.last_reset = today
                habit.save()
 
    
    habits_data = []
    for habit in habits:
        checked_days = set(HabitCheck.objects.filter(
            habit=habit, week_number=current_week, year=current_year
        ).values_list('day_of_week', flat=True))
 
        habits_data.append({
            'habit': habit,
            'days': [d in checked_days for d in range(7)],
            'total': len(checked_days),
        })
 
    return render(request, 'habits.html', {
        'habits': habits,
        'habits_data': habits_data,   
        'week': current_week,         
        'year': current_year,         
    })
 

def toggle_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id)
    day = int(request.POST.get('day'))
    today = date.today()
    week = today.isocalendar()[1]
    year = today.year
 
    obj, created = HabitCheck.objects.get_or_create(
        habit=habit, week_number=week, year=year, day_of_week=day
    )
    if not created:
        obj.delete()
 
    total = HabitCheck.objects.filter(habit=habit, week_number=week, year=year).count()
    return JsonResponse({'checked': created, 'total': total})
 

def add_habit(request):
    name = request.POST.get('name', '').strip()
    if name:
        Habit.objects.create(name=name)
    return redirect('/habits')
 

def delete_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id)
    habit.delete()
    return redirect('/habits')
 
def register_users(request):
    if request.method == "POST":
       form = RegisterForm(request.POST)
 
       if form.is_valid():
        user = form.save()
        login(request, user)  
        return redirect("/")
 
    else:
        form = RegisterForm()
    print("POST:", request.POST)
    print("VALID:", form.is_valid())
    print("ERRORS:", form.errors)
    return render(request, "register.html", {"form": form})
