import cv2
import pytesseract
from PIL import Image
import matplotlib.pyplot as plt
# import numpy as np
font_scale = 10
font = cv2.FONT_HERSHEY_PLAIN

pytesseract.pytesseract.tesseract_cmd = "tesseract"


def imageDetection():
    image = cv2.imread('demo.png')
    # text = pytesseract.image_to_string(Image.fromarray(image))

    image2char = pytesseract.image_to_string(image)
    print(image2char)

    image2boxes = pytesseract.image_to_boxes(image)
    print(image2boxes)

    imgH, imgW, _ = image.shape
    for boxes in image2boxes.splitlines():
        # S 220 1248 321 1398 0 -> sample string
        boxes = boxes.split(' ')
        x, y, w, h = int(boxes[1]), int(boxes[2]), int(boxes[3]), int(boxes[4])
        # cv2.rectangle(imageRef, width, height, color, scale)
        cv2.rectangle(image, (x, imgH-y), (w, imgH-h), (0, 0, 255), 3)

    plt.imshow(image)


def videoDetection():
    cap = cv2.VideoCapture(0)  # loads webcam
    # cap = cv2.VideoCapture("demo-video.mp4")

    if not cap.isOpened():
        cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("Cannot open video")

    cntr = 0
    while True:
        ret, frame = cap.read()
        cntr = cntr + 1
        # read every 20 frames of video
        if ((cntr % 20) == 0):
            imgH, imgW, _ = frame.shape
            x1, y1, w1, h1 = 0, 0, imgH, imgW

            imgchar = pytesseract.image_to_string(frame)
            imgboxes = pytesseract.image_to_boxes(frame)
            for boxes in imgboxes.splitlines():
                boxes = boxes.split(' ')
                x, y, w, h = int(boxes[1]), int(
                    boxes[2]), int(boxes[3]), int(boxes[4])
                cv2.rectangle(frame, (x, imgH-y), (w, imgH-h), (0, 0, 255), 3)

            cv2.putText(frame, imgchar, (x1 + int(w1/50), y1 + int(h1/50)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            font = cv2.FONT_HERSHEY_SIMPLEX

            cv2.imshow('Text Detection', frame)

            if cv2.waitKey(2) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()


videoDetection()
