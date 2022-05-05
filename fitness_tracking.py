import math
from pprint import pprint
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

class MadPT():
    def __init__(self):
        self.state = 0
        self.side = ""
        self.count = {
            "push_up": 0,
            "squat": 0,
            "lunge": 0,
            "shoulder_press" : 0
        }
        self.max_score = {
            "push_up": 0,
            "squat": [0,0,0],
            "lunge": 0,
            "shoulder_press": 0
        }

        self.init_size = {
            "right_leg" : 210,
            "left_leg" : 210
        }

        self.tmp = 0
        self.tmp2 = 0
        self.tmp3 = 0
    def push_up(self, list_person):
        body_parts = list_person[0][0]

        side = "left" if (body_parts[5].score + body_parts[7].score + body_parts[9].score) > \
                         (body_parts[6].score + body_parts[8].score + body_parts[10].score) else "right"
        
        #condition check
        observe_point = (5,7,9) if side == "left" else (6,8,10)
        if body_parts[observe_point[0]].score + body_parts[observe_point[1]].score + body_parts[observe_point[2]].score > 1:
            angle = self.calculate_angle(
                body_parts[observe_point[0]].coordinate,
                body_parts[observe_point[1]].coordinate,
                body_parts[observe_point[2]].coordinate
            )

            if angle < 110 and self.state == 0:
                self.state = 1
                print("down")

            if angle > 160 and self.state == 1:
                self.state = 0
                print("up")
                self.count["push_up"] += 1
                print(self.count["push_up"])
                
                if self.max_score["push_up"] < 10:
                    print("bad")
                    
                elif self.max_score["push_up"] < 20:
                    print("good")
                elif self.max_score["push_up"] < 30:
                    print("great")
                else:
                    print("excellent!!")
                self.max_score["push_up"] = 0

            if angle < 110:
                if self.max_score["push_up"] < angle - 80:
                    self.max_score["push_up"] = angle - 80

        return self.max_score["push_up"]

    def squat(self, list_person):
        score = list_person[0][2]
        min_thigh_angle = 75        # 무릎 각도 (이거보다 작으면 최소점수)
        max_thigh_angle = 110       # 인식을 하는 최소 무릎 각도 (이거 이하부터 점수 계산)
        min_calf_angle = 20         # 지면에 수직인 벡터와 종아리의 각도의 최소값 (즉 가장 적게 튀어나간)
        max_calf_angle = 35         # 지면에 수직인 벡터와 종아리의 각도의 최대값 (이거보다 더 많이 튀어나가면 0)
        min_waist_angle = 5
        max_waist_angle = 30
        body_parts = list_person[0][0]
        side = "left" if (body_parts[11].score + body_parts[13].score + body_parts[15].score) > \
                         (body_parts[12].score + body_parts[14].score + body_parts[16].score) else "right"

        observe_point = (11, 13, 15, 5) if side == "left" else (12, 14, 16, 6)
        class P():
            def __init__(self, x, y):
                self.x = x
                self.y = y

        if body_parts[observe_point[0]].score + \
                body_parts[observe_point[1]].score + \
                body_parts[observe_point[2]].score > 1.5:

            thigh_angle = self.calculate_angle(
                body_parts[observe_point[0]].coordinate,
                body_parts[observe_point[1]].coordinate,
                body_parts[observe_point[2]].coordinate,
            )

            calf_angle = self.calculate_angle(
                P(body_parts[observe_point[2]].coordinate.x, 0),
                body_parts[observe_point[2]].coordinate,
                body_parts[observe_point[1]].coordinate
            )

            waist_angle = self.calculate_angle(
                P(body_parts[observe_point[0]].coordinate.x, 0),
                body_parts[observe_point[0]].coordinate,
                body_parts[observe_point[3]].coordinate
            )
            print(waist_angle)

            if thigh_angle < min_thigh_angle:
                thigh_score = 1
            elif thigh_angle < max_thigh_angle:
                thigh_score = (max_thigh_angle - thigh_angle) / (max_thigh_angle - min_thigh_angle)
            else:
                thigh_score = 0

            if calf_angle < min_calf_angle:
                calf_score = 1
            elif calf_angle < max_calf_angle:
                calf_score = (max_calf_angle - calf_angle) / (max_calf_angle - min_calf_angle)
            else:
                calf_score = 0

            # print("thigh_angle : ", thigh_angle)
            # print("calf_angle : ", calf_angle)
            # print("thigh_score : ", thigh_score)
            # print("calf_score : ", calf_score)
            # print()

            if self.max_score['squat'][0] < thigh_score:
                self.max_score['squat'][0] = thigh_score
                self.max_score['squat'][1] = calf_score


            if thigh_angle < max_thigh_angle and self.state == 0:
                self.state = 1
                print("down")

            if thigh_angle > 160 and self.state == 1:
                self.state = 0
                print("up")
                self.count["squat"] += 1
                return_val = self.max_score['squat']
                # print(self.count["squat"])
                # if self.max_score["squat"] < 10:
                #     print("bad", self.max_score["squat"], self.tmp)
                # elif self.max_score["squat"] < 20:
                #     print("good", self.max_score["squat"], self.tmp)
                # elif self.max_score["squat"] < 30:
                #     print("great", self.max_score["squat"], self.tmp)
                # else:
                #     print("excellent", self.max_score["squat"], self.tmp)
                #
                self.max_score["squat"] = [0,0,0]
                self.tmp = 0

                return return_val

        return 0

    def lunge(self, list_person):
        body_parts = list_person[0][0]

        right_leg = self.calculate_length(body_parts[12].coordinate, body_parts[14].coordinate)
        left_leg = self.calculate_length(body_parts[11].coordinate, body_parts[13].coordinate)

        if left_leg < self.init_size["left_leg"] * 0.5:
            self.side = "left"
            if self.state == 0:
                print("left down")
                self.state = 1

        if right_leg < self.init_size["right_leg"] * 0.5:
            self.side = "right"
            if self.state == 0:
                print("right down")
                self.state = 1

        if self.side == "left" and self.state == 1:
            if left_leg > self.init_size["left_leg"] * 0.9:
                self.state = 0
                print("left up")
                self.side = ""

        if self.side == "right" and self.state == 1:
            if right_leg > self.init_size["right_leg"] * 0.9:
                self.state = 0
                print("right up")
                self.side = ""

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