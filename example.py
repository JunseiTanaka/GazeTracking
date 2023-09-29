"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import cv2
from gaze_tracking import GazeTracking
import pyautogui


gaze = GazeTracking()
webcam = cv2.VideoCapture(0)


def draw_meter(frame, ratio,center_x = 1100, center_y = 600):
    # メーターの中心座標
    

    # メーターの半径
    radius = 80

    # メーターの角度範囲
    start_angle = 0
    if ratio is not None:
        end_angle = int(ratio * 180)
    else:
        end_angle = 0    
    # メーターのバックグラウンドを描画
    cv2.rectangle(frame, (center_x-120, center_y-50), (center_x+100, center_y+100), (0, 0, 0), -1)
    # メーターの弧を描画
    cv2.ellipse(frame, (center_x, center_y), (radius, radius), 0, start_angle, end_angle, (0, 255, 0), -1)


while True:
    # We get a new frame from the webcam
    _, frame = webcam.read()
    frame = cv2.flip(frame, 1)

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""

    if gaze.is_blinking(5.0):
        text = "Blinking"
    elif gaze.is_right(0.5):
        text = "Looking right"
    elif gaze.is_left(0.65):
        text = "Looking left"
    elif gaze.is_center():
        text = "Looking center"

    
    screen_x, screen_y,  = pyautogui.size()

    gaze_horizontal_ratio = gaze.horizontal_ratio()
    gaze_vertical_ratio = gaze.vertical_ratio()

    # メーターを描画
    draw_meter(frame, gaze_horizontal_ratio)
    draw_meter(frame, gaze_vertical_ratio, 1100,400)

    if (gaze_horizontal_ratio is not None) and (gaze_vertical_ratio is not None):
        gaze_vertical_ratio = float(gaze_vertical_ratio) -0.4
        if gaze_vertical_ratio < 0:
            gaze_vertical_ratio = 0

        gaze_horizontal_ratio = gaze_horizontal_ratio - 0.15

        if gaze_horizontal_ratio > 0.55:
            gaze_horizontal_ratio = gaze_horizontal_ratio * 1.5
        elif gaze_horizontal_ratio < 0.45:
            gaze_horizontal_ratio = gaze_horizontal_ratio * 0.25

        if gaze_vertical_ratio > 0.55:
            gaze_vertical_ratio = gaze_vertical_ratio * 1.5
        elif gaze_vertical_ratio < 0.45:
            gaze_vertical_ratio = gaze_vertical_ratio * 0.25


        #cursor_x = screen_x * gaze_horizontal_ratio
        #cursor_y = screen_y * gaze_vertical_ratio

        #pyautogui.moveTo(cursor_x, cursor_y)    

        #print("v: ", gaze_vertical_ratio, "h: ",gaze_horizontal_ratio)
        


    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    #left_pupil = gaze.pupil_left_coords()
    #light_pupil = gaze.pupil_right_coords()
    #cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    #cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    cv2.namedWindow('Demo', cv2.WND_PROP_FULLSCREEN)
    #cv2.setWindowProperty('Demo', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    cv2.imshow("Demo", frame)

    if cv2.waitKey(1) == 27:
        break
   
webcam.release()
cv2.destroyAllWindows()
