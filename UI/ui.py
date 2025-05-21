import tkinter as tk
import datetime
import cv2
from PIL import Image, ImageTk
from taomoi import capture_images ,stop_capture_images
from diemdanh import start_face_recognition, stop_face_recognition
import threading
from tkinter import messagebox
import os
label_dir = r'C:\Users\Doan Quy\Desktop\Project_Final_CV\Train'
class_names = os.listdir(label_dir)
cap = None
after_id_capture = None
root = tk.Tk()
root.title("Điểm danh hệ thống")
root.geometry("1200x650")
root.configure(bg="#E5E5E5")  # màu nền chính

# ====== CAMERA FRAME ======
camera_frame = tk.LabelFrame(root, text="Camera", bg="#F4BABA", font=("Arial", 10, "bold"))
camera_frame.place(x=30, y=30, width=500, height=400)
video_label = tk.Label(camera_frame, bg="#F4BABA")
video_label.pack(expand=True, fill="both")

# ====== FORM NHẬP DỮ LIỆU ======
form_frame = tk.Frame(root, bg="#D9D9D9")
form_frame.place(x=30, y=460,width=500, height=100)

tk.Label(form_frame, text="Thêm dữ liệu", bg="#D9D9D9", font=("Arial", 10)).grid(row=0, column=0, columnspan=3, sticky="w")
tk.Label(form_frame, text="Họ và tên :", bg="#D9D9D9").grid(row=1, column=0, pady=5, sticky="e")
entry_name = tk.Entry(form_frame, bg="#B41717", fg="white", width=30, state=tk.DISABLED)
entry_name.grid(row=1, column=1, padx=5)

tk.Label(form_frame, text="Năm sinh :", bg="#D9D9D9").grid(row=2, column=0, pady=5, sticky="e")
entry_year = tk.Entry(form_frame, bg="#B41717", fg="white", width=30, state=tk.DISABLED)
entry_year.grid(row=2, column=1, padx=5)

add_button = tk.Button(form_frame, text="ADD", bg="#2E1A81", fg="white", width=10, command=lambda: add_and_start_camera() , state=tk.DISABLED)
add_button.grid(row=1, column=2, rowspan=2, padx=10)

def on_cmr():
    add_button.config(state=tk.NORMAL)
    entry_name.config(state=tk.NORMAL)
    entry_year.config(state=tk.NORMAL)
    messagebox.showinfo("Thông báo", "Nhập họ tên và năm sinh, sau đó nhấn ADD")

# def off_cmr():
#     global cap
#     if cap is not None:
#         cap.release()
#         cap = None
#         video_label.config(image='')
#     messagebox.showinfo("Thông báo", "Đã thu thập thành công.")
#     video_label.configure(image='')  
def off_cmr():
    messagebox.showinfo("Thông báo", "Đã Điểm Danh.")
    stop_capture_images(video_label)

def add_and_start_camera():
    name = entry_name.get().strip()
    birth = entry_year.get().strip()
    if name and birth:
        capture_images(name, birth, video_label)

# ====== CAMERA CONTROL ======
tk.Button(root, text="ON Camera", bg="#2E1A81", fg="white", width=10, command=on_cmr).place(x=70, y=580)
tk.Button(root, text="OFF Camera", bg="#2E1A81", fg="white", width=10, command=off_cmr).place(x=200, y=580)

# ====== ĐIỂM DANH VÀ THỜI GIAN ======
right_frame = tk.Frame(root, bg="#D9D9D9")
right_frame.place(x=600, y=40)

tk.Label(right_frame, text="Điểm danh", bg="#D9D9D9", font=("Arial", 12)).grid(row=0, column=0, sticky="w")

time_label = tk.Label(right_frame, text="", bg="#87B95E", width=55, height=2, font=("Arial", 12, "bold"))
time_label.grid(row=1, column=0, columnspan=2, pady=10)

def update_time():
    now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    time_label.config(text=now)
    root.after(1000, update_time)

update_time()

def run_face_recognition_thread():
    thread = threading.Thread(target=start_face_recognition, args=(video_label, listbox_attended))
    thread.daemon = True
    thread.start()
def off_cmrrr():
    messagebox.showinfo("Thông báo", "Đã Điểm Danh.")
    stop_face_recognition(video_label)

tk.Button(right_frame, text="Điểm danh", bg="#D6C653", width=15, height=2, command=run_face_recognition_thread).grid(row=2, column=0, padx=10, pady=5)
tk.Button(right_frame, text="Dừng", bg="#D6C653", width=15, height=2, command=off_cmrrr).grid(row=2, column=1, padx=10, pady=5)

# ====== DANH SÁCH CÔNG NHÂN VÀ ĐI LÀM ======
list_frame = tk.Frame(root, bg="#D9D9D9")
list_frame.place(x=600, y=200,width=558, height=360)

tk.Label(list_frame, text="Danh sách công nhân", bg="#D9D9D9").grid(row=0, column=0, sticky="w")
tk.Label(list_frame, text="Công nhân đi làm", bg="#D9D9D9").grid(row=0, column=1, sticky="w", padx=40)

listbox_all = tk.Listbox(list_frame, bg="white", width=43, height=40)
listbox_all.grid(row=1, column=0, padx=5)
for name in class_names:
    listbox_all.insert(tk.END, name)
listbox_attended = tk.Listbox(list_frame, bg="white", width=43, height=40)
listbox_attended.grid(row=1, column=1, padx=5)

# ====== THỐNG KÊ ======
tk.Button(root, text="Thống kê", bg="#B83A98", fg="white", width=10).place(x=1050, y=580)

root.mainloop()
