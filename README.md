This project implements a face recognition-based attendance system using deep neural networks (DNNs). It detects faces using a pre-trained Caffe model and recognizes them using a MobileNetV2-based classifier. The goal is to automate worker attendance tracking in an efficient and contactless manner.

## Features

- 🔍 **Face Detection** using OpenCV's DNN module with a `.caffemodel`.
- 🤖 **Face Recognition** using a MobileNetV2 deep learning model trained on custom worker face data.
- 📸 Real-time webcam input or image/video processing.
- 📝 Automatic attendance logging.
- 💾 Easy to extend with new worker data.

## Technologies Used

- Python 3
- OpenCV (for face detection)
- TensorFlow / Keras (for training MobileNetV2)
- NumPy, Pandas
- Caffe pre-trained model (`deploy.prototxt`, `res10_300x300_ssd_iter_140000.caffemodel`)
