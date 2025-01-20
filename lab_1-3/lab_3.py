import cv2
import time

def process_video():
    cap = cv2.VideoCapture(1)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')

    if face_cascade.empty() or eye_cascade.empty() or smile_cascade.empty():
        print("Error loading face cascade.")
        exit()

    prev_frame_time = 0
    new_frame_time = 0

    while(True):
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        new_frame_time = time.time()
        fps = 1/(new_frame_time-prev_frame_time)
        prev_frame_time = new_frame_time
        fps = int(fps)
        fps = str(fps)

        cv2.putText(frame, fps, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray_eyes = gray[y:y + int(h * 0.7), x:x + w]
            roi_color_eyes = frame[y:y + int(h * 0.7), x:x + w]
            roi_gray_smile = gray[y + int(h * 0.5):y + h, x:x + w]
            roi_color_smile = frame[y + int(h * 0.5):y + h, x:x + w]

            eyes = eye_cascade.detectMultiScale(roi_gray_eyes, scaleFactor=1.1, minNeighbors=8, minSize=(10, 10))
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color_eyes, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

            smile = smile_cascade.detectMultiScale(roi_gray_smile, scaleFactor=1.7, minNeighbors=22, minSize=(25, 25))
            if not len(smile):
                cv2.putText(frame, "Smile!", (x, y - 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                for (sx, sy, sw, sh) in smile:
                    cv2.rectangle(roi_color_smile, (sx, sy), (sx + sw, sy + sh), (0, 0, 255), 2)

            eyes_detected = len(eyes)
            if eyes_detected != 2:
                cv2.putText(frame, "Open your eyes!", (x, y - 70 if not len(smile) else y - 100),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 0, 255), 2)
                cv2.putText(frame, f"Eyes detected: {eyes_detected}", (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                            (0, 255, 0), 2)

            cv2.imshow('Face', roi_color_eyes)

        cv2.imshow('Camera Feed', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    process_video()