from mediapipe.python.solutions.hands import HAND_CONNECTIONS
import cv2
import math
import numpy as np

angle_tolerance = 10

def draw_hand(h, w, hand_landmarks, canvas):
    for landmark in hand_landmarks.landmark:
        x, y = int(landmark.x * w), int(landmark.y * h)
        cv2.circle(canvas, (x, y), 5, (0, 255, 0), -1)

    for connection in HAND_CONNECTIONS:
        start = hand_landmarks.landmark[connection[0]]
        end = hand_landmarks.landmark[connection[1]]
        
        start_x, start_y = int(start.x * w), int(start.y * h)
        end_x, end_y = int(end.x * w), int(end.y * h)
        
        cv2.line(canvas, (start_x, start_y), (end_x, end_y), (255, 0, 0), 2)

def calculate_angle(point1, point2):
    x1, y1, z1 = point1
    x2, y2, z2 = point2
    
    angle = math.degrees(math.atan2(y1 - y2, x1 - x2))
    yx = (360 + 180 - angle) % 360
    
    angle = math.degrees(math.atan2(y1 - y2, z1 - z2))
    yz = (360 + 180 - angle) % 360
    
    angle = math.degrees(math.atan2(z1 - z2, x1 - x2))
    zx = (360 + 180 - angle) % 360
    
    return yx, zx, yz

def angle_difference(a0, a1):
    diff = abs(a0 - a1)
    return min(diff, 360 - diff)

def angles_same(landmarks, finger):
    a00, a01, a02 = calculate_angle(landmarks[finger[0]], landmarks[finger[1]])
    a10, a11, a12 = calculate_angle(landmarks[finger[1]], landmarks[finger[2]])
    a20, a21, a22 = calculate_angle(landmarks[finger[2]], landmarks[finger[3]])
    
    a001 = angle_difference(a00, a01)
    a012 = angle_difference(a01, a02)
    
    a101 = angle_difference(a10, a11)
    a112 = angle_difference(a11, a12)
    
    a201 = angle_difference(a20, a21)
    a212 = angle_difference(a21, a22)
    
    z0 = (a001 <= angle_tolerance) and (a012 <= angle_tolerance)
    z1 = (a101 <= angle_tolerance) and (a112 <= angle_tolerance)
    z2 = (a201 <= angle_tolerance) and (a212 <= angle_tolerance)
    
    return z0 and z1 and z2

def get_up_down(hand_landmarks):
    thumb_landmarks = [1, 2, 3, 4]  # Thumb landmarks (knuckle to tip)
    index_landmarks = [5, 6, 7, 8]  # Index finger landmarks
    middle_landmarks = [9, 10, 11, 12]  # Middle finger landmarks
    ring_landmarks = [13, 14, 15, 16]  # Ring finger landmarks
    pinky_landmarks = [17, 18, 19, 20]  # Pinky finger landmarks
    
    thumb = angles_same(hand_landmarks.landmark, thumb_landmarks)
    index = angles_same(hand_landmarks.landmark, index_landmarks)
    middle = angles_same(hand_landmarks.landmark, middle_landmarks)
    ring = angles_same(hand_landmarks.landmark, ring_landmarks)
    pinky = angles_same(hand_landmarks.landmark, pinky_landmarks)
    return [thumb, index, middle, ring, pinky]

def get_action(hand_landmarks):
    arr = get_up_down(hand_landmarks)
    if arr[1] and not arr[2] and not arr[3] and not arr[4]: return 1 # Draw
    if arr[1] and arr[2] and arr[3] and arr[4]: return 2 # Change Collor
    if arr[1] and arr[2] and not arr[3] and not arr[4]: return 3 # Drag
    if arr[1] and arr[2] and arr[3] and not arr[4]: return 4 # Zoom
    return 0


    
