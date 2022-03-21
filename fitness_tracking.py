import math

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


class HealthCoach():
    def __init__(self):
        self.state = 0
        self.count = {
            "push_up": 0,
            "squat": 0
        }
        self.max_score = {
            "push_up": 0,
            "squat": 0
        }

    def push_up(self, list_person):
        body_parts = list_person[0][0]

        if body_parts[5].score > 0.5:
            left_arm_angle = self.calculate_angle(
                body_parts[5].coordinate,
                body_parts[7].coordinate,
                body_parts[9].coordinate
            )

            if left_arm_angle < 110 and self.state == 0:
                self.state = 1
                print("down")

            if left_arm_angle > 160 and self.state == 1:
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

            if left_arm_angle < 110:
                if self.max_score["push_up"] < 110 - left_arm_angle:
                    self.max_score["push_up"] = 110 - left_arm_angle

    def calculate_angle(self, p1, p2, p3):
        vector1 = (p1.x - p2.x, p1.y - p2.y)
        vector2 = (p3.x - p2.x, p3.y - p2.y)

        theta = math.acos((vector1[0] * vector2[0] + vector1[1] * vector2[1]) / (
                math.sqrt(vector1[0] ** 2 + vector1[1] ** 2) * math.sqrt(vector2[0] ** 2 + vector2[1] ** 2) + 1e-5
        ))

        return theta * (180 / math.pi)
