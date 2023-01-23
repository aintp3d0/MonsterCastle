import cv2
import numpy


def load_image_as_gray(image_path: str) -> numpy.ndarray:
  image = cv2.imread(image_path)
  return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)


def get_image_container(image_gray: numpy.ndarray) -> numpy.ndarray:
  # SEE: https://stackoverflow.com/a/58802719
  image_blur = cv2.blur(image_gray, (5, 5))

  minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(image_blur)
  ret, image_thresh = cv2.threshold(image_blur, 0.5 * maxVal, 255, cv2.THRESH_BINARY)

  cnts, _ = cv2.findContours(image_thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

  rcnt = None
  max_area = float('-inf')

  for cnt in cnts:
    area = cv2.contourArea(cnt)

    if area > max_area:
      max_area = area
      rcnt = cnt

  x, y, w, h = cv2.boundingRect(rcnt)
  # TODO: rewrite the background with zeros
  return image_gray[y:y+h, x:x+w]
