from cv2 import cv2
import mediapipe as mp

# https://google.github.io/mediapipe/solutions/hands.html


class FingerDetector:
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )

    def __prepare(self, image):
        """Prepare two lists of marks, one for each hand (left and right)
        if one of the hands (or both) is not detected the corresponding list in empty.
        Each list has 21 marks corresponding to 21  hand-knuckles.
        Each mark is represented by (x,y), being x and y
        normalized to [0.0, 1.0] by the image width and height respectively.
        The function returns also the image including the drawing of detected
        hand-knuckles and conecting lines"""
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        left_hand_landmarks = []
        right_hand_landmarks = []

        if results.multi_hand_landmarks:

            for hand_landmarks in results.multi_hand_landmarks:

                # Get hand index to check label (left or right)
                hand_index = results.multi_hand_landmarks.index(hand_landmarks)
                hand_label = (
                    results.multi_handedness[hand_index].classification[0].label
                )
                # Set variable to keep landmarks positions (x and y)
                if hand_label == "Left":
                    # Fill list with x and y positions of each landmark
                    for landmarks in hand_landmarks.landmark:
                        left_hand_landmarks.append([landmarks.x, landmarks.y])
                if hand_label == "Right":
                    # Fill list with x and y positions of each landmark
                    for landmarks in hand_landmarks.landmark:
                        right_hand_landmarks.append([landmarks.x, landmarks.y])
                # draw hand-knuckles and conecting lines in image
                self.mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style(),
                )

        return left_hand_landmarks, right_hand_landmarks, image

    # this is an example of difficult pattern detection
    # the difficult pattern is the OK gesture
    def __pose_d1(self, left_hand_landmarks, right_hand_landmarks):
        left_hand_landmarks = right_hand_landmarks
        if len(left_hand_landmarks) > 0:

            if (
                (left_hand_landmarks[18][1] > left_hand_landmarks[19][1])
                and (left_hand_landmarks[19][1] > left_hand_landmarks[20][1])
                and (left_hand_landmarks[14][1] > left_hand_landmarks[15][1])
                and (left_hand_landmarks[15][1] > left_hand_landmarks[16][1])
                and (left_hand_landmarks[10][1] > left_hand_landmarks[11][1])
                and (left_hand_landmarks[8][0] < left_hand_landmarks[5][0])
                and (left_hand_landmarks[6][1] < left_hand_landmarks[5][1])
                and (left_hand_landmarks[6][1] < left_hand_landmarks[7][1])
                and (left_hand_landmarks[7][1] < left_hand_landmarks[8][1])
                and (left_hand_landmarks[4][0] < left_hand_landmarks[3][0])
                and (left_hand_landmarks[4][1] < left_hand_landmarks[3][1])
                and (left_hand_landmarks[3][1] < left_hand_landmarks[2][1])
                and abs(left_hand_landmarks[8][1] - left_hand_landmarks[4][1]) < 0.05
                and abs(left_hand_landmarks[8][0] - left_hand_landmarks[4][0]) < 0.05
            ):

                return True
            else:
                return False
        else:
            return False

    def detect(self, image, level):
        left_hand_landmarks, right_hand_landmarks, img = self.__prepare(image)
        res = ""
        if level == "difficult":
            if self.__pose_d1(left_hand_landmarks, right_hand_landmarks):
                res = "Pose D11111"
            """elif self.__poseD2( left_hand_landmarks, right_hand_landmarks):
                res = 'Pose D22222'
            elif self.__poseD3( left_hand_landmarks, right_hand_landmarks):
                res = 'Pose D333333"""
            return res, img
        else:
            # returns the number of risen fingers
            # ATTENTION: WE DO NOT TAKE INTO ACCOUNT THE THUMB FINGER
            # Initially set finger count to 0 for each cap
            finger_count = 0
            if len(left_hand_landmarks) > 0:
                if (
                    left_hand_landmarks[8][1] < left_hand_landmarks[6][1]
                ):  # Index finger
                    finger_count = finger_count + 1
                if (
                    left_hand_landmarks[12][1] < left_hand_landmarks[10][1]
                ):  # Middle finger
                    finger_count = finger_count + 1
                if (
                    left_hand_landmarks[16][1] < left_hand_landmarks[14][1]
                ):  # Ring finger
                    finger_count = finger_count + 1
                if left_hand_landmarks[20][1] < left_hand_landmarks[18][1]:  # Pinky
                    finger_count = finger_count + 1

            if len(right_hand_landmarks) > 0:

                if (
                    right_hand_landmarks[8][1] < right_hand_landmarks[6][1]
                ):  # Index finger
                    finger_count = finger_count + 1
                if (
                    right_hand_landmarks[12][1] < right_hand_landmarks[10][1]
                ):  # Middle finger
                    finger_count = finger_count + 1
                if (
                    right_hand_landmarks[16][1] < right_hand_landmarks[14][1]
                ):  # Ring finger
                    finger_count = finger_count + 1
                if right_hand_landmarks[20][1] < right_hand_landmarks[18][1]:  # Pinky
                    finger_count = finger_count + 1

            return finger_count, img
