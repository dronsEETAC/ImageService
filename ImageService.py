import json

import paho.mqtt.client as mqtt

import cv2 as cv2
import numpy as np


import base64
import time
import threading

from fingerDetector import FingerDetector
from poseDetector import PoseDetector
from faceDetector import FaceDetector
from speechDetector import SpeechDetector


def __set_direction(code):
    if code == 1:
        return "Norte"
    elif code == 2:
        return "Sur"
    elif code == 3:
        return "Este"
    elif code == 4:
        return "Oeste"
    elif code == 5:
        return "Drop"
    elif code == 6:
        return "Retorna"
    elif code == 0:
        return "Stop"
    else:
        return ""

def on_message(cli, userdata, message):

    global client
    global mode
    global selected_level
    global level
    global detector
    global prevCode
    global cont
    global code_sent
    global video_on
    global clientAutopilot
    global returning

    splited = message.topic.split("/")
    origin = splited[0]
    command = splited[2]
    print(message.topic)

    if command == 'Connect':
        print('connected')
        client.subscribe('+/imageService/parameters')

    if command == 'parameters':
        parameters = json.loads(message.payload.decode("utf-8"))
        mode = parameters['mode']
        level = parameters['level']
        selected_level = parameters['selected_level']
        if mode == "fingers":
            detector = FingerDetector()
        elif mode == "pose":
            detector = PoseDetector()
        elif mode == "voice":
            detector = SpeechDetector()
        else:
            detector = FaceDetector()
        video_on = True
        client.subscribe('+/imageService/videoFramePractice')
        client.subscribe('+/imageService/videoFrameFlying')

    if command == 'stopVideoStream':

        prevCode = -1
        cont = 0
        code_sent = False
        video_on = False

    if command == 'videoFramePractice':
        # Decoding the message
        image = base64.b64decode(message.payload)
        # converting into numpy array from buffer
        npimg = np.frombuffer(image, dtype=np.uint8)
        # Decode to Original Frame
        frame = cv2.imdecode(npimg, 1)

        if (video_on):

            # when the user changes the pattern (new face, new pose or new fingers) the system
            # waits some time (ignore 8 video frames) for the user to stabilize the new pattern
            # we need the following variables to control this
            #
            # if mode == "voice":
            #     self.map.putText("Di algo ...")
            if mode != "voice":

                img = cv2.resize(frame, (800, 600))
                img = cv2.flip(img, 1)
                code, img2 = detector.detect(img, level)
                x = threading.Thread(target=send_video_detected(img2))
                x.start()
                # if user changed the pattern we will ignore the next 8 video frames
                print("code: ", code, "prev code: ", prevCode, "code_sent: ", code_sent)
                if code != prevCode:
                    cont = 4
                    prevCode = code
                    code_sent = False
                else:
                    cont = cont - 1
                    if cont < 0:
                        # the first 8 video frames of the new pattern (to be ignored) are done
                        # we can start showing new results
                        if not code_sent:
                            direction = __set_direction(int(code))
                            client.publish('imageService/droneCircus/direction', direction)

            # else:
            #     code, voice = self.detector.detect(self.level)
            #     if code != -1:
            #         self.direction = self.__set_direction(code)
            #     self.map.putText(voice)

    if command == "videoFrameFlying":

        # Decoding the message
        image = base64.b64decode(message.payload)
        # converting into numpy array from buffer
        npimg = np.frombuffer(image, dtype=np.uint8)
        # Decode to Original Frame
        frame = cv2.imdecode(npimg, 1)

        if not returning:
            code, img = detector.detect(frame, level)
            img = cv2.resize(img, (800, 600))
            img2 = cv2.flip(img, 1)
            x2 = threading.Thread(target=send_video_detected(img2))
            x2.start()
            print("code: ", code, "prev code: ", prevCode, "code_sent: ", code_sent)
            if code != prevCode:
                cont = 4
                prevCode = code
                code_sent = False
            else:
                cont = cont - 1
                if cont < 0:
                    if not code_sent:
                        direction = __set_direction(int(code))
                        client.publish('imageService/droneCircus/direction', direction)
                    go_topic = "droneCircus/autopilotService/go"
                    if code == 1:
                        # north
                        # clientAutopilot.publish(go_topic, "North")
                        client.publish(go_topic, "North")
                    elif code == 2:  # south
                        # clientAutopilot.publish(go_topic, "South")
                        client.publish(go_topic, "South")
                    elif code == 5:
                        # clientAutopilot.publish("droneCircus/autopilotService/drop")
                        client.publish("droneCircus/autopilotService/drop")
                        time.sleep(2)
                        # clientAutopilot.publish("droneCircus/autopilotService/reset")
                        client.publish("droneCircus/autopilotService/reset")
                    elif code == 3:  # east
                        # clientAutopilot.publish(go_topic, "East")
                        client.publish(go_topic, "East")
                    elif code == 4:  # west
                        # clientAutopilot.publish(go_topic, "West")
                        client.publish(go_topic, "West")
                    elif code == 6:
                        returning = True
                        direction = "Volviendo a casa"
                        # clientAutopilot.publish("droneCircus/autopilotService/returnToLaunch")
                        client.publish("droneCircus/autopilotService/returnToLaunch")
                    elif code == 0:
                        # clientAutopilot.publish(go_topic, "Stop")
                        client.publish(go_topic, "Stop")


def on_message_autopilot(cli, userdata, message):
    print("message received")

def send_video_detected(img):
    if video_on:
        # Converting into encoded bytes
        _, buffer = cv2.imencode('.jpg', img)
        jpg_as_text = base64.b64encode(buffer)
        client.publish('imageService/droneCircus/videoFrame', jpg_as_text)



def ImageService ():
    global cap
    global client
    global clientAutopilot
    global prevCode
    global cont
    global code_sent
    global video_on
    global returning

    prevCode = -1
    cont = 0
    code_sent = False
    video_on = False
    returning = False

    # broker_address ="localhost"
    # broker_port = 8080
    broker_address = "broker.hivemq.com"
    broker_port = 8000
    cap = cv2.VideoCapture(0)
    client = mqtt.Client(transport="websockets")
    client.on_message = on_message # Callback function executed when a message is received
    client.connect(broker_address, broker_port)
    client.subscribe('+/imageService/Connect')
    print('Waiting connection')
    client.loop_start()

    # broker_address = "broker.hivemq.com"
    # broker_port = 8000
    # clientAutopilot = mqtt.Client(transport="websockets")
    # clientAutopilot.on_message = on_message_autopilot  # Callback function executed when a message is received
    # clientAutopilot.connect(broker_address, broker_port)
    # clientAutopilot.loop_start()


if __name__ == '__main__':
    ImageService()
