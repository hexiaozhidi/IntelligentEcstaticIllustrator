from django.contrib import admin

from .models import Task, Image, Prompt

admin.site.register(Task)
admin.site.register(Image)
admin.site.register(Prompt)
