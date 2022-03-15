import cv2

print("종료하려면 ESC")
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
while cv2.waitKey(33) != 27:
    ret, frame = capture.read()
    cv2.imshow("VideoFrame", frame)
            
