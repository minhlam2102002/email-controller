from tkinter import *
from tkinter import ttk
import dotenv
import platform
import controller
from textwrap import dedent
import os
from server import *
from utils import *

OS_NAME = platform.system()
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)
KEY = os.getenv("KEY")
if KEY == "NULL":
    KEY = get_random_string()
    dotenv.set_key(dotenv_file, "KEY", KEY)
PADX = 20
WIDTH = 700
HEIGHT = 550
app = Tk()
app.title('Email Controller')
app.resizable(width=False, height=False)
app.geometry("{}x{}".format(WIDTH, HEIGHT))
app.option_add("*Font", "Lucida 10")
# img = PhotoImage(file="background.png")

def show_border(window):
    for child in window.winfo_children():
        child.config(highlightbackground="black", highlightcolor="black", highlightthickness=1)
def clear(window):
    for child in window.winfo_children():
        child.destroy()
    # img_label = Label(app, image=img)
    # img_label.place(x=0, y=0)
def back_button(cmd):
    back_button = Button(app, text="Back", command=cmd)
    back_button.pack(anchor="w")
def handle_guide_button():
    clear(app)
    main_frame = Frame(app, width=WIDTH, height=HEIGHT)
    main_frame.place(x=0, y=20)
    back_button(start)

    Label(main_frame, text='Hướng dẫn sử dụng', font="Helvetica 20 bold").pack()
    Label(main_frame, text='!!! ỨNG DỤNG CHỈ SỬ DỤNG CHO HỆ ĐIỀU HÀNH WINDOWS !!!', font="Helvetica 8 italic").pack()
    Label(main_frame, text=dedent(
    '''
    Đầu tiên, bạn cần phải khởi tạo key dành cho riêng bạn. Nó giống như password của bạn vậy.
    Sau đó, bạn có thể sử dụng key để gửi các yêu cầu vào email để thao tác với máy tính của bạn.
    Cú pháp gửi email để thao tác với máy tính:'''
    ), justify=LEFT).pack(padx=PADX, anchor="w")
    Label(main_frame, text='Subject: <key> <command> <arguments> (nếu có) ', height=1).pack()
    Label(main_frame, text=dedent(
    '''
    Ví dụ:
    Subject: abcxyz RECORD_VIDEO 10
    Trong đó: abcxyz là key, RECORD_VIDEO là command, 10 là arguments.
    Câu lệnh trên sẽ ghi lại video bằng camera trong 10 giây.
    Các lệnh có thể dùng:'''[1:]
    ), justify=LEFT).pack(padx=PADX, anchor="w")
    for command in controller.COMMANDS:
        frame = Frame(main_frame)
        frame.pack(anchor="w")
        cmd, description = controller.USAGE[command].split(':')
        Label(frame, text=cmd + ':', font="Lucida 10 italic").pack(side=LEFT, anchor="n", padx=(PADX, 0))
        Label(frame, text=description).pack(side=LEFT, anchor="n")

def create_key(key, info_frame):
    dotenv.set_key(dotenv_file, "KEY", key)
    print("Created key {}".format(key))
    info = Label(info_frame, text="Created key successfully")
    info.pack(padx=PADX)
    info.after(2000 , lambda: info.destroy())

def handle_create_key_button():
    clear(app)
    back_button(start)
    entry_frame = Frame(app)
    entry_frame.pack(anchor="w", pady=10)
    info_frame = Frame(app)
    info_frame.pack(anchor="w")
    Label(entry_frame, text="Enter your key:").pack(side=LEFT, anchor="n", padx=(PADX, 0), pady=(3, 0))
    key_entry = Entry(entry_frame, width=30)
    key_entry.insert(0, KEY)
    key_entry.pack(side=LEFT, anchor="n", padx=5, pady=(4, 0))
    Button(entry_frame, text="Create", width=7, command=lambda:create_key(key_entry.get(), info_frame)).pack(side=LEFT, anchor="n")

def start():
    clear(app)
    Label(app, text='Email controller', font="Helvetica 20 bold").pack(pady=70)
    Button(app, text="Read guide", width=20, command=handle_guide_button).pack(pady=(10, 0))
    Button(app, text="Config key", width=20, command=handle_create_key_button).pack(pady=(10, 0))


if __name__ == '__main__':
    print('Starting app...')
    start()
    # controller.start_listening_email()
    app.mainloop()
