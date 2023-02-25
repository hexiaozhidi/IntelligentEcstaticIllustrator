from django.urls import path

from . import views

app_name = 'iei'
urlpatterns = [
    path('', views.index, name='index'),
    path('create_task', views.create_task, name='create_task'),
    path('create_task_post', views.create_task_post, name='create_task_post'),
    path('get_waiting_task', views.get_waiting_task, name='get_waiting_task'),
    path('post_processed_task', views.post_processed_task, name='post_processed_task')
]
