import cv2
import argparse
from pprint import pprint
import numpy as np
import time

from ml import Movenet
from ml import Posenet
import utils

def run(
    estimation_model: str, 
    input_type: str,
    input_data
    ):
    if estimation_model in ['movenet_lightning', 'movenet_thunder']:
        pose_detector = Movenet(estimation_model)
    elif estimation_model == 'posenet':
        pose_detector = Posenet(estimation_model)

    capture = None
    frame = None

    start_time = time.time()
    
    if input_type != "image":
        capture = cv2.VideoCapture(input_data)

    while cv2.waitKey(1) != 27:        # esc
        if capture != None:
            ret, frame = capture.read()
        else:
            frame = cv2.imread(input_data)
        list_persons = [pose_detector.detect(frame)]
        skeleton_pprint(list_persons)

        origin_frame = frame.copy()
        white_background = np.ones(frame.shape, dtype='uint8') * 255
        utils.visualize(frame, list_persons)
        utils.visualize(white_background, list_persons)
        
        time_gap = (time.time() - start_time)
        fps = 1 / time_gap
        start_time = time.time()

        fps_text = "FPS : " + str(int(fps))
        cv2.putText(img=origin_frame, text=fps_text, org=(10,10),
        fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1, color=(0,0,255), lineType=4)
        
        total_image = np.hstack([origin_frame, frame, white_background])
        cv2.imshow(f"{input_type}", total_image)
        
def skeleton_pprint(list_persons):
    persons = list_persons[0][0]
    
    for i in persons:
        print(i)
    print()


def main():
    print("종료하려면 ESC")
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_type", help = "input type ex) [webcam , video , image]", default="video")
    parser.add_argument("--input_data", help = "input data", default="test_data/test_video.mp4")
    parser.add_argument("--model", help = "choose the model ex) [movenet_lightning, movenet_thunder, posenet]", default="movenet_lightning")
    args = parser.parse_args()
    
    estimation_model = args.model
    input_type = args.input_type
    input_data = 0
    
    if input_type != "webcam":
        input_data = args.input_data
    
    run(estimation_model, input_type, input_data)


if __name__ == "__main__":
    main()
