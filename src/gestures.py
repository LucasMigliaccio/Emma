
from config import MAX_HAND_BOX_RATIO
from utils import distance, get_hand_box_ratio


#DETECTAR DEDOS, INDENTIFICAR GESTO
class GestureDetector:
    def detect(self, landmarks, frame_w, frame_h):
        hand_ratio = get_hand_box_ratio(landmarks, frame_w, frame_h)

        if hand_ratio > MAX_HAND_BOX_RATIO:
            return "TOO_CLOSE"

        fingers = self.detect_fingers(landmarks)

        thumb, index, middle, ring, pinky = fingers
        total_fingers = fingers.count(True)

        if self.is_side_scissors(landmarks):
            return "OPEN_SOFTBARBER"

        if total_fingers == 5:
            return "PAUSE"

        if total_fingers == 0:
            return "SAFE_MODE"

        if index and not middle and not ring and not pinky:
            return "MOVE_CURSOR"

        if index and middle and not ring and not pinky:
            index_tip = landmarks[8]
            middle_tip = landmarks[12]

            if distance(index_tip, middle_tip) < 45:
                return "LEFT_CLICK"

            return "SCROLL"

        if index and not middle and not ring and pinky:
            return "RIGHT_CLICK"

        if thumb and index and not middle and not ring and not pinky:
            return "DRAG"

        if index and middle and ring and not pinky:
            return "ALT_TAB"

        return "UNKNOWN"

    def detect_fingers(self, lm):
        fingers = []

        # Pulgar mano derecha con cámara espejada.
        # Si queda invertido, cambiar < por >.
        thumb_up = lm[4][0] < lm[3][0]
        fingers.append(thumb_up)

        fingers.append(lm[8][1] < lm[6][1])
        fingers.append(lm[12][1] < lm[10][1])
        fingers.append(lm[16][1] < lm[14][1])
        fingers.append(lm[20][1] < lm[18][1])

        return fingers

    def is_side_scissors(self, lm):
        index_mcp = lm[5]
        index_tip = lm[8]

        middle_mcp = lm[9]
        middle_tip = lm[12]

        ring_tip = lm[16]
        ring_pip = lm[14]

        pinky_tip = lm[20]
        pinky_pip = lm[18]

        index_horizontal = abs(index_tip[0] - index_mcp[0]) > 55
        middle_horizontal = abs(middle_tip[0] - middle_mcp[0]) > 55

        index_not_vertical = abs(index_tip[1] - index_mcp[1]) < 80
        middle_not_vertical = abs(middle_tip[1] - middle_mcp[1]) < 80

        fingers_separated = distance(index_tip, middle_tip) > 35

        ring_folded = ring_tip[1] > ring_pip[1] - 10
        pinky_folded = pinky_tip[1] > pinky_pip[1] - 10

        return (
            index_horizontal and
            middle_horizontal and
            index_not_vertical and
            middle_not_vertical and
            fingers_separated and
            ring_folded and
            pinky_folded
        )