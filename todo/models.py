from django.db import models

states = [('todo', 'Todo'), ('in-progress', 'In Progress'), ('done', 'Done')]


class Todo(models.Model):
    title = models.CharField(max_length=200)
    state = models.CharField(choices=states, default='todo', max_length=15)
    due_date = models.DateField('due_date')
    description = models.TextField()

    def __str__(self):
        return self.title
