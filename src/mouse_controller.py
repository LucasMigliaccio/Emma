import time
import os
import subprocess

import numpy as np
import pyautogui

from config import (
    FRAME_REDUCTION,
    SMOOTHENING,
    ACTION_DELAY,
    ALT_TAB_DELAY,
    SOFTBARBER_EXE_PATH,
    SOFTBARBER_OPEN_DELAY
)

#CONTROLADORES DE ACCION
class MouseController:
    def __init__(self):
        pyautogui.FAILSAFE = False

        self.screen_w, self.screen_h = pyautogui.size()

        self.prev_x = 0
        self.prev_y = 0

        self.last_action_time = 0
        self.last_alt_tab_time = 0
        self.last_softbarber_open_time = 0

        self.dragging = False
        self.last_scroll_y = None

    def handle_gesture(self, gesture, landmarks, frame_w, frame_h):
        if gesture in ["PAUSE", "SAFE_MODE", "UNKNOWN", "TOO_CLOSE"]:
            self.release()
            return

        if gesture == "MOVE_CURSOR":
            self.release_drag()
            self.last_scroll_y = None
            self.move_mouse(landmarks[8], frame_w, frame_h)
            return

        if gesture == "LEFT_CLICK":
            self.release_drag()
            self.last_scroll_y = None

            if self.can_do_action(ACTION_DELAY):
                pyautogui.click(button="left")

            return

        if gesture == "RIGHT_CLICK":
            self.release_drag()
            self.last_scroll_y = None

            if self.can_do_action(ACTION_DELAY):
                pyautogui.click(button="right")

            return

        if gesture == "SCROLL":
            self.release_drag()
            self.scroll(landmarks)
            return

        if gesture == "DRAG":
            self.last_scroll_y = None
            self.drag(landmarks[8])
            return

        if gesture == "ALT_TAB":
            self.release_drag()
            self.last_scroll_y = None
            self.alt_tab()
            return

        if gesture == "OPEN_SOFTBARBER":
            self.release_drag()
            self.last_scroll_y = None
            self.open_softbarber()
            return

    def move_mouse(self, index_tip, frame_w, frame_h):
        x, y = index_tip

        screen_x = np.interp(
            x,
            (FRAME_REDUCTION, frame_w - FRAME_REDUCTION),
            (0, self.screen_w)
        )

        screen_y = np.interp(
            y,
            (FRAME_REDUCTION, frame_h - FRAME_REDUCTION),
            (0, self.screen_h)
        )

        current_x = self.prev_x + (screen_x - self.prev_x) / SMOOTHENING
        current_y = self.prev_y + (screen_y - self.prev_y) / SMOOTHENING

        pyautogui.moveTo(current_x, current_y)

        self.prev_x = current_x
        self.prev_y = current_y

    def scroll(self, landmarks):
        index_tip = landmarks[8]
        middle_tip = landmarks[12]

        current_y = int((index_tip[1] + middle_tip[1]) / 2)

        if self.last_scroll_y is not None:
            diff = self.last_scroll_y - current_y

            if abs(diff) > 8:
                pyautogui.scroll(int(diff / 2))

        self.last_scroll_y = current_y

    def drag(self, index_tip):
        if not self.dragging:
            pyautogui.mouseDown(button="left")
            self.dragging = True

        pyautogui.moveTo(index_tip[0], index_tip[1])

    def alt_tab(self):
        now = time.time()

        if now - self.last_alt_tab_time > ALT_TAB_DELAY:
            pyautogui.hotkey("alt", "tab")
            self.last_alt_tab_time = now

    def open_softbarber(self):
        now = time.time()

        if now - self.last_softbarber_open_time < SOFTBARBER_OPEN_DELAY:
            return

        if not os.path.exists(SOFTBARBER_EXE_PATH):
            print("No se encontro SoftBarber.exe")
            return

        subprocess.Popen([SOFTBARBER_EXE_PATH], shell=False)
        self.last_softbarber_open_time = now

    def can_do_action(self, delay):
        now = time.time()

        if now - self.last_action_time > delay:
            self.last_action_time = now
            return True

        return False

    def release_drag(self):
        if self.dragging:
            pyautogui.mouseUp(button="left")
            self.dragging = False

    def release(self):
        self.release_drag()
        self.last_scroll_y = None