import subprocess
import cv2
from datetime import datetime
import inspect

def run(cmd):
    completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    return completed
def record(file_name='output', file_format='avi', duration=5, FPS = 20, WIDTH = 640, HEIGHT = 480):
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if file_format == 'avi':
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
    elif file_format == 'mp4':
        fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    else:
        print('Invalid file format')
        return
    out = cv2.VideoWriter(file_name + '.' + file_format, fourcc, FPS, (WIDTH, HEIGHT))
    frame_count = 0
    total_frames = duration * FPS
    while True:
        ret, frame = cap.read()
        frame_count += 1
        if ret == True:
            frame = cv2.flip(frame,1)
            out.write(frame)
            cv2.imshow('Recording...', frame)
            if frame_count == total_frames:
                break
            # press q to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    out.release()
    cv2.destroyAllWindows()
def clean_file_name(text):
    return "".join(c if c.isalnum() else "_" for c in text)
def current_date_in_format():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
def get_prefix(text, n):
    if len(text) < n:
        return text
    return text[:n]
def current_function_name():
    return inspect.stack()[1].function  