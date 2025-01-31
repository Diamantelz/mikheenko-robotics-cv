import cv2
import numpy as np

def detect_coins(frame, known_diameters, focal_length):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.bilateralFilter(gray, 9, 75, 75)

    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    kernel = np.ones((5, 5),np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) > 100:
            ellipse = cv2.fitEllipse(contour)
            (x, y), (major_axis, minor_axis), angle = ellipse

            pixel_diameter = (major_axis + minor_axis) / 2

            for real_diameter, coin_name in known_diameters.items():
                distance_mm = (real_diameter * focal_length) / pixel_diameter
                distance_cm = distance_mm / 10

                if 5 < distance_cm < 50:
                    cv2.ellipse(frame, ellipse, (0, 255, 0), 2)

    return frame

known_diameters = {25.0: "5 RUB", 23.0: "2 RUB", 20.5: "1 RUB"}

focal_length = 1200

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    processed_frame = detect_coins(frame.copy(), known_diameters, focal_length)

    cv2.imshow('Coin Detection Frame', processed_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
