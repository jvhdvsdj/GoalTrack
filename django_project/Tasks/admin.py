from django.contrib import admin
from .models import Task, Habit, HabitCheck


admin.site.register(Task)
admin.site.register(Habit)
admin.site.register(HabitCheck)


