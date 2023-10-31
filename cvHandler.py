import cv2
import pytesseract
from PIL import Image
import matplotlib.pyplot as plt


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
    toReturn = ""
    cap = cv2.VideoCapture(0)  # loads webcam
    # cap = cv2.VideoCapture("./assets/demo-video.mp4")

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
            toReturn = imgchar
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
    return toReturn


def captureImageAndExtractText():
    cap = cv2.VideoCapture(0)  # Load the webcam

    if not cap.isOpened():
        # Try the default camera if the webcam is not available
        cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("Cannot open camera")

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Failed to capture a frame.")
            break

        # Extract text from the captured frame
        extracted_text = pytesseract.image_to_string(frame)
        imgH, imgW, _ = frame.shape

        # Get the word boxes
        imgboxes = pytesseract.image_to_boxes(frame)

        # Draw red rectangles around detected words
        for boxes in imgboxes.splitlines():
            boxes = boxes.split(' ')
            x, y, w, h = int(boxes[1]), int(
                boxes[2]), int(boxes[3]), int(boxes[4])
            cv2.rectangle(frame, (x, imgH - y), (w, imgH - h), (0, 0, 255), 3)

        # Display a preview of the extracted text
        cv2.putText(frame, "Recognized Text:", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(frame, extracted_text, (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Display the live video feed with red rectangles and text
        cv2.imshow('Live Video Feed', frame)

        # Press 'q' to capture an image and exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # Save the captured frame as an image
            cv2.imwrite('captured_image.png', frame)
            break

    cap.release()
    cv2.destroyAllWindows()

    # Return the extracted text
    return extracted_text


def captureImageAndExtractTextSimple():
    cap = cv2.VideoCapture(0)  # Load the webcam

    if not cap.isOpened():
        # Try the default camera if the webcam is not available
        cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("Cannot open camera")

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Failed to capture a frame.")
            break

        # Display the live video feed
        cv2.imshow('Live Video Feed', frame)

        # Press 'q' to capture an image and exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # Save the captured frame as an image
            cv2.imwrite('captured_image.png', frame)
            break

    cap.release()
    cv2.destroyAllWindows()

    # Now, use Pytesseract to extract text from the captured image
    captured_image = cv2.imread('captured_image.png')
    extracted_text = pytesseract.image_to_string(captured_image)

    return extracted_text

# captureImageAndExtractText()
