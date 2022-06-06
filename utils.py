import cv2
from datetime import datetime
import logging
import random
import os

def get_random_string(length=10):
    return ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for i in range(length))
def record(file_path='record.mp4', file_format='mp4', duration=5, FPS = 30, WIDTH = 640, HEIGHT = 480):
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if file_format == 'avi':
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
    elif file_format == 'mp4':
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    else:
        logging.error('Invalid file format')
        return
    out = cv2.VideoWriter(file_path, fourcc, FPS, (WIDTH, HEIGHT))
    frame_count = 0
    total_frames = duration * FPS
    logging.info('Start recording')
    while True:
        ret, frame = cap.read()
        frame_count += 1
        if ret == True:
            frame = cv2.flip(frame,1)
            out.write(frame)
            cv2.imshow('Recording...', frame)
            if frame_count == total_frames:
                break
        else:
            break
    logging.info('Stop recording')
    cap.release()
    out.release()
    cv2.destroyAllWindows()
def clean_file_name(text):
    return "".join(c if c.isalnum() else "_" for c in text)

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
def time_in_format(format=DATE_FORMAT):
    return datetime.now().strftime(format)

def extract_mail_address(mail_address):
    return mail_address[mail_address.index('<') + 1:mail_address.index('>')]

def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)