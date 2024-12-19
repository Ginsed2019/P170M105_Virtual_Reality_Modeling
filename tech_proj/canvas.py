import numpy as np
import cv2
import mediapipe as mp
import math

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

window_size = (1920, 1080)

thumb_landmarks = [1, 2, 3, 4]  # Thumb landmarks (knuckle to tip)
index_landmarks = [5, 6, 7, 8]  # Index finger landmarks
middle_landmarks = [9, 10, 11, 12]  # Middle finger landmarks
ring_landmarks = [13, 14, 15, 16]  # Ring finger landmarks
pinky_landmarks = [17, 18, 19, 20]  # Pinky finger landmarks

angle_tolerance = 10
angle_tolerance_zx = 50

class CanvasDraw:
    def __init__(self, width_pct, height_pct, center_x_pct, center_y_pct, canvas):
        self.canvas = canvas
        
        self.width_pct = width_pct / 100
        self.height_pct = height_pct / 100
        self.center_x_pct = center_x_pct / 100
        self.center_y_pct = center_y_pct / 100
        
        self.width_px = int(self.width_pct * window_size[0])
        self.height_px = int(self.height_pct * window_size[1])
        self.center_x_px = int(self.center_x_pct * window_size[0])
        self.center_y_px = int(self.center_y_pct  * window_size[1])
        
        self.corner_x_px = int(self.center_x_px - self.width_px / 2)
        self.corner_y_px = int(self.center_y_px - self.height_px / 2)
    
    def draw_image(self, image):
        image = cv2.resize(image, (self.width_px, self.height_px))
        self.canvas[self.corner_y_px:self.corner_y_px+self.height_px,self.corner_x_px:self.corner_x_px+self.width_px] = image

    def draw_circle(self, point_a):
        x, y, _ = point_a
        x = int(self.corner_x_px + x * self.width_px)
        y = int(self.corner_y_px + y * self.height_px)
        cv2.circle(self.canvas, (x, y), 5, (0, 255, 0), -1)
    
    def draw_line(self, point_a, point_b, color = None):
        x, y, _ = point_a
        x = int(self.corner_x_px + x * self.width_px)
        y = int(self.corner_y_px + y * self.height_px)
        x1, y1, _ = point_b
        x1 = int(self.corner_x_px + x1 * self.width_px)
        y1 = int(self.corner_y_px + y1 * self.height_px)
        if color is None:
            color = (255, 0, 0)
        cv2.line(self.canvas, (x, y), (x1, y1), color, 2)
    
    def get_absoulute(self, point_a):
        x, y = point_a
        x = int(self.corner_x_px + x * self.width_px)
        y = int(self.corner_y_px + y * self.height_px)
        return x, y
    
    
def draw_gradient_with_outline(image, x_start, y_start, x_end, y_end, band, value, rgb = None):
    """
    Draws a rectangle with a vertical red gradient and a black outline on the given image.

    Parameters:
        image (numpy.ndarray): The image to draw on.
        x_start (int): The starting x-coordinate of the rectangle.
        y_start (int): The starting y-coordinate of the rectangle.
        x_end (int): The ending x-coordinate of the rectangle.
        y_end (int): The ending y-coordinate of the rectangle.
    """
    # Create the red gradient
    gradient_height = y_end - y_start
    gradient_width = x_end - x_start
    gradient = np.zeros((gradient_height, gradient_width, 3), dtype=np.uint8)
    if rgb is None:
        for i in range(gradient_height):
            red_value = int((i / (gradient_height - 1)) * 255)  # Scale red from 0 to 255
            gradient[i, :, band] = red_value  # Set the red channel
            if abs(value - red_value) <= 3:
                gradient[i, :] = 255
    else:
        gradient[:, :, 0] = rgb[2]
        gradient[:, :, 1] = rgb[1]
        gradient[:, :, 2] = rgb[0]

    # Overlay the gradient onto the image
    image[y_start:y_end, x_start:x_end] = gradient

    # Add a black outline
    cv2.rectangle(image, (x_start, y_start), (x_end, y_end), (0, 0, 0), thickness=2)

class CanvasDrawMenu(CanvasDraw):
    def __init__(self, width_pct, height_pct, center_x_pct, center_y_pct, canvas):
        super().__init__(width_pct, height_pct, center_x_pct, center_y_pct, canvas)
        self.r_value = 100
        self.g_value = 200
        self.b_value = 245

    def draw(self):
        self.draw_image(np.ones((self.height_px, self.width_px, 3), dtype=np.uint8) * 245)
        
        x0, y0 = self.get_absoulute((0.3, 0.2)); x1, y1 = self.get_absoulute((0.4, 0.8));
        draw_gradient_with_outline(self.canvas, x0, y0, x1, y1, 2, self.r_value)
        x0, y0 = self.get_absoulute((0.45, 0.2)); x1, y1 = self.get_absoulute((0.55, 0.8));
        draw_gradient_with_outline(self.canvas, x0, y0, x1, y1, 1, self.g_value)
        x0, y0 = self.get_absoulute((0.6, 0.2)); x1, y1 = self.get_absoulute((0.7, 0.8));
        draw_gradient_with_outline(self.canvas, x0, y0, x1, y1, 0, self.b_value)
        
        x0, y0 = self.get_absoulute((0.85, 0.1)); x1, y1 = self.get_absoulute((0.95, 0.9));
        draw_gradient_with_outline(self.canvas, x0, y0, x1, y1, 2, None, (self.r_value, self.g_value, self.b_value))
        
    def update_color(self, point):
        x, y, z = point
        if 0.2 <= y and y <= 0.8:
            if 0.3 <= x and x <= 0.4:
                self.r_value = int((y - 0.2) / 0.6 * 255)
            if 0.45 <= x and x <= 0.55:
                self.g_value = int((y - 0.2) / 0.6 * 255)
            if 0.6 <= x and x <= 0.7:
                self.b_value = int((y - 0.2) / 0.6 * 255)
    
    def get_color(self):
        return (self.r_value, self.g_value, self.b_value)
                
        
    
    

class Paper:
    def __init__(self):
        
        self.zoom = 1
        
        self.width_px = window_size[0]
        self.height_px = window_size[1]
        
        self.max_zoom = 0.1
        self.max_width_px = int(self.width_px / self.max_zoom)
        self.max_height_px = int(self.height_px / self.max_zoom)
        
        self.canvas = np.ones((self.max_height_px, self.max_width_px, 3), dtype=np.uint8) * 255
        self.add_grid_lines(100)
        
        self.center_x_px = int(self.max_width_px / 2)
        self.center_y_px = int(self.max_height_px / 2)
        
        self.corner_x_px = int(self.center_x_px - self.width_px / 2)
        self.corner_y_px = int(self.center_y_px - self.height_px / 2)
        
    def add_grid_lines(self, spacing_px):
        # Add horizontal lines
        for y in range(0, self.max_height_px, spacing_px):
            self.canvas[y, :, :] = 0

        # Add vertical lines
        for x in range(0, self.max_width_px, spacing_px):
            self.canvas[:, x, :] = 0
        
    def get_absoulute(self, point):
        x, y = point
        x = int(self.corner_x_px + x * self.width_px)
        y = int(self.corner_y_px + y * self.height_px)
        return x, y
        
    def draw_line(self, point_a, point_b, color):
        if point_a is None: point_a = point_b
        x, y, _ = point_a
        x, y = self.get_absoulute((x, y))
        x1, y1, _ = point_b
        x1, y1 = self.get_absoulute((x1, y1))
        
        r,g,b = color
        cv2.line(self.canvas, (x, y), (x1, y1), (b, g, r), 5)
    
    def get_paper(self):
        x0, y0 = self.get_absoulute((0, 0))
        x1, y1 = self.get_absoulute((1, 1))
        return self.canvas[y0:y1,x0:x1,:]

    # FIXME: What to do when out of baunds
    def move(self, point_a, point_b):
        if point_a is None: point_a = point_b
        
        x, y, _ = point_a
        x1, y1, _ = point_b
        
        dx = x-x1
        dy = y-y1
        
        dx = int(dx * self.width_px)
        dy = int(dy * self.height_px)
        
        self.center_x_px = self.center_x_px + dx
        self.center_y_px = self.center_y_px + dy
        
        self.corner_x_px = self.corner_x_px + dx
        self.corner_y_px = self.corner_y_px + dy
    
    def zoomf(self, point, up_down):
        inn = up_down[1] and not up_down[2] and not up_down[3] and not up_down[4]
        out = up_down[1] and up_down[2] and not up_down[3] and not up_down[4]
        if (not inn) and (not out): return None
        
        factor = 1.005 if inn else 1 / 1.005
        x, y, _ = point  # User-specified zoom center
        x, y = self.get_absoulute((x, y))  # Convert to absolute coordinates
    
    
        # Create and apply the zoom matrix
        z_mat = create_zoom_matrix((x, y), factor)
        tmp = apply_transformation(
            z_mat,
            np.array([
                [self.center_x_px, self.center_y_px],  # Center of viewport
                [self.corner_x_px, self.corner_y_px]  # Top-left corner
            ])
        )
    
        # Update center and corner
        self.center_x_px, self.center_y_px = int(tmp[0][0]), int(tmp[0][1])
        self.corner_x_px, self.corner_y_px = int(tmp[1][0]), int(tmp[1][1])
    
        # Adjust width and height to scale properly
        self.width_px = int(self.width_px / factor)
        self.height_px = int(self.height_px / factor)
    
        # Recalculate corner position to keep the center fixed
        self.corner_x_px = self.center_x_px - self.width_px // 2
        self.corner_y_px = self.center_y_px - self.height_px // 2
    
    
    def reset(self):
        self.zoom = 1
        
        self.width_px = window_size[0]
        self.height_px = window_size[1]
        
        self.center_x_px = int(self.max_width_px / 2)
        self.center_y_px = int(self.max_height_px / 2)
        
        self.corner_x_px = int(self.center_x_px - self.width_px / 2)
        self.corner_y_px = int(self.center_y_px - self.height_px / 2)
        
        self.canvas[:,:,:] = 255
        self.add_grid_lines(100)

def create_zoom_matrix(zoom_center, zoom_factor):
    x_c, y_c = zoom_center  # Explicitly [x, y]

    T_to_origin = np.array([
        [1, 0, -x_c],
        [0, 1, -y_c],
        [0, 0, 1]
    ])
    S = np.array([
        [zoom_factor, 0, 0],
        [0, zoom_factor, 0],
        [0, 0, 1]
    ])
    T_back = np.array([
        [1, 0, x_c],
        [0, 1, y_c],
        [0, 0, 1]
    ])
    return T_back @ S @ T_to_origin

def apply_transformation(matrix, points):
    # Ensure points are treated as [x, y]
    homogeneous_points = np.hstack([points, np.ones((points.shape[0], 1))])
    transformed_points = homogeneous_points @ matrix.T
    return transformed_points[:, :2]  # Return as [x, y]


def h_draw_finger(draw_line, joints):
    draw_line(joints[0], joints[1])
    draw_line(joints[1], joints[2])
    draw_line(joints[2], joints[3])

def draw_hand(joints, canvas_draw):
    if len(joints) == 0: return None
    for joint in joints:
        canvas_draw.draw_circle(joint)
    h_draw_finger(canvas_draw.draw_line, joints[thumb_landmarks])
    h_draw_finger(canvas_draw.draw_line, joints[index_landmarks])
    h_draw_finger(canvas_draw.draw_line, joints[middle_landmarks])
    h_draw_finger(canvas_draw.draw_line, joints[ring_landmarks])
    h_draw_finger(canvas_draw.draw_line, joints[pinky_landmarks])
    # Palm
    canvas_draw.draw_line(joints[thumb_landmarks][0], joints[index_landmarks][0])
    canvas_draw.draw_line(joints[index_landmarks][0], joints[middle_landmarks][0])
    canvas_draw.draw_line(joints[middle_landmarks][0], joints[ring_landmarks][0])
    canvas_draw.draw_line(joints[ring_landmarks][0], joints[pinky_landmarks][0])
    canvas_draw.draw_line(joints[pinky_landmarks][0], joints[0])
    canvas_draw.draw_line(joints[0], joints[thumb_landmarks][0])
    
    


def setup_fullscreen_window():
    cv2.namedWindow("Canvas with Camera Feed", cv2.WINDOW_NORMAL)
    cv2.moveWindow("Canvas with Camera Feed", 1920, 0)
    cv2.setWindowProperty("Canvas with Camera Feed", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    canvas = np.ones((window_size[1], window_size[0], 3), dtype=np.uint8) * 255
    return canvas

def get_hand_info(image):
    rgb_frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    results = hands.process(rgb_frame)
    
    hand_info = {'left': [], 'right': []}

    if results.multi_handedness and results.multi_hand_landmarks:
        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            # Get hand label ('Left' or 'Right')
            hand_label = results.multi_handedness[idx].classification[0].label.lower()

            # Collect joint positions (x, y, z) for the hand
            joints = [(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark]
            
            # Append to the respective hand in the dictionary
            if hand_label in hand_info:
                hand_info[hand_label] = joints
    
    hand_info['left'] = np.array(hand_info['left'])
    hand_info['right'] = np.array(hand_info['right'])
    return hand_info

def get_index_tip(joints):
    return joints[index_landmarks][3]


# Finger angles
# -----------------------------------------------------------------------------
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

def angles_same(joints):
    yx01, zx01, yz01 = calculate_angle(joints[0], joints[1])
    yx12, zx12, yz12 = calculate_angle(joints[1], joints[2])
    yx23, zx23, yz23 = calculate_angle(joints[2], joints[3])
    
    yx012 = angle_difference(yx01, yx12)
    yx123 = angle_difference(yx12, yx23)
    
    zx012 = angle_difference(zx01, zx12)
    zx123 = angle_difference(zx12, zx23)
    
    yz012 = angle_difference(yz01, yz12)
    yz123 = angle_difference(yz12, yz23)
    
    yx = (yx012 <= angle_tolerance) and (yx123 <= angle_tolerance)
    zx = (zx012 <= angle_tolerance_zx) and (zx123 <= angle_tolerance_zx)
    yz = (yz012 <= angle_tolerance_zx) and (yz123 <= angle_tolerance_zx)
    
    return yx and zx and yz

def get_up_down(joints):
    thumb = angles_same(joints[thumb_landmarks])
    index = angles_same(joints[index_landmarks])
    middle = angles_same(joints[middle_landmarks])
    ring = angles_same(joints[ring_landmarks])
    pinky = angles_same(joints[pinky_landmarks])
    return [thumb, index, middle, ring, pinky]

def get_action(joints):
    if len(joints) == 0: return 0
    arr = get_up_down(joints)
    if arr[1] and not arr[2] and not arr[3] and not arr[4]: return 1 # Draw
    if arr[1] and arr[2] and arr[3] and arr[4]: return 2 # Change Collor
    if arr[1] and arr[2] and not arr[3] and not arr[4]: return 3 # Drag
    if arr[1] and arr[2] and arr[3] and not arr[4]: return 4 # Zoom
    if not arr[1] and not arr[2] and not arr[3] and arr[4]: return 5 # Clean
    return 0
