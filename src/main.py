import cv2

from hand_tracker import HandTracker
from gestures import GestureDetector
from mouse_controller import MouseController
from config import CAMERA_INDEX


def main():
    cap = cv2.VideoCapture(CAMERA_INDEX)

    hand_tracker = HandTracker()
    gesture_detector = GestureDetector()
    mouse_controller = MouseController()

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        frame = cv2.flip(frame, 1)

        hand_data = hand_tracker.process_frame(frame)

        if hand_data:
            landmarks = hand_data["landmarks"]
            frame_w = hand_data["frame_w"]
            frame_h = hand_data["frame_h"]
            hand_label = hand_data["hand_label"]

            gesture = gesture_detector.detect(landmarks, frame_w, frame_h)

            mouse_controller.handle_gesture(
                gesture=gesture,
                landmarks=landmarks,
                frame_w=frame_w,
                frame_h=frame_h
            )

            cv2.putText(
                frame,
                f"Gesture: {gesture}",
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (255, 255, 255),
                2
            )

            cv2.putText(
                frame,
                f"Hand: {hand_label}",
                (30, 90),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2
            )

            hand_tracker.draw_landmarks(frame, hand_data["raw_landmarks"])

        cv2.imshow("Emma - Gesture Control", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    mouse_controller.release()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()