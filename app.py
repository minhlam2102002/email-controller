import tkinter as tk
import controller
import dotenv
import os
import platform

OS_NAME = platform.system()
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

app = tk.Tk()
app.title('Email Controller')
app.resizable(width=False, height=False)
app.geometry("640x480")

def clear(window):
    for child in window.winfo_children():
        child.destroy()

def handle_guide_button():
    clear(app)
    guide = '''
    Hướng dẫn sử dụng
    !!! ỨNG DỤNG CHỈ SỬ DỤNG CHO HỆ THỐNG WINDOWS !!!
    Đầu tiên, bạn cần phải khởi tạo key dành cho riêng bạn. Nó giống như password của bạn vậy.
    Sau đó, bạn có thể sử dụng key để gửi các yêu cầu vào email để thao tác với máy tính của bạn.
    Cú pháp gửi email để thao tác với máy tính:
    Subject: <key> <command> <arguments> (nếu có) 
    Ví dụ:
    Subject: 1234567890 CREATE_FOLDER "D:\\New Folder"
    Các lệnh có thể dùng:
    CREATE_FOLDER: tạo thư mục
    DELETE_FOLDER: xóa thư mục
    CREATE_FILE: tạo file
    DELETE_FILE: xóa file
    SCREENSHOT: chụp màn hình
    COPY_FILE: sao chép file
    MOVE_FILE: di chuyển file
    '''
    tk.Label(app, text=guide).grid(column=0, row=0)

def create_key(key):
    dotenv.set_key(dotenv_file, "KEY", key)
    print("Created key {}".format(key))

def handle_create_key_button():
    clear(app)
    tk.Label(app, text="Enter your key").grid(column=0, row=0)
    create_key_entry = tk.Entry(app)
    create_key_entry.grid(column=1, row=0)

    login_button = tk.Button(app, text="Create", command=lambda:controller.create_key(create_key_entry.get()))
    login_button.grid(column=2, row=0)
def start():
    clear(app)
    guide_button = tk.Button(app, text="Guide", command=handle_guide_button)
    guide_button.grid(column=0, row=0)

    create_key_button = tk.Button(app, text="Create key", command=handle_create_key_button)
    create_key_button.grid(column=1, row=0)


if __name__ == '__main__':
    print('Starting app...')
    start()
    # controller.start_listening_email()
    app.mainloop()