import cv2
import argparse
import os
import numpy as np
import time

from ml import Movenet
from ml import Posenet
import post_process
from fitness_tracking import MadPT
import utils


def run(
        estimation_model: str,
        input_type: str,
        input_data,
        save_dir: str,
        save_result
):
    pose_detector = None
    capture = None
    frame = None
    save_index = 0
    check_point = time.time()
    hc = MadPT()

    if estimation_model in ['movenet_lightning', 'movenet_thunder']:
        pose_detector = Movenet(estimation_model)
    elif estimation_model == 'posenet':
        pose_detector = Posenet(estimation_model)

    if input_type != "image":
        capture = cv2.VideoCapture(input_data)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    image_list = []
    body_part_list = []

    while cv2.waitKey(1) != 27:  # esc
        # print(f'{save_index} frame')
        # read frame
        if capture != None:
            ret, frame = capture.read()
            # print(frame.shape)
            if not ret:
                break
        else:
            frame = cv2.imread(input_data)

        # inference
        list_persons = [pose_detector.detect(frame)]

        # calculate fps
        time_gap = (time.time() - check_point)
        fps = 1 / time_gap
        check_point = time.time()

        # make output image
        origin_frame = frame.copy()
        white_background = np.zeros(frame.shape, dtype='uint8')
        utils.visualize(frame, list_persons)
        utils.visualize(white_background, list_persons)
        fps_text = "FPS : " + str(int(fps))
        cv2.putText(img=origin_frame, text=fps_text, org=(10, 10),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1, color=(0, 0, 255), lineType=4)
        total_image = np.hstack([origin_frame, frame, white_background])

        # image save path
        image_list.append(total_image)
        body_part_list.append(list_persons)
        # skeleton_pprint(list_persons)
        cv2.imshow(f"{input_type}", total_image)
        save_index += 1

        # fitness_score = hc.push_up(list_persons)

    print("terminate!!")
    if save_result:
        post_process.main(save_dir, image_list, body_part_list)


def skeleton_pprint(list_persons):
    persons = list_persons[0][0]
    for i in persons:
        print(i)
    print()


def main():
    print("종료하려면 ESC")
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_type", help="input type ex) [webcam , video , image]", default="image")
    parser.add_argument("--input_data", help="input data", default='test_data/img2.png')
    parser.add_argument("--model", help="choose the model ex) [movenet_lightning, movenet_thunder, posenet]",
                        default="posenet")
    parser.add_argument("--save_result", help="input data", default="False")
    args = parser.parse_args()

    estimation_model = args.model
    input_type = args.input_type
    input_data = 0

    if input_type != "webcam":
        input_data = args.input_data

    if args.save_result == "True":
        save_result = True
    else:
        save_result = False

    save_dir = make_save_dir()

    run(estimation_model, input_type, input_data, save_dir, save_result)


def make_save_dir():
    tm = time.gmtime(time.time())
    save_dir = f'./data/{tm.tm_year}.{tm.tm_mon:02}.{tm.tm_mday:02}T{tm.tm_hour:02}:{tm.tm_min:02}:{tm.tm_sec:02}'
    if not os.path.exists(save_dir):
        image_path = os.path.join(save_dir, "image")
        plot_path = os.path.join(save_dir, "accu_plot")
        transition_path = os.path.join(save_dir, "body_part_transition")
        os.mkdir(save_dir)
        os.mkdir(image_path)
        os.mkdir(plot_path)
        os.mkdir(transition_path)
    return save_dir


if __name__ == "__main__":
    main()
