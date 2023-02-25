import base64
import io

from PIL import Image, PngImagePlugin
import requests
from time import sleep
from multiprocessing import Process

from sys import path as sys_path
from os import mkdir, rename, path

from hashlib import md5

sys_path.append('A:\\stable-diffusion-webui')
from launch import start as start_webui

env_path = '../env'

url_webui_api = 'http://127.0.0.1:7861/sdapi/v1'
url_txt2img = url_webui_api + '/txt2img'
url_png_info = url_webui_api + '/png-info'

url_iei_server = 'http://127.0.0.1:8000/iei'
url_get_waiting_task = url_iei_server + '/get_waiting_task'
url_post_processed_task = url_iei_server + '/post_processed_task'

outputs_dir = 'outputs'


def initialize_webui():
    webui = Process(target=start_webui)
    webui.start()

    for _ in range(60):
        try:
            requests.post(url=url_webui_api)
            return webui
        except requests.exceptions.ConnectionError:
            sleep(1)

    webui.terminate()
    print('Starting webui FAILED.')
    return None


def process_task(task):
    task_id = task.get('task_id')
    if not task_id or task_id < 0:
        return

    print(f'Processing Task #{task_id}...')
    webui = initialize_webui()
    if not webui:
        error_massage = 'Initializing webui FAILED.'
        data = {'task_id': task_id, 'status': 'F', 'error': error_massage}
        response_post_processed_task = requests.post(url=url_post_processed_task, data=data)
        print(f'Task #{task_id} FAILED. Reason: {error_massage}')
        return

    response_txt2img = requests.post(url=url_txt2img, json=task['payload'])
    if response_txt2img.status_code != 200:
        sleep(2)
        webui.terminate()
        error_massage = 'Generating images FAILED.'
        data = {'task_id': task_id, 'status': 'F', 'error': error_massage}
        response_post_processed_task = requests.post(url=url_post_processed_task, data=data)
        print(f'Task #{task_id} FAILED. Reason: {error_massage}')
        return

    result = response_txt2img.json()['images']
    file_names = []
    files = {}
    for image_id in range(len(result)):
        tmp_file_name = f'{task_id}_{image_id}.png'
        image = Image.open(io.BytesIO(base64.b64decode(result[image_id].split(',', 1)[0])))
        png_payload = {'image': f'data:image/png;base64,{result[image_id]}'}
        response_png_info = requests.post(url=url_png_info, json=png_payload)
        png_info = PngImagePlugin.PngInfo()
        png_info.add_text('parameters', response_png_info.json()['info'])
        image.save(tmp_file_name, pnginfo=png_info)

        file = open(tmp_file_name, 'rb')
        md5_hash = md5()
        md5_hash.update(file.read())
        file.seek(0)
        file_name = f'{md5_hash.hexdigest()}.png'
        file_names.append(file_name)
        files[file_name] = file

    data = {'task_id': task_id, 'status': 'S', 'images': '\n'.join(file_names)}
    response_post_processed_task = requests.post(url=url_post_processed_task, data=data, files=files)
    print(response_post_processed_task.text)

    for image_id in range(len(file_names)):
        tmp_file_name = f'{task_id}_{image_id}.png'
        file_name = file_names[image_id]
        files[file_name].close()
        rename(tmp_file_name, f'{outputs_dir}/{file_name}')

    webui.terminate()
    print(f'Task #{task["task_id"]} accomplished.')
    return


if __name__ == '__main__':
    env_vars = {}
    if path.exists(env_path):
        with open(env_path, 'r') as file:
            for line in file.readlines():
                var = line.strip().split('=')
                if len(var) == 2:
                    env_vars[var[0]] = var[1]

    if env_vars.get('url_iei_server'):
        url_iei_server = env_vars['url_iei_server']
        url_get_waiting_task = url_iei_server + '/get_waiting_task'
        url_post_processed_task = url_iei_server + '/post_processed_task'

    if not path.exists(outputs_dir):
        mkdir(outputs_dir)

    print('IEI Factory started.')
    print(f'IEI Server: {url_iei_server}')

    while True:
        response_get_waiting_task = requests.get(url=url_get_waiting_task)
        waiting_task = response_get_waiting_task.json()
        process_task(waiting_task)
        sleep(5)
