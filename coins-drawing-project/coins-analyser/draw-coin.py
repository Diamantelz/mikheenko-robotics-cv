import cv2
import numpy as np
import serial
import time

def detect_coins(frame, focal_length):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.bilateralFilter(gray, 9, 75, 75)
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    kernel = np.ones((5, 5), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    total_coin_count = 0

    for contour in contours:
        if cv2.contourArea(contour) > 100:
            ellipse = cv2.fitEllipse(contour)
            (x, y), (major_axis, minor_axis), angle = ellipse

            pixel_diameter = (major_axis + minor_axis) / 2
            if 10 < (focal_length * 25) / pixel_diameter /10 < 30:
                cv2.ellipse(frame, ellipse, (0, 255, 0), 2)
                total_coin_count += 1

    return frame, total_coin_count

focal_length = 1200
cap = cv2.VideoCapture(0)
drawing_in_progress = False
last_total_count = None

ser = serial.Serial('/dev/cu.usbmodem1201', 115200, timeout=1)

file_paths = {
    1: "/Users/diamantelz/Desktop/coins/drawing-coin-1-edited.gcode",
    2: "/Users/diamantelz/Desktop/coins/drawing-coin-2-edited.gcode",
    3: "/Users/diamantelz/Desktop/coins/drawing-coin-3-edited.gcode",
    4: "/Users/diamantelz/Desktop/coins/drawing-coin-add-edited.gcode",
}

def send_gcode(file_path):
    try:
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                print(line)
                ser.write(line.encode() + b'\n')
                time.sleep(1)
                try:
                    response = ser.readline().decode().strip()
                    print(f"Ответ Arduino: {response}")
                    if "Invalid coordinate format" in response:
                        print("Ошибка координат от Arduino!")
                except:
                    print("Нет ответа от Arduino (таймаут)")
        return True
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
        return False
    except Exception as e:
        print(f"Ошибка: {e}")
        return False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    processed_frame, total_coin_count = detect_coins(frame.copy(), focal_length)

    if not drawing_in_progress:
        if last_total_count is None or last_total_count != total_coin_count:
            print(f"Общее количество монет: {total_coin_count}")
            last_total_count = total_coin_count
            if total_coin_count in file_paths:
                file_path = file_paths[total_coin_count]
                drawing_in_progress = True
                if send_gcode(file_path):
                    coins_drawn = total_coin_count
                drawing_in_progress = False

    cv2.imshow('Coin Detection Frame', processed_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

ser.close()
cap.release()
cv2.destroyAllWindows()