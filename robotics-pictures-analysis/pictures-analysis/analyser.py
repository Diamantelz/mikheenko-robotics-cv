import cv2
import numpy as np
import os

# в этой функции реализуется вся необходимая обработка изображения
def mark_objects(image_path, output_dir):

    # чтение изображения
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Error: Could not read image at {image_path}")
        return

    # бинаризация изображения
    thresh = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    # заполнение возможных пробелов внутри объектов на картинке
    kernel = np.ones((3, 3), np.uint8)
    closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # нахождение контуров объектов
    contours, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # преобразование изображения в цветное
    img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    # проверка на наличие контуров
    if not contours:
        print("Error: No contours found in the image.")
        cv2.imshow("Result", img_color)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return

    # фильтрация маленьких контуров (шум)
    min_area = 50
    filtered_contours = [c for c in contours if cv2.contourArea(c) > min_area]

    # проверка на наличие контуров уже после фильтрации
    if not filtered_contours:
        print("Error: No contours found after filtering small contours.")
        cv2.imshow("Result", img_color)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return

    # рисование контуров и центров объектов
    for c in filtered_contours:
        cv2.drawContours(img_color, [c], -1, (0, 255, 0), 2)
        M = cv2.moments(c)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.circle(img_color, (cX, cY), 5, (0, 0, 255), -1)

    # нахождение самого большого и самого маленького контуров объектов
    largest_contour = max(filtered_contours, key=cv2.contourArea)
    smallest_contour = min(filtered_contours, key=cv2.contourArea)

    def draw_center(contour, color, label):
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.circle(img_color, (cX, cY), 7, color, -1)
            cv2.putText(img_color, label, (cX - 25, cY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # отдельно рисование контуров самого большого / маленького объектов
    draw_center(largest_contour, (0, 255, 255), "Largest")
    draw_center(smallest_contour, (255, 0, 255), "Smallest")

    # создание директории result и сохранение в нее обработанного изображения
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, os.path.basename(image_path))
    cv2.imwrite(output_path, img_color)
    print(f"Image saved to: {output_path}")

    # отображение результата и закрытие окон
    cv2.imshow("Result", img_color)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

output_directory = "/Users/diamantelz/PycharmProjects/robotics-pictures-analysis/images/result"

image_path = "/Users/diamantelz/PycharmProjects/robotics-pictures-analysis/images/source/balloons.jpg"
# image_path = "/Users/diamantelz/PycharmProjects/robotics-pictures-analysis/images/source/coins.jpg"
# image_path = "/Users/diamantelz/PycharmProjects/robotics-pictures-analysis/images/source/markers.jpg"

mark_objects(image_path, output_directory)