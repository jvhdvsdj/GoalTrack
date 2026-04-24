from django.db import models

class Task(models.Model):
    title = models.CharField(max_length = 200)
    description = models.TextField()
    deadline = models.DateTimeField(null=True, blank=True, verbose_name="Термін виконання", help_text="Оберіть дату та час для зворотного відліку")
