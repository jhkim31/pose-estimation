import matplotlib.pyplot as plt
import os
from jh_pbar import jh_pbar
import cv2

from data import BodyPart

'''
KeyPoint(body_part=<BodyPart.NOSE: 0>, coordinate=Point(x=657, y=380), score=0.5295743)
KeyPoint(body_part=<BodyPart.LEFT_EYE: 1>, coordinate=Point(x=717, y=306), score=0.71167743)
KeyPoint(body_part=<BodyPart.RIGHT_EYE: 2>, coordinate=Point(x=590, y=308), score=0.60980856)
KeyPoint(body_part=<BodyPart.LEFT_EAR: 3>, coordinate=Point(x=773, y=335), score=0.4879389)
KeyPoint(body_part=<BodyPart.RIGHT_EAR: 4>, coordinate=Point(x=481, y=348), score=0.6443689)
KeyPoint(body_part=<BodyPart.LEFT_SHOULDER: 5>, coordinate=Point(x=901, y=541), score=0.6466513)
KeyPoint(body_part=<BodyPart.RIGHT_SHOULDER: 6>, coordinate=Point(x=374, y=555), score=0.61255854)
KeyPoint(body_part=<BodyPart.LEFT_ELBOW: 7>, coordinate=Point(x=990, y=704), score=0.25749794)
KeyPoint(body_part=<BodyPart.RIGHT_ELBOW: 8>, coordinate=Point(x=252, y=716), score=0.27520007)
KeyPoint(body_part=<BodyPart.LEFT_WRIST: 9>, coordinate=Point(x=1001, y=670), score=0.14146397)
KeyPoint(body_part=<BodyPart.RIGHT_WRIST: 10>, coordinate=Point(x=377, y=684), score=0.07703042)
KeyPoint(body_part=<BodyPart.LEFT_HIP: 11>, coordinate=Point(x=732, y=772), score=0.32744354)
KeyPoint(body_part=<BodyPart.RIGHT_HIP: 12>, coordinate=Point(x=428, y=731), score=0.36347598)
KeyPoint(body_part=<BodyPart.LEFT_KNEE: 13>, coordinate=Point(x=973, y=701), score=0.16954657)
KeyPoint(body_part=<BodyPart.RIGHT_KNEE: 14>, coordinate=Point(x=285, y=700), score=0.20464075)
KeyPoint(body_part=<BodyPart.LEFT_ANKLE: 15>, coordinate=Point(x=579, y=701), score=0.018676013)
KeyPoint(body_part=<BodyPart.RIGHT_ANKLE: 16>, coordinate=Point(x=562, y=690), score=0.035004675)
'''
plot_x_data = ["nose", "L_eye", "L_ear", "L_shoulder", "L_elbow", "L_wrist", "L_hip", "L_knee", "L_ankle",
               "R_eye",  "R_ear",  "R_shoulder",  "R_elbow", "R_wrist", "R_hip", "R_knee", "R_ankle"]

left_data = [BodyPart.NOSE, BodyPart.LEFT_EAR, BodyPart.LEFT_EYE, BodyPart.LEFT_HIP, BodyPart.LEFT_ELBOW, BodyPart.LEFT_KNEE, BodyPart.LEFT_ANKLE, BodyPart.LEFT_SHOULDER, BodyPart.LEFT_WRIST]
def make_plot(list_persons, save_dir, index):
    persons = list_persons[0][0]
    plot_data = []

    for idx, i in enumerate(persons):
        if i.body_part in left_data:
            plot_data.append(i.score)
    for idx, i in enumerate(persons[1:]):
        if i.body_part not in left_data:
            plot_data.append(i.score)

    
    fig = plt.figure(figsize=(20,6))
    ax1 = fig.add_subplot()
    ax1.bar(x=plot_x_data, height=plot_data)
    ax1.set_xlabel("body part")
    ax1.set_ylabel("accuracy")
    ax1.grid(True, axis='y')

    save_path = os.path.join(save_dir, "accu_plot", f'{index}.png')
    plt.savefig(save_path)
    plt.close(fig)

def body_part_position_transition(save_dir, body_part_position):
    for idx, i in enumerate(body_part_position):
        save_path = os.path.join(save_dir, "body_part_transition", f"{plot_x_data[idx]}.png")
        plt.clf()
        x_position = []
        y_position = []
        fig = plt.figure(figsize=(16, 8))
        ax = fig.add_subplot()
        ax.set_ylim([0, 1280])
        for j in i:
            x_position.append(j.x)
            y_position.append(j.y)
        ax.plot(x_position, label = "x coordinate")
        ax.plot(y_position, label = "y coordinate")

        ax.set_xlabel("frame")
        ax.set_ylabel("coordinate")
        ax.legend()
        print(save_path)
        plt.savefig(save_path)
        plt.close(fig)

def main(save_dir, image_list, body_part_list):
    length = len(image_list)
    tmp = []
    body_part_position = [[] for _ in range(17)]

    pbar = jh_pbar(steps=length, size=30, prefix='후처리 중입니다(프레임별 사진)...', color=1)
    for idx, (image, body_part) in enumerate(zip(image_list, body_part_list)):
        image_save_path = os.path.join(save_dir, "image", f'{idx}_image.png')
        cv2.imwrite(image_save_path, image)
        make_plot(body_part, save_dir, idx)
        pbar.update(postfix=f'[{idx + 1} / {length}]')

    for idx, person in enumerate(body_part_list):
        for index, body_part in enumerate(person[0].keypoints):
            body_part_position[index].append(body_part.coordinate)

    body_part_position_transition(save_dir, body_part_position)

