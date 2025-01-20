import cv2
import numpy as np


def process_video():
    cap = cv2.VideoCapture(0)

    def on_mouse(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            param[0] = (x, y)

    flood_point = [None]
    cv2.namedWindow('Mask')
    cv2.setMouseCallback('Mask', on_mouse, flood_point)


    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        blurred = cv2.GaussianBlur(frame, (5, 5), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        lower_purple = np.array([20, 5, 20])
        upper_purple = np.array([150, 150, 140])

        mask = cv2.inRange(hsv, lower_purple, upper_purple)

        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=5)

        mask_floodfill = mask.copy()
        if flood_point[0]:
            h, w = mask.shape[:2]
            seed_point = flood_point[0]
            cv2.floodFill(mask_floodfill, None, seed_point, 255)
            mask_floodfill_inv = cv2.bitwise_not(mask_floodfill)
            mask = mask | mask_floodfill_inv

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        min_area = 100
        contours = [c for c in contours if cv2.contourArea(c) > min_area]

        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            cv2.drawContours(frame, [largest_contour], -1, (0, 255, 0), 2)
            M = cv2.moments(largest_contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv2.circle(frame, (cX, cY), 5, (255, 0, 0), -1)
                cv2.putText(frame, f"Center: ({cX}, {cY})", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.imshow('Mask', mask)
        cv2.imshow('Processed Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    process_video()