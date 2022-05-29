import os
from PIL import ImageGrab
import mail
from utils import *

def SHUTDOWN(req):
    os.system('shutdown /s /t 1')
    res = mail.new_instance()
    res['receiver'] = req['sender']
    res['subject'] = 'Response for your {} query'.format(current_function_name())
    res['content'] = 'Computer shutdown at {}'.format(current_date_in_format())
    return res
def RESTART(req):
    os.system('shutdown /r /t 1')
    res = mail.new_instance()
    res['receiver'] = req['sender']
    res['subject'] = 'Response for RESTART query'
    res['content'] = 'Computer restarted at {}'.format(current_date_in_format())
    return res
def LIST_PROCESS(req): 
    process_list = os.popen('tasklist').read()
    res = mail.new_instance()
    res['receiver'] = req['sender']
    res['subject'] = 'Process list at {}'.format(current_date_in_format())
    res['content'] = process_list
    return res
def STOP_PROCESS_BY_NAME(req):
    process_name = req['subject'].split()[-1]
    content = run('Stop-Process -Name "{}"'.format(process_name)).stdout.decode('utf-8')
    res = mail.new_instance()
    res['receiver'] = req['sender']
    res['subject'] = 'Response for stop_process_name query'
    res['content'] = content
    return res
def STOP_PROCESS_BY_ID(req):
    process_id = req['subject'].split()[-1]
    content = run('Stop-Process -Id {}'.format(process_id)).stdout.decode('utf-8')
    res = mail.new_instance()
    res['receiver'] = req['sender']
    res['subject'] = 'Response for stop_process_id query'
    res['content'] = content
    return res
def OPEN_URL(req):
    url = req['subject'].split()[-1]
    content = os.system('start {}'.format(url))
    res = mail.new_instance()
    res['receiver'] = req['sender']
    res['subject'] = 'Response for open_website query'
    res['content'] = content
    return res
def OPEN_FILE(req):
    file_path = req['subject'].split()[-1]
    content = os.system('start {}'.format(file_path))
    res = mail.new_instance()
    res['receiver'] = req['sender']
    res['subject'] = 'Response for open_file query'
    res['content'] = content
    return res
def SCREENSHOT(req):
    file_path="screenshot.png"
    ImageGrab.grab().save(file_path)
    res = mail.new_instance()
    res['receiver'] = req['sender']
    res['subject'] = 'Screenshot taken at {}'.format(current_date_in_format())
    res['file'] = [file_path]
    return res
def COPY_FILE(req):
    file_path, destination_path = req.subject.split(' ')[-2:]
    content = run('Copy-Item "{}" -Destination "{}"'.format(file_path, destination_path))
    res = mail.new_instance()
    res['receiver'] = req['sender']
    res['subject'] = 'Response for copy_file query'
    res['content'] = content
    return res
def MOVE_FILE(req):
    file_path, destination_path = req.subject.split(' ')[-2:]
    content = run('Move-Item "{}" -Destination "{}"'.format(file_path, destination_path))
    res = mail.new_instance()
    res['receiver'] = req['sender']
    res['subject'] = 'Response for move_file query'
    res['content'] = content
    return res
def DELETE_FILE(req):
    file_path = req['subject'].split()[-1]
    content = run('Remove-Item "{}"'.format(file_path))
    res = mail.new_instance()
    res['receiver'] = req['sender']
    res['subject'] = 'Response for delete_file query'
    res['content'] = content
    return res
def CREATE_FOLDER(req):
    folder_path = req['subject'].split()[-1]
    content = run('mkdir "{}"'.format(folder_path))
    res = mail.new_instance()
    res['receiver'] = req['sender']
    res['subject'] = 'Response for create_folder query'
    res['content'] = content
    return res
def CREATE_FILE(req):
    file_path = req['subject'].split()[-1]
    content = run('New-Item -Path "{}"'.format(file_path))
    res = mail.new_instance()
    res['receiver'] = req['sender']
    res['subject'] = 'Response for create_file query'
    res['content'] = content
    return res
def WRITE_FILE(req):
    file_path = req['subject'].split()[-1]
    content = req['content']
    with open(file_path, 'w') as f:
        f.write(content)
    res = mail.new_instance()
    res['receiver'] = req['sender']
    res['subject'] = 'Response for write_file query'
    res['content'] = content
def READ_FILE(req):
    file_path = req['subject'].split()[-1]
    res = mail.new_instance()
    res['receiver'] = req['sender']
    res['subject'] = 'File content at {}'.format(current_date_in_format())
    res['body'] = open(file_path, 'r').read()
    return res
def RUN_COMMAND(req):
    command = req['subject'].split()[-1]
    res = mail.new_instance()
    res['receiver'] = req['sender']
    res['subject'] = 'Command output at {}'.format(current_date_in_format())
    res['body'] = run(command).stdout.decode('utf-8')
    return res
def RECORD_VIDEO(req):
    duration = req['subject'].split()[-1]
    record(duration=duration)
    res = mail.new_instance()
    res['receiver'] = req['sender']
    res['subject'] = 'Video recording at {}'.format(current_date_in_format())
    res['file'] = ['video.mp4']
    return res

# list of all available commands    
EXECUTE = []
for key, value in list(locals().items()):
        if callable(value) and value.__module__ == __name__:
            EXECUTE.append(key)
