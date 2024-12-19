# L ha : R ha : Command
# --------------------------
# ...| : |... : Draw
# |||| : ||.. : Pick new collor
# |... : .... : Clear window
# ..|| : |... : Drag
# .||| : |... : Zoom in
# .||| : ||.. : Zoom out

import cv2
from canvas import setup_fullscreen_window, CanvasDraw, CanvasDrawMenu, get_hand_info, draw_hand, get_index_tip, Paper, get_action, get_up_down

canvas = setup_fullscreen_window()

# Views
main = CanvasDraw(100, 100, 50, 50, canvas)
camera = CanvasDraw(18, 28, 90, 15, canvas)
menu = CanvasDrawMenu(50, 50, 50, 50, canvas)

paper = Paper()

action = 0

# Camera stream
cap = cv2.VideoCapture(0)

prev_point = None
while cap.isOpened():
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    hand_info = get_hand_info(frame)
    
    action = get_action(hand_info['left'])
    
    
    if action == 0:
        prev_point = None
    
    if action == 1:
        if (len(hand_info['right']) != 0):
            color = menu.get_color()
            point = get_index_tip(hand_info['right'])
            paper.draw_line(prev_point, point, color)
            prev_point = point
    
    # Darg
    if action == 3:
        if (len(hand_info['right']) != 0):
            point = get_index_tip(hand_info['right'])
            paper.move(prev_point, point)
            prev_point = point
    
    # zoom
    if action == 4:
        if (len(hand_info['right']) != 0):
            point = get_index_tip(hand_info['right'])
            tmp = get_up_down(hand_info['right'])
            paper.zoomf(point, tmp)
    
    if action == 5:
        paper.reset()
        
    
    canvas[:,:,:] = 255
    main.draw_image(paper.get_paper())
    draw_hand(hand_info['right'], main)
    
    if action == 2:
        menu.draw()
        draw_hand(hand_info['right'], menu)
        if len(hand_info['right']) != 0:
            tmp = get_up_down(hand_info['right'])
            if tmp[1] and tmp[2] and not tmp[3] and not tmp[4]:
                menu.update_color(get_index_tip(hand_info['right']))
    
    camera.draw_image(frame)
    draw_hand(hand_info['left'], camera)
    draw_hand(hand_info['right'], camera)
    
    cv2.imshow("Canvas with Camera Feed", canvas)
    

cap.release()
cv2.destroyAllWindows()
