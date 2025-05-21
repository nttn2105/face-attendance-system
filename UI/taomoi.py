cap = None
after_id = None
def capture_images(name, birth, video_label):
    import cv2
    import os
    import time
    from PIL import Image, ImageTk

    folder_name = f"{name}_{birth}"
    test_folder = f"C:/Users/Doan Quy/Desktop/Project_Final_CV/Test/{folder_name}"
    train_folder = f"C:/Users/Doan Quy/Desktop/Project_Final_CV/Train/{folder_name}"
    os.makedirs(test_folder, exist_ok=True)
    os.makedirs(train_folder, exist_ok=True)

    net = cv2.dnn.readNetFromCaffe(
        r"C:\Users\Doan Quy\Desktop\Project_Final_CV\Lib\deploy.prototxt.txt",
        r"C:\Users\Doan Quy\Desktop\Project_Final_CV\Lib\res10_300x300_ssd_iter_140000_fp16 (1).caffemodel"
    )

    cap = cv2.VideoCapture(0)
    image_count = 0

    def process_frame():
        nonlocal image_count
        ret, frame = cap.read()
        if not ret:
            return

        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104, 177, 123), swapRB=False)
        net.setInput(blob)
        faces = net.forward()

        h, w = frame.shape[:2]

        for i in range(faces.shape[2]):
            confidence = faces[0, 0, i, 2]
            if confidence > 0.5:
                padding = 20  # bạn có thể tăng/giảm số này để mở rộng thêm

                startx = max(0, int(faces[0, 0, i, 3] * w) - padding)
                starty = max(0, int(faces[0, 0, i, 4] * h) - padding)
                endx = min(w, int(faces[0, 0, i, 5] * w) + padding)
                endy = min(h, int(faces[0, 0, i, 6] * h) + padding)
                cv2.rectangle(frame, (startx, starty), (endx, endy), (0, 255, 0), 2)

                face_img = frame[starty:endy, startx:endx]
                if face_img.size > 0:
                    grayFace_resized = cv2.resize(face_img, (224, 224))
                    folder_path = test_folder if image_count < 80 else train_folder
                    file_path = os.path.join(folder_path, f"{folder_name}_{image_count+1}.jpg")
                    cv2.imwrite(file_path, grayFace_resized)
                    
                    image_count += 1

                    if image_count >= 400:
                        cap.release()
                        return

        # Convert frame to ImageTk and show on label
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb_frame)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.config(image=imgtk)

        # Lặp lại sau 10ms
        video_label.after(10, process_frame)

    process_frame()

def stop_capture_images(video_label):
    global cap, after_id
    if cap is not None:
        cap.release()
        cap = None
    if after_id is not None:
        video_label.after_cancel(after_id)
        after_id = None
    video_label.config(image='', bg="#F4BABA")

