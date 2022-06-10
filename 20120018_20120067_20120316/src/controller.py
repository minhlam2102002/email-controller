from PIL import ImageGrab
from mail import *
from textwrap import dedent
from utils import *
import os, keyboard, time

def SHUTDOWN(req):
    res = create_mail(
        plain_content='Computer shutdown at {}'.format(time_in_format()),
        original=req
    )
    send_mail(res)
    os.system('shutdown /s')
SHUTDOWN.__doc__ = 'SHUTDOWN: tắt máy tính'

def RESTART(req):
    res = create_mail(
        plain_content='Computer restart at {}'.format(time_in_format()),
        original=req
    )
    send_mail(res)
    os.system('shutdown /r')
RESTART.__doc__ = 'RESTART: khởi động lại máy tính'

def LIST_PROCESS(req): 
    process_list = os.popen('tasklist').read()
    res = create_mail(
        plain_content='Process list at {} \n\n{}'.format(time_in_format(), process_list),
        original=req,
    )
    return res
LIST_PROCESS.__doc__ = 'LIST_PROCESS: lấy danh sách các tiến trình đang chạy'

def STOP_PROCESS_BY_NAME(req):
    process_name = req['Subject'].split()[-1]
    content = os.popen('taskkill /f /im {}'.format(process_name)).read()
    res = create_mail(
        plain_content='Process {} is stopped at {}\n\n{}'.format(process_name, time_in_format(), content),
        original=req
    )
    return res
STOP_PROCESS_BY_NAME.__doc__ = 'STOP_PROCESS_BY_NAME <process_name>: tắt tiến trình theo tên <process_name>'

def STOP_PROCESS_BY_ID(req):
    process_id = req['Subject'].split()[-1]
    content = os.popen('taskkill /f /pid {}'.format(process_id)).read()
    res = create_mail(
        plain_content='Process {} is stopped at {}\n\n{}'.format(process_id, time_in_format(), content),
        original=req
    )
    return res
STOP_PROCESS_BY_ID.__doc__ = 'STOP_PROCESS_BY_ID <process_id>: tắt tiến trình theo id <process_id>'

def SCREENSHOT(req):
    file_path = 'logs/mail/' + clean_file_name(req['Message-ID']) + '_screenshot.png'
    ImageGrab.grab().save(file_path)
    res = res = create_mail(
        plain_content='Screenshot is taken at {}'.format(time_in_format()),
        attachments=[file_path],
        alias_attachment_name=['screenshot.png'],
        original=req
    )
    return res
SCREENSHOT.__doc__ = 'SCREENSHOT: chụp màn hình hiện tại'

def RECORD_VIDEO(req):
    duration = req['Subject'].split()[-1]
    duration = int(duration)
    file_path = 'logs/mail/' + clean_file_name(req['Message-ID']) + '_record.mp4'
    file_format = os.path.basename(file_path).split('.')[-1]
    record(duration=duration, file_path=file_path, file_format=file_format)
    res = create_mail(
        plain_content='Video recording at {} for {} seconds.'.format(time_in_format(), duration),
        original=req,
        attachments=[file_path],
        alias_attachment_name=['record.{}'.format(file_format)]
    )
    return res
RECORD_VIDEO.__doc__ = 'RECORD_VIDEO <duration>: record video từ camera trong khoảng thời gian <duration> (giây)'


def COPY_FILE(req):
    source_path, destination_path = req['Subject'].split()[2:]
    content = os.popen('copy {} {}'.format(source_path, destination_path)).read()
    res = create_mail(
        plain_content='Copy file at {}\n\n{}'.format(time_in_format(), content),
        original=req
    )
    return res
COPY_FILE.__doc__ = 'COPY_FILE <source_path> <dest_path>: copy file từ <source_path> sang <dest_path>'

def RUN_COMMAND(req):
    command = req['Subject'].split()[2:]
    command = ' '.join(command)
    content = os.popen(command).read()
    res = create_mail(
        plain_content='Command {} is executed at {}.\n\n{}'.format(command, time_in_format(), content),
        original=req
    )
    return res
RUN_COMMAND.__doc__ = 'RUN_COMMAND <command>: chạy lệnh <command>'

def CATCH_KEYPRESS(req):
    duration = req['Subject'].split()[-1]
    duration = int(duration)
    key_pressed = keyboard.start_recording()
    time.sleep(duration)
    keyboard.stop_recording()
    key_pressed = list(key_pressed[0].queue)
    content = ''
    for key in key_pressed:
        content += key.name + ' ' + key.event_type + '\n'
    res = create_mail(
        plain_content='Keyboard event from {} in {} second\n\n{}'.format(time_in_format(), duration, content),
        original=req
    )
    return res
CATCH_KEYPRESS.__doc__ = 'CATCH_KEYPRESS <duration>: bắt phím nhấm trong khoảng thời gian <duration> (giây)'

def SET_REGISTRY(req):
    reg_path, name, value = req['Subject'].split()[2:]
    content = set_registry(reg_path, name, value)
    res = create_mail(
        plain_content='Registry {} is set at {}\n\n{}'.format(reg_path, time_in_format(), content),
        original=req
    )
    return res
SET_REGISTRY.__doc__ = 'SET_REGISTRY <reg_path> <name> <value>: cập nhật giá trị <value> cho registry <name> trong <reg_path>'
def GET_REGISTRY(req):
    reg_path, name = req['Subject'].split()[2:]
    content = get_registry(reg_path, name)
    res = create_mail(
        plain_content='Registry {} is get at {}\n\n{}'.format(reg_path, time_in_format(), content),
        original=req
    )
    return res
GET_REGISTRY.__doc__ = 'GET_REGISTRY <reg_path> <name>: lấy giá trị của registry <name> trong <reg_path>'
COMMANDS = []
EXECUTE = {}
USAGE = {}
for key, value in list(locals().items()):
        if callable(value) and value.__module__ == __name__:
            COMMANDS.append(key)
            EXECUTE[key] = value
            USAGE[key] = value.__doc__

def HELP(req, isInvalid=False):
    content = '''
    !!! ỨNG DỤNG CHỈ SỬ DỤNG CHO HỆ ĐIỀU HÀNH WINDOWS !!!
    Đầu tiên, bạn cần phải khởi tạo key dành cho riêng bạn. Nó giống như password của bạn vậy.
    Sau đó, bạn có thể sử dụng key để gửi các yêu cầu vào email để thao tác với máy tính của bạn.
    Cú pháp gửi email để thao tác với máy tính:
    Subject: <key> <command> <arguments> (nếu có)
    Ví dụ:
    Subject: abcxyz RECORD_VIDEO 10
    Trong đó: abcxyz là key, RECORD_VIDEO là command, 10 là arguments.
    Câu lệnh trên sẽ ghi lại video bằng camera trong 10 giây.
    Các lệnh có thể dùng:
    '''
    content = dedent(content)
    for command in COMMANDS:
        content += USAGE[command] + '\n'
    content += 'HELP: hiển thị danh sách các lệnh có thể dùng'
    if isInvalid:
        content = '!!! Câu lệnh không hợp lệ !!!\n\n' + content
    res = create_mail(
        plain_content=content,
        original=req
    )
    return res
HELP.__doc__ = 'HELP: hiển thị danh sách các lệnh có thể dùng'
COMMANDS.append('HELP')
EXECUTE['HELP'] = HELP
USAGE['HELP'] = HELP.__doc__
