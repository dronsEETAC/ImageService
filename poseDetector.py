from cv2 import cv2
import mediapipe as mp

# https://google.github.io/mediapipe/solutions/pose


class PoseDetector:
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=True,
            model_complexity=2,
            enable_segmentation=True,
            min_detection_confidence=0.5,
        )

    def __prepare(self, image):
        """Prepare a list with the marks of 33 pose landmarks
        if no pose is detected the list in empty.
        Each mark is represented by (x,y), being x and y
        normalized to [0.0, 1.0] by the image width and height respectively.
        The function returns also the image including the drawing of detected
        pose landmarks and conecting lines"""

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image)
        image.flags.writeable = True

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        self.mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            self.mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style(),
        )
        pose_landmarks = []
        if results.pose_landmarks:
            for landmark in results.pose_landmarks.landmark:
                pose_landmarks.append([landmark.x, landmark.y])
        return pose_landmarks, image

    # these are 3 examples of difficult patterns

    def __p1(self, pose_landmarks):

        if (
            (pose_landmarks[24][0] > pose_landmarks[26][0])
            and (pose_landmarks[26][0] < pose_landmarks[28][0])
            and (pose_landmarks[28][1] < pose_landmarks[25][1])
            and (pose_landmarks[12][1] < pose_landmarks[14][1])
            and (pose_landmarks[14][1] < pose_landmarks[16][1])
            and (pose_landmarks[11][1] < pose_landmarks[13][1])
            and (pose_landmarks[13][1] < pose_landmarks[15][1])
        ):
            return True
        else:
            return False

    def __p2(self, pose_landmarks):

        if (
            (pose_landmarks[23][0] < pose_landmarks[25][0])
            and (pose_landmarks[25][0] > pose_landmarks[27][0])
            and (pose_landmarks[27][1] < pose_landmarks[26][1])
            and (pose_landmarks[12][1] < pose_landmarks[14][1])
            and (pose_landmarks[14][1] < pose_landmarks[16][1])
            and (pose_landmarks[11][1] < pose_landmarks[13][1])
            and (pose_landmarks[13][1] < pose_landmarks[15][1])
        ):
            return True
        else:
            return False

    # este
    def __p3(self, pose_landmarks):

        if (
            (pose_landmarks[11][0] < pose_landmarks[13][0])
            and (pose_landmarks[13][0] < pose_landmarks[15][0])
            and (pose_landmarks[11][1] > pose_landmarks[13][1])
            and (pose_landmarks[13][1] > pose_landmarks[15][1])
            and (pose_landmarks[25][0] > pose_landmarks[23][0])
            and (pose_landmarks[27][0] > pose_landmarks[25][0])
            and (pose_landmarks[25][0] > pose_landmarks[13][0])
            and (pose_landmarks[27][1] < pose_landmarks[28][1])
        ):

            return True
        else:
            return False

    # oeste
    def __p4(self, pose_landmarks):

        if (
            (pose_landmarks[12][0] > pose_landmarks[14][0])
            and (pose_landmarks[14][0] > pose_landmarks[16][0])
            and (pose_landmarks[12][1] > pose_landmarks[14][1])
            and (pose_landmarks[14][1] > pose_landmarks[16][1])
            and (pose_landmarks[26][0] < pose_landmarks[24][0])
            and (pose_landmarks[28][0] < pose_landmarks[26][0])
            and (pose_landmarks[26][0] < pose_landmarks[14][0])
            and (pose_landmarks[28][1] < pose_landmarks[27][1])
        ):

            return True
        else:
            return False

    # drop
    def __p5(self, pose_landmarks):

        if (
            (pose_landmarks[23][0] < pose_landmarks[25][0])
            and (pose_landmarks[25][0] > pose_landmarks[27][0])
            and (pose_landmarks[26][0] > pose_landmarks[24][0])
            and (pose_landmarks[26][0] > pose_landmarks[28][0])
        ):

            return True
        else:
            return False

    # return
    def __p6(self, pose_landmarks):

        if (
            (pose_landmarks[24][0] > pose_landmarks[26][0])
            and (pose_landmarks[26][0] < pose_landmarks[28][0])
            and (pose_landmarks[28][1] < pose_landmarks[25][1])
            and (pose_landmarks[12][1] > pose_landmarks[14][1])
            and (pose_landmarks[14][1] > pose_landmarks[16][1])
            and (pose_landmarks[14][0] < pose_landmarks[12][0])
            and (pose_landmarks[14][0] < pose_landmarks[16][0])
            and (pose_landmarks[11][1] > pose_landmarks[13][1])
            and (pose_landmarks[13][1] > pose_landmarks[15][1])
            and (pose_landmarks[13][0] > pose_landmarks[11][0])
            and (pose_landmarks[13][0] > pose_landmarks[15][0])
        ):
            return True
        else:
            return False

    # stop
    def __p0(self, pose_landmarks):

        if (
            (pose_landmarks[26][0] < pose_landmarks[24][0])
            and (pose_landmarks[26][0] < pose_landmarks[30][0])
            and (pose_landmarks[25][0] > pose_landmarks[23][0])
            and (pose_landmarks[25][0] > pose_landmarks[29][0])
        ):

            return True
        else:
            return False

    def __pose_d3(self, pose_landmarks):
        if (
            (pose_landmarks[16][0] > pose_landmarks[12][0])
            and (pose_landmarks[12][0] > pose_landmarks[14][0])
            and (pose_landmarks[16][1] < pose_landmarks[14][1])
            and (pose_landmarks[14][1] < pose_landmarks[12][1])
            and (pose_landmarks[15][0] < pose_landmarks[11][0])
            and (pose_landmarks[11][0] < pose_landmarks[13][0])
            and (pose_landmarks[15][1] < pose_landmarks[13][1])
            and (pose_landmarks[13][1] < pose_landmarks[11][1])
            and (pose_landmarks[15][0] > pose_landmarks[16][0])
            and (pose_landmarks[23][0] > pose_landmarks[25][0])
            and (pose_landmarks[25][0] > pose_landmarks[27][0])
            and (pose_landmarks[26][0] < pose_landmarks[24][0])
            and (pose_landmarks[24][0] < pose_landmarks[28][0])
            and (pose_landmarks[28][1] < pose_landmarks[25][1])
        ):
            return True
        else:
            return False

    def __pose_d2(self, pose_landmarks):
        if (
            (pose_landmarks[16][0] > pose_landmarks[12][0])
            and (pose_landmarks[12][0] > pose_landmarks[14][0])
            and (pose_landmarks[16][1] < pose_landmarks[14][1])
            and (pose_landmarks[14][1] < pose_landmarks[12][1])
            and (pose_landmarks[15][0] < pose_landmarks[11][0])
            and (pose_landmarks[11][0] < pose_landmarks[13][0])
            and (pose_landmarks[15][1] < pose_landmarks[13][1])
            and (pose_landmarks[13][1] < pose_landmarks[11][1])
            and (pose_landmarks[15][0] < pose_landmarks[16][0])
            and (pose_landmarks[23][0] < pose_landmarks[25][0])
            and (pose_landmarks[27][0] < pose_landmarks[25][0])
            and (pose_landmarks[26][0] < pose_landmarks[28][0])
            and (pose_landmarks[26][0] < pose_landmarks[24][0])
        ):
            return True
        else:
            return False

    def __pose_d1(self, pose_landmarks):
        if (
            (pose_landmarks[16][0] < pose_landmarks[14][0])
            and (pose_landmarks[14][0] < pose_landmarks[12][0])
            and (pose_landmarks[16][1] < pose_landmarks[14][1])
            and (pose_landmarks[14][1] < pose_landmarks[12][1])
            and (pose_landmarks[11][0] < pose_landmarks[13][0])
            and (pose_landmarks[13][0] < pose_landmarks[15][0])
            and (pose_landmarks[15][1] < pose_landmarks[13][1])
            and (pose_landmarks[13][1] < pose_landmarks[11][1])
            and (pose_landmarks[12][0] < pose_landmarks[11][0])
            and (pose_landmarks[24][1] < pose_landmarks[26][1])
            and (pose_landmarks[26][1] < pose_landmarks[28][1])
            and (pose_landmarks[28][0] < pose_landmarks[26][0])
            and (pose_landmarks[26][0] < pose_landmarks[24][0])
            and (pose_landmarks[23][0] < pose_landmarks[25][0])
            and (pose_landmarks[25][0] > pose_landmarks[27][0])
            and (pose_landmarks[23][1] < pose_landmarks[25][1])
            and (pose_landmarks[25][1] < pose_landmarks[27][1])
            and (pose_landmarks[24][0] < pose_landmarks[23][0])
        ):
            return True
        else:
            return False

    def detect(self, image, level):
        pose_landmarks, img = self.__prepare(image)
        res = ""
        if len(pose_landmarks) > 17:
            if level == "difficult":
                if self.__p0(pose_landmarks):
                    res = 0
                elif self.__p1(pose_landmarks):
                    res = 1
                elif self.__p2(pose_landmarks):
                    res = 2
                elif self.__p3(pose_landmarks):
                    res = 3
                elif self.__p4(pose_landmarks):
                    res = 4
                elif self.__p5(pose_landmarks):
                    res = 5
                elif self.__p6(pose_landmarks):
                    res = 6
            else:
                # to see what are the easy patterns see picture assets_needed/poses_faciles.png
                if (
                    (pose_landmarks[12][1] < pose_landmarks[14][1])
                    and (pose_landmarks[14][1] < pose_landmarks[16][1])
                    and (pose_landmarks[11][1] < pose_landmarks[13][1])
                    and (pose_landmarks[13][1] < pose_landmarks[15][1])
                    and (pose_landmarks[18][0] < pose_landmarks[17][0])
                ):
                    res = 0  # STOP
                elif (
                    (pose_landmarks[12][1] < pose_landmarks[14][1])
                    and (pose_landmarks[14][1] < pose_landmarks[16][1])
                    and (pose_landmarks[11][1] < pose_landmarks[13][1])
                    and (pose_landmarks[13][1] < pose_landmarks[15][1])
                    and (pose_landmarks[18][0] > pose_landmarks[17][0])
                ):
                    res = 5  # DROP
                elif (
                    (pose_landmarks[14][1] > pose_landmarks[12][1])
                    and (pose_landmarks[14][1] > pose_landmarks[16][1])
                    and (pose_landmarks[13][1] > pose_landmarks[11][1])
                    and (pose_landmarks[13][1] > pose_landmarks[15][1])
                    and (pose_landmarks[18][0] < pose_landmarks[17][0])
                ):
                    res = 6  # RETURN

                elif (pose_landmarks[12][1] < pose_landmarks[14][1]) and (
                    pose_landmarks[11][1] > pose_landmarks[13][1]
                ):
                    res = 3  # EAST
                elif (pose_landmarks[12][1] > pose_landmarks[14][1]) and (
                    pose_landmarks[11][1] < pose_landmarks[13][1]
                ):
                    res = 4  # WEST
                elif (pose_landmarks[12][1] > pose_landmarks[14][1]) and (
                    pose_landmarks[11][1] > pose_landmarks[13][1]
                ):
                    if pose_landmarks[18][0] > pose_landmarks[17][0]:
                        res = 2  # SOUTH
                    if pose_landmarks[18][0] < pose_landmarks[17][0]:
                        res = 1  # NORTH

        return res, img
