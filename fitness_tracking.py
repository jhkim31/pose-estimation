import math
from pprint import pprint

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


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class MadPT():
    def __init__(self):
        self.state = 0
        self.side = ""
        self.count = {
            "push_up": 0,
            "squat": 0,
            "lunge": 0,
            "shoulder_press": 0
        }
        self.score = {
            "push_up": [0, 0, 100, 100],
            "squat": [0, 100, 100],
            "lunge": [0, 100, 100],
            "shoulder_press": 0
        }

        self.init_size = {
            "right_leg": 1.0,
            "left_leg": 1.0
        }

        self.tmp = 0
        self.tmp2 = 0
        self.tmp3 = 0

    def push_up(self, list_person):

        score = list_person[0][2]
        body_parts = list_person[0][0]
        score_th = 0.5
        min_head_angle = 130
        max_head_angle = 160
        min_arm_angle = 90
        max_arm_angle = 120
        min_hip_angle = 130
        max_hip_angle = 160
        min_depth = 0
        max_depth = 100

        body_angle = self.calculate_angle(
            Point(body_parts[15].coordinate.x, 0),
            body_parts[15].coordinate,
            body_parts[5].coordinate
        )

        if score > score_th and body_angle > 45:
            left_arm_angle = self.calculate_angle(
                body_parts[5].coordinate,
                body_parts[7].coordinate,
                body_parts[9].coordinate
            )

            right_arm_angle = self.calculate_angle(
                body_parts[6].coordinate,
                body_parts[8].coordinate,
                body_parts[10].coordinate
            )

            left_hip_angle = self.calculate_angle(
                body_parts[5].coordinate,
                body_parts[11].coordinate,
                body_parts[13].coordinate
            )

            right_hip_angle = self.calculate_angle(
                body_parts[6].coordinate,
                body_parts[12].coordinate,
                body_parts[14].coordinate
            )

            hip_angle = (left_hip_angle + right_hip_angle) / 2

            left_head_angle = self.calculate_angle(
                body_parts[3].coordinate,
                body_parts[5].coordinate,
                body_parts[11].coordinate
            )

            right_head_angle = self.calculate_angle(
                body_parts[4].coordinate,
                body_parts[6].coordinate,
                body_parts[12].coordinate
            )
            head_angle = (left_head_angle + right_head_angle) / 2
            print(head_angle)

            depth = body_parts[7].coordinate.y - body_parts[5].coordinate.y
            arm_angle = (left_arm_angle + right_arm_angle) / 2

            if depth < min_depth:
                depth_score = 100
            elif depth < max_depth:
                depth_score = int((max_depth - depth) / (max_depth - min_depth) * 100)
            else:
                depth_score = 0

            if arm_angle < min_arm_angle:
                arm_score = 100
            elif arm_angle < max_arm_angle:
                arm_score = int((max_arm_angle - arm_angle) / (max_arm_angle - min_arm_angle) * 100)
            else:
                arm_score = 0

            if head_angle > max_head_angle:
                head_score = 100
            elif head_angle > min_head_angle:
                head_score = int((max_head_angle - head_angle) / (max_head_angle - min_head_angle) * 100)
            else:
                head_score = 0

            if hip_angle > max_hip_angle:
                hip_score = 100
            elif hip_angle > min_hip_angle:
                hip_score = int((max_hip_angle - hip_angle) / (max_hip_angle - min_hip_angle) * 100)
            else:
                hip_score = 0

            if self.score['push_up'][0] < depth_score:
                self.score['push_up'][0] = depth_score

            if self.score['push_up'][1] < arm_score:
                self.score['push_up'][1] = arm_score

            if self.score['push_up'][2] > hip_score:
                self.score['push_up'][2] = hip_score

            if self.score['push_up'][3] > head_score:
                self.score['push_up'][3] = head_score

            if arm_angle < 120 and self.state == 0:
                self.state = 1

            if arm_angle > 160 and self.state == 1:
                self.state = 0
                self.count["push_up"] += 1
                return_val = self.score['push_up']
                self.score["push_up"] = [0, 0, 100, 100]
                self.tmp = 0

                return return_val
            return 0

    def squat(self, list_person):
        score = list_person[0][2]
        body_parts = list_person[0][0]
        min_thigh_angle = 75  # 무릎 각도 (이거보다 작으면 최소점수)
        max_thigh_angle = 110  # 인식을 하는 최소 무릎 각도 (이거 이하부터 점수 계산)
        min_calf_angle = 20  # 지면에 수직인 벡터와 종아리 각도의 최소값 (즉 가장 적게 튀어나간)
        max_calf_angle = 35  # 지면에 수직인 벡터와 종아리 각도의 최대값 (이거보다 더 많이 튀어나가면 0)
        min_waist_angle = 40 # 지면에 수직인 벡터와 허리 각도의 최소값
        max_waist_angle = 60 # 지면에 수직인 벡터와 허리 각도의 최대값
        weighted_sum = [0.5, 0.35, 0.15]
        score_th = 0.5


        if score > score_th:

            left_thigh_angle = self.calculate_angle(
                body_parts[11].coordinate,
                body_parts[13].coordinate,
                body_parts[15].coordinate,
            )

            left_calf_angle = self.calculate_angle(
                Point(body_parts[15].coordinate.x, 0),
                body_parts[15].coordinate,
                body_parts[13].coordinate
            )

            left_waist_angle = self.calculate_angle(
                Point(body_parts[11].coordinate.x, 0),
                body_parts[11].coordinate,
                body_parts[5].coordinate
            )

            right_thigh_angle = self.calculate_angle(
                body_parts[12].coordinate,
                body_parts[14].coordinate,
                body_parts[16].coordinate,
            )

            right_calf_angle = self.calculate_angle(
                Point(body_parts[16].coordinate.x, 0),
                body_parts[16].coordinate,
                body_parts[14].coordinate
            )

            right_waist_angle = self.calculate_angle(
                Point(body_parts[12].coordinate.x, 0),
                body_parts[12].coordinate,
                body_parts[6].coordinate
            )

            thigh_angle = (left_thigh_angle + right_thigh_angle) / 2
            calf_angle = (left_calf_angle + right_calf_angle) / 2
            waist_angle = (left_waist_angle + right_waist_angle) / 2

            # 깊이를 측정하는 점수 (깊을수록 높음)
            if thigh_angle < min_thigh_angle:
                thigh_score = 100
            elif thigh_angle < max_thigh_angle:
                thigh_score = int((max_thigh_angle - thigh_angle) / (max_thigh_angle - min_thigh_angle) * 100)
            else:
                thigh_score = 0
            # 무릎의 튀어나감을 측정하는 점수 (안튀어나갈수록 높음)
            if calf_angle < min_calf_angle:
                calf_score = 100
            elif calf_angle < max_calf_angle:
                calf_score = int((max_calf_angle - calf_angle) / (max_calf_angle - min_calf_angle) * 100)
            else:
                calf_score = 0

            # 허리의 각도를 측정하는 점수 (세울수록 높음)
            if waist_angle < min_waist_angle:
                waist_score = 100
            elif waist_angle < max_waist_angle:
                waist_score = int((max_waist_angle - waist_angle) / (max_waist_angle - min_waist_angle) * 100)
            else:
                waist_score = 0

            if self.score['squat'][0] < thigh_score:
                self.score['squat'][0] = thigh_score

            if self.score['squat'][1] > calf_score:
                self.score['squat'][1] = calf_score

            if self.score['squat'][2] > waist_score:
                self.score['squat'][2] = waist_score

            if left_thigh_angle < max_thigh_angle and self.state == 0:
                self.state = 1

            if left_thigh_angle > 160 and self.state == 1:
                self.state = 0
                self.count["squat"] += 1
                return_val = self.score['squat']
                self.score["squat"] = [0, 100, 100]
                self.tmp = 0

                return return_val

        return 0

    def lunge(self, list_person):
        body_parts = list_person[0][0]
        if self.state == 0:
            if self.init_size['right_leg'] < self.calculate_length(body_parts[12].coordinate, body_parts[14].coordinate):
                self.init_size['right_leg'] = self.calculate_length(body_parts[12].coordinate, body_parts[14].coordinate)
            if self.init_size['left_leg'] < self.calculate_length(body_parts[11].coordinate, body_parts[13].coordinate):
                self.init_size['left_leg'] = self.calculate_length(body_parts[11].coordinate, body_parts[13].coordinate)

        min_down_rate = 0.3
        max_down_rate = 0.7
        min_angle = 5
        max_angle = 20
        right_leg = self.calculate_length(body_parts[12].coordinate, body_parts[14].coordinate)
        left_leg = self.calculate_length(body_parts[11].coordinate, body_parts[13].coordinate)
        right_angle = 0
        left_angle = 0

        if left_leg < self.init_size["left_leg"] * max_down_rate and self.state == 0:
            print("left down")
            self.state = 1
            self.side = "left"

        if right_leg < self.init_size["right_leg"] * max_down_rate and self.state == 1:
            print("right down")
            self.state = 1
            self.side = "right"

        print(self.init_size['left_leg'], self.init_size['right_leg'])
        print(left_leg, right_leg)
        down_rate = min(left_leg / self.init_size['left_leg'], right_leg, self.init_size['right_leg'])

        print(down_rate)
        if self.side == 'left':
            left_angle = self.calculate_angle(
                Point(body_parts[15].coordinate.x, 0),
                body_parts[15].coordinate,
                body_parts[13].coordinate
            )
            right_angle = self.calculate_angle(
                Point(body_parts[14].coordinate.x, 0),
                body_parts[14].coordinate,
                body_parts[12].coordinate
            )

        if self.side == 'right':
            left_angle = self.calculate_angle(
                Point(body_parts[13].coordinate.x, 0),
                body_parts[13].coordinate,
                body_parts[11].coordinate
            )
            right_angle = self.calculate_angle(
                Point(body_parts[16].coordinate.x, 0),
                body_parts[16].coordinate,
                body_parts[14].coordinate
            )

        if down_rate < min_down_rate:
            down_score = 100
        elif down_rate < max_down_rate:
            down_score = int((max_down_rate - down_rate) / (max_down_rate - min_down_rate) * 100)
        else:
            down_score = 0

        if right_angle < min_angle:
            right_score = 100
        elif right_angle < max_angle:
            right_score = int((max_angle - right_angle) / (max_angle - min_angle) * 100)
        else:
            right_score = 0

        if left_angle < min_angle:
            left_score = 100
        elif left_angle < max_angle:
            left_score = int((max_angle - left_angle) / (max_angle - min_angle) * 100)
        else:
            left_score = 0

        if self.score['lunge'][0] < down_score:
            self.score['lunge'][0] = down_score

        if self.score['lunge'][1] > right_score:
            self.score['lunge'][1] = right_score

        if self.score['lunge'][2] > left_score:
            self.score['lunge'][2] = left_score

        if down_rate > 0.8 and self.state == 1:
            self.state = 0
            return_val = self.score['lunge']
            self.score['lunge'] = [0, 100, 100]
            self.side = ""
            return return_val

        return 0

    def shoulder_press(self, list_person):
        body_parts = list_person[0][0]

        left_angle = self.calculate_angle(
            body_parts[5].coordinate,
            body_parts[7].coordinate,
            body_parts[9].coordinate
        )

        right_angle = self.calculate_angle(
            body_parts[6].coordinate,
            body_parts[8].coordinate,
            body_parts[10].coordinate
        )

        if left_angle < 95 and right_angle < 95 and self.state == 0:
            self.state = 1
            print("down")
        print(left_angle, right_angle)
        if left_angle > 150 and right_angle > 150 and self.state == 1:
            self.state = 0
            print("up")
            self.count["shoulder_press"] += 1

    def calculate_angle(self, p1, p2, p3):
        vector1 = (p1.x - p2.x, p1.y - p2.y)
        vector2 = (p3.x - p2.x, p3.y - p2.y)

        theta = math.acos(
            (vector1[0] * vector2[0] + vector1[1] * vector2[1]) /
            (math.sqrt(vector1[0] ** 2 + vector1[1] ** 2) * math.sqrt(vector2[0] ** 2 + vector2[1] ** 2) + 1e-5)
        )

        return theta * (180 / math.pi)

    def calculate_length(self, p1, p2):
        return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)
