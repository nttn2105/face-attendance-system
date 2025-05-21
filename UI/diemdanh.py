import cv2
import numpy as np
from PIL import Image, ImageTk
import os
import datetime
from tensorflow.keras.models import load_model
import tkinter as tk
import sys
sys.stdout.reconfigure(encoding='utf-8')
cap = None
after_id = None
recognized_today = set()  

def start_face_recognition(video_label, listbox_attended=None):
    global cap, after_id, recognized_today

    today = datetime.datetime.now().strftime("%Y-%m-%d")
    attendance_file = f"diemdanh_{today}.csv"

    label_dir = r'C:\Users\Doan Quy\Desktop\Project_Final_CV\Train'
    class_names = os.listdir(label_dir)

    faceDetectionProto = r"C:\Users\Doan Quy\Desktop\Project_Final_CV\Lib\deploy.prototxt.txt"
    faceDetectionModel = r"C:\Users\Doan Quy\Desktop\Project_Final_CV\Lib\res10_300x300_ssd_iter_140000_fp16 (1).caffemodel"
    faceNet = cv2.dnn.readNetFromCaffe(faceDetectionProto, faceDetectionModel)

    model = load_model(r'C:\Users\Doan Quy\Desktop\Project_Final_CV\notebook\face_MobileNet_model_8.h5')

    cap = cv2.VideoCapture(0)

    def mark_attendance(name):
        if name not in recognized_today:
            recognized_today.add(name)

            with open(attendance_file, "a", encoding="utf-8") as f:
                now = datetime.datetime.now().strftime("%H:%M:%S")
                f.write(f"{name},{today},{now}\n")

            if listbox_attended:
                listbox_attended.insert(tk.END, name)

    def update_frame():
        global after_id, cap

        ret, frame = cap.read()
        if not ret:
            print("Không lấy được frame từ camera.")
            return

        h, w = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0))
        faceNet.setInput(blob)
        detections = faceNet.forward()

        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (x1, y1, x2, y2) = box.astype("int")
                padding = 20
                x1 = max(0, x1 - padding)
                y1 = max(0, y1 - padding)
                x2 = min(w, x2 + padding)
                y2 = min(h, y2 + padding)
                face = frame[y1:y2, x1:x2]
                try:
                    face_input = cv2.resize(face, (224, 224))
                    face_input = face_input.astype("float32") / 255.0
                    face_input = np.expand_dims(face_input, axis=0)

                    preds = model.predict(face_input)
                    class_id = np.argmax(preds)
                    confidence_pred = np.max(preds)

                    label = f"{class_names[class_id]} ({confidence_pred:.2f})"
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, label, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

                    # Nếu độ tin cậy > 0.85 thì điểm danh
                    if confidence_pred > 0.85:
                        name_only = class_names[class_id]
                        mark_attendance(name_only)

                except Exception as e:
                    print("Lỗi xử lý:", e)

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb_frame)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.config(image=imgtk)

        after_id = video_label.after(10, update_frame)

    update_frame()
def stop_face_recognition(video_label):
    global cap, after_id
    if cap is not None:
        cap.release()
        cap = None
    if after_id is not None:
        video_label.after_cancel(after_id)
        after_id = None
    video_label.config(image='', bg="#F4BABA")