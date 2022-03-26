import cv2

print("종료하려면 ESC")
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
print(capture.get(cv2.CAP_PROP_FPS))

fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter('output.mp4', fourcc, 15, (640, 480))


while cv2.waitKey(33) != 27:
    ret, frame = capture.read()
    cv2.imshow("VideoFrame", frame)
    out.write(frame)

