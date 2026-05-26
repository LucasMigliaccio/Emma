import math


def distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])


def get_hand_box_ratio(landmarks, frame_w, frame_h):
    xs = [point[0] for point in landmarks.values()]
    ys = [point[1] for point in landmarks.values()]

    box_w = max(xs) - min(xs)
    box_h = max(ys) - min(ys)

    ratio_w = box_w / frame_w
    ratio_h = box_h / frame_h

    return max(ratio_w, ratio_h)