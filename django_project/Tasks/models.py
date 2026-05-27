from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    title = models.CharField(max_length = 200)
    description = models.TextField()
    deadline = models.DateTimeField(null=True, blank=True, verbose_name="Термін виконання", help_text="Оберіть дату та час для зворотного відліку")
    is_done = models.BooleanField(default=False) 
 
class Habit(models.Model):
    name = models.CharField(max_length = 100)
    last_reset = models.DateField(auto_now=True)
 

class HabitCheck(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='checks')
    week_number = models.IntegerField()
    year = models.IntegerField()
    day_of_week = models.IntegerField()  
 
    class Meta:
        unique_together = ('habit', 'week_number', 'year', 'day_of_week')
