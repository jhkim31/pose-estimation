import matplotlib.pyplot as plt
import numpy as np
import os
from jh_pbar import jh_pbar
import cv2
plot_x_data = ["nose", "L_eye", "R_eye", "L_ear", "R_ear", "L_shoulder", "R_shoulder", "L_elbow", "R_elbow",
                   "L_wrist", "R_wrist", "L_hip", "R_hip", "L_knee", "R_knee", "L_ankle", "R_ankle"]

def make_plot(list_persons, save_dir, index):
    persons = list_persons[0][0]
    plot_data = []
    for idx, i in enumerate(persons):
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

