import numpy as np

from modules.vision.m455 import find_element


def detect_buttons(image: np.ndarray) -> list[dict]:
    return find_element(image, "button")


def detect_icons(image: np.ndarray) -> list[dict]:
    return find_element(image, "icon")


def detect_text_fields(image: np.ndarray) -> list[dict]:
    return find_element(image, "text")


def detect_all_ui_elements(image: np.ndarray) -> list[dict]:
    return find_element(image, "")
