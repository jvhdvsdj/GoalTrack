from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from tasks.models import Task
from django.utils import timezone


def task_cards(request):
    tasks_1 = Task.objects.all()
    task_for_timer = Task.objects.first()
    seconds_left = None

    paginator = Paginator(tasks_1, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if task_for_timer and task_for_timer.deadline:
        now = timezone.now()
        diff = (task_for_timer.deadline - now).total_seconds()
        seconds_left = int(diff) if diff > 0 else 0

    return render(request, 'task_cards.html', {
        'page_obj': page_obj, 
        'seconds_left': seconds_left,
        'task': task_for_timer 
    })
