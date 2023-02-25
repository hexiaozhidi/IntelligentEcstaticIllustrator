from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import Task, Image, Prompt

from .Payload import Payload

import json
from os import path, makedirs

outputs_dir = 'iei/static/iei/images/outputs'


def index(request):
    context = {'latest_tasks': []}
    for task in Task.objects.filter(time_created__lte=timezone.now()).order_by('-time_created')[:5]:
        task_info = {'task_id': task.task_id, 'status': Task.Status(task.status).label, 'images': []}
        if task.status == Task.Status.SUCCESSFUL:
            for image in Image.objects.filter(task_id=task.task_id):
                task_info['images'].append(
                    {'image_id': image.image_id, 'image_url': f'iei/images/outputs/{image.image_id}.png'})

        context['latest_tasks'].append(task_info)

    return render(request, 'iei/index.html', context)


def create_task(request):
    return render(request, 'iei/create_task.html')


def create_task_post(request):
    payload = Payload(
        prompt=request.POST.get('prompt'),
        negative_prompt=request.POST.get('negative_prompt'),
        steps=int(request.POST.get('steps')),
        sampler_name=request.POST.get('sampler_name'),
        width=int(request.POST.get('width')),
        height=int(request.POST.get('height')),
        restore_faces=bool(request.POST.get('restore_faces')),
        tiling=bool(request.POST.get('tiling')),
        enable_hr=bool(request.POST.get('enable_hr')),
        firstphase_width=int(request.POST.get('firstphase_width')),
        firstphase_height=int(request.POST.get('firstphase_height')),
        denoising_strength=float(request.POST.get('denoising_strength')),
        n_iter=int(request.POST.get('n_iter')),
        batch_size=int(request.POST.get('batch_size')),
        cfg_scale=float(request.POST.get('cfg_scale')),
        seed=int(request.POST.get('seed')),
        subseed=int(request.POST.get('subseed')),
        subseed_strength=float(request.POST.get('subseed_strength')),
        seed_resize_from_w=int(request.POST.get('seed_resize_from_w')),
        seed_resize_from_h=int(request.POST.get('seed_resize_from_h')),
        eta=float(request.POST.get('eta')),
        s_churn=float(request.POST.get('s_churn')),
        s_tmin=float(request.POST.get('s_tmin')),
        s_noise=float(request.POST.get('s_noise'))
    )

    Task.objects.create(
        status=Task.Status.WAITING,
        time_created=timezone.now(),
        time_finished=timezone.now(),
        payload=payload.__dict__
    )

    return HttpResponseRedirect(reverse('iei:index'))


def get_waiting_task(request):
    response = '{"task_id": -1, "payload": {}}'
    with transaction.atomic():
        task = Task.objects.filter(status=Task.Status.WAITING).order_by('time_created')[:1]
        if task:
            task = task[0]
            response = f'{{"task_id": {task.task_id}, "payload": {json.dumps(task.payload)}}}'
            task.status = Task.Status.PROCESSING
            task.save()

    return HttpResponse(response)


@csrf_exempt
def post_processed_task(request):
    if not path.exists(outputs_dir):
        makedirs(outputs_dir)

    task_id = request.POST['task_id']
    status = Task.Status(request.POST['status'])
    error_massage = ''

    if status == Task.Status.SUCCESSFUL:
        images = request.POST['images'].split('\n')
        for file_name in images:
            image_data = request.FILES.get(file_name)
            if not image_data:
                status = Task.Status.FAILED
                error_massage = f'Task #{task_id} without image: {file_name}'
                break
    else:
        error_massage = request.POST['error']

    # Failed
    if status == Task.Status.FAILED:
        task = Task.objects.get(task_id=task_id)
        task.status = Task.Status.FAILED
        task.time_finished = timezone.now()
        task.save()
        return HttpResponse(f'post_processed_task FAILED: {error_massage}')

    # Successful
    task = Task.objects.get(task_id=task_id)
    images = request.POST['images'].split('\n')
    for file_name in images:
        image_id = file_name.split('.')[0]
        Image.objects.create(image_id=image_id, task_id=task_id)
        for prompt in task.payload['prompt'].split(','):
            Prompt.objects.create(prompt=prompt.strip(' ()'), image_id=image_id)

        image_data = request.FILES.get(file_name)
        with open(f'{outputs_dir}/{file_name}', 'wb+') as file:
            for chunk in image_data.chunks():
                file.write(chunk)

    task.status = Task.Status.SUCCESSFUL
    task.time_finished = timezone.now()
    task.save()

    return HttpResponse(
        f'post_processed_task accomplished: ' +
        f'Task #{task_id} with {len(images)} image{"s" if len(images) > 1 else ""}: \n' +
        request.POST['images'])
