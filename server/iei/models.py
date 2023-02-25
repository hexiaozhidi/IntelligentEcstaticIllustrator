from django.db import models
from django.utils.translation import gettext_lazy as _


class Task(models.Model):
    class Status(models.TextChoices):
        WAITING = 'W', _('Waiting')
        PROCESSING = 'P', _('Processing')
        SUCCESSFUL = 'S', _('Successful')
        FAILED = 'F', _('Failed')

    task_id = models.BigAutoField(primary_key=True)
    status = models.CharField(max_length=1, choices=Status.choices, default=Status.WAITING)
    time_created = models.DateTimeField('Time Created')
    time_finished = models.DateTimeField('Time Finished')
    payload = models.JSONField()

    def __str__(self):
        return f'Task #{self.task_id}'


class Image(models.Model):
    image_id = models.CharField(max_length=32, primary_key=True)
    task_id = models.BigIntegerField()

    def __str__(self):
        return f'Image #{self.task_id}_{self.image_id}'


class Prompt(models.Model):
    prompt = models.CharField(max_length=128)
    image_id = models.CharField(max_length=32)

    class Meta:
        indexes = [models.Index(fields=['prompt'])]

    def __str__(self):
        return self.prompt
