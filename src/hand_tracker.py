import cv2
import mediapipe as mp

from config import ONLY_RIGHT_HAND, RIGHT_HAND_LABEL


class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.75,
            min_tracking_confidence=0.75
        )

    def process_frame(self, frame):
        frame_h, frame_w, _ = frame.shape

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)

        if not results.multi_hand_landmarks:
            return None

        for hand_index, hand_landmarks in enumerate(results.multi_hand_landmarks):
            handedness = results.multi_handedness[hand_index]
            hand_label = handedness.classification[0].label
            hand_score = handedness.classification[0].score

            if ONLY_RIGHT_HAND and hand_label != RIGHT_HAND_LABEL:
                continue

            landmarks = self.get_landmark_positions(
                hand_landmarks,
                frame_w,
                frame_h
            )

            return {
                "landmarks": landmarks,
                "raw_landmarks": hand_landmarks,
                "frame_w": frame_w,
                "frame_h": frame_h,
                "hand_label": hand_label,
                "hand_score": hand_score
            }

        return None

    def get_landmark_positions(self, hand_landmarks, frame_w, frame_h):
        positions = {}

        for idx, lm in enumerate(hand_landmarks.landmark):
            x = int(lm.x * frame_w)
            y = int(lm.y * frame_h)
            positions[idx] = (x, y)

        return positions

    def draw_landmarks(self, frame, raw_landmarks):
        self.mp_draw.draw_landmarks(
            frame,
            raw_landmarks,
            self.mp_hands.HAND_CONNECTIONS
        )