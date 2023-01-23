"""Getting the user credentials from image to login the user to the system

Credentials
  - Open ID (digits, validated)
  - Name (cropped image)
"""

import os
from typing import Optional, Tuple

import cv2
import numpy
import pytesseract

from .image_processing import load_image_as_gray, get_image_container


class UserCredentials:

  def __init__(self, image_path: str):
    self.image_path = image_path

  def get_username_and_openid(self) -> Tuple[numpy.ndarray, numpy.ndarray]:
    image_gray = load_image_as_gray(self.image_path)
    image_container = get_image_container(image_gray)

    ret, thresh1 = cv2.threshold(image_container, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

    cnts, _ = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    rcnts = []

    for cnt in cnts:
      area = cv2.contourArea(cnt)

      if (area < 1000):
        continue
      if (area > 30000):
        continue

      rcnts.append(cnt)

    image_y, image_x = image_container.shape
    image_half_half_y = image_y // 4
    image_half_x = image_x // 2

    open_id = None
    user_name = None

    for cnt in rcnts:
      rect = cv2.boundingRect(cnt)

      if (rect[0] > image_half_x):
        continue
      if (rect[1] > image_half_half_y):
        continue

      if user_name is None:
        user_name = rect
        continue
      if open_id is None:
        open_id = rect
        break

    x, y, w, h = user_name
    image_user_name = image_container[y:y+h, x:x+w]

    x, y, w, h = open_id
    image_open_id = image_container[y:y+h, x:x+w]

    return (image_user_name, image_open_id)

  def validate_image_openid(self, image_open_id: numpy.ndarray) -> Optional[str]:
    # SEE: https://stackoverflow.com/a/65242285
    # TODO
    # check if all *open_id has the same length of digits if so, remove *pytesseract
    text_open_id = pytesseract.image_to_string(image_open_id, config='--psm 7 digits')
    text_open_id = text_open_id.strip()
    return None if not text_open_id.isdigit() else text_open_id

  def save_credential_image(self, image_path: str, image: numpy.ndarray) -> None:
    cv2.imwrite(image_path, image)


def _test():
  from helper import show_image
  image_path = os.path.join('static', 'test.jpg')
  uc = UserCredentials(image_path)
  image_username, image_openid = uc.get_username_and_openid()
  show_image(image_username)
  show_image(image_openid)
  text_openid = uc.validate_image_openid(image_openid)
  print('OPEN_ID:', text_openid)
  uc.save_credential_image(os.path.join('static', 'openid') + '.jpg', image_openid)


if __name__ == '__main__':
  _test()
