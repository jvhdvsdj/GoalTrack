from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from tasks.models import Task

def task_cards(request):
    tasks_1 = Task.objects.all()

    paginator = Paginator(tasks_1, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tasks.html', {'page_obj': page_obj})
