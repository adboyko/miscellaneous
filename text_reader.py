import numpy as np
import cv2
import pytesseract


def main():
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract'
    cam_feed = cv2.VideoCapture(0)

    while True:
        ret, cam_frame = cam_feed.read()
        out_frame = cv2.cvtColor(cam_frame, cv2.COLOR_BGR2GRAY)
        out_frame = out_frame[100:250, 100:300]
        ret, thresh = cv2.threshold(out_frame, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
        out_kern = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
        dilate = cv2.dilate(thresh, out_kern, iterations=1)
        cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        assumed_text = pytesseract.image_to_string(out_frame)
        if assumed_text:
            print(assumed_text)
        cv2.rectangle(cam_frame, (100, 100), (300, 250),
                      color=(0, 255, 0), thickness=5, lineType=cv2.LINE_4)
        cv2.putText(cam_frame, assumed_text, (100, 350),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow("camera", cam_frame)
        if cv2.waitKey(2) == ord('q'):
            break
    cam_feed.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
