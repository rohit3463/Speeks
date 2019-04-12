import cv2
import numpy as np
from keras.models import load_model
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session
import dlib

config = tf.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.1
set_session(tf.Session(config=config))

detector = dlib.get_frontal_face_detector()

video_capture = cv2.VideoCapture(0)
model = load_model('model_5-49-0.62.hdf5')
model.get_config()

target = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
font = cv2.FONT_HERSHEY_SIMPLEX
while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    (h_frame, w_frame) = frame.shape[:2]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(gray, 1)

    for face in faces:
        (x1, y1, x2, y2) = (face.left(), face.top(), face.right(), face.bottom())
        x = int(x1)
        y = int(y1)
        w = int(x2 - x1)
        h = int(y2 - y1)
        x = int(x - 0.1*w) if int(x - 0.1*w)>0 else 0
        y = int(y - 0.1*h) if int(y - 0.1*h)>0 else 0
        w = int(w + 0.2*w) if int(w + 0.2*w)<w_frame else w_frame-1
        h = int(h + 0.2*h) if int(h + 0.2*h)<h_frame else h_frame-1
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2, 5)
        face_crop = frame[y:y + h, x:x + w]
        face_crop = cv2.resize(face_crop, (48, 48))
        face_crop = cv2.cvtColor(face_crop, cv2.COLOR_BGR2GRAY)
        face_crop = face_crop.astype('float32') / 255
        face_crop = np.asarray(face_crop)
        face_crop = face_crop.reshape(1, 1, face_crop.shape[0], face_crop.shape[1])
        result = target[np.argmax(model.predict(face_crop))]
        cv2.putText(frame, result, (x, y), font, 1, (200, 0, 0), 3, cv2.LINE_AA)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
