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
from queue import Queue


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
    global frameCont1
    global frameCont2
    global origin
    global q

    splited = message.topic.split("/")
    origin = splited[0]
    command = splited[2]
    print(message.topic)

    if command == 'Connect':
        print('connected')
        client.subscribe(origin+'/imageService/parameters')

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
        client.subscribe(origin+'/imageService/videoFrame')

    if command == 'stopVideoStream':
        prevCode = -1
        cont = 0
        code_sent = False
        video_on = False

    if command == 'videoFrame':
        frameCont1 = frameCont1 + 1
        print("received: ", frameCont1)

        # si el frame rate es molt alt, utilitzar la queue per fer flow control

        if q.qsize() < 5:
            payload = json.loads(message.payload.decode("utf-8"))
            # Decoding the message
            image_text = payload["image"]
            image = base64.b64decode(bytes(image_text, "utf-8"))
            index_img = payload["index"]
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
                    # detect(frame, origin, index_img)
                    print("size queue: ", q.qsize())
                    q.put((frame, index_img))


def on_message_autopilot(cli, userdata, message):
    print("message received")

def send_video_detected(img,origin):

    global video_on

    if video_on:
        # Converting into encoded bytes
        _, buffer = cv2.imencode('.jpg', img)
        jpg_as_text = base64.b64encode(buffer)
        topic = 'imageService/'+origin+'/videoFrame'
        client.publish(topic, jpg_as_text)


def detect(frame, origin, index):
    global prevCode
    global code_sent
    global cont
    global frameCont1
    global frameCont2

    img = cv2.resize(frame, (800, 600))
    img = cv2.flip(img, 1)
    code, multi_landmarks = detector.detect(img, level)
    print("code: ", code, "prev code: ", prevCode, "code_sent: ", code_sent)
    message = {
        "landmarks": multi_landmarks,
        "index": index
    }
    topic = 'imageService/' + origin + '/videoFrame'
    # client.publish(topic, index)
    client.publish(topic, json.dumps(message))
    frameCont2 = frameCont2 + 1
    print("received: ", frameCont1, " sent: ", frameCont2)

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
                topic = 'imageService/' + origin + '/code'
                client.publish(topic, code)

def process_queue():
    global video_on
    global q
    global origin

    while True:
        if not q.empty():
            frame, index = q.get()
            detect(frame, origin, index)
        else:
            time.sleep(0.25)


def ImageService ():
    global cap
    global client
    global clientAutopilot
    global prevCode
    global cont
    global code_sent
    global video_on
    global returning
    global frameCont1
    global frameCont2
    global q
    global origin

    q = Queue()

    frameCont1 = 0
    frameCont2 = 0

    prevCode = -1
    cont = 0
    code_sent = False
    video_on = False
    returning = False

    # broker_address = "broker.hivemq.com"
    broker_address = "localhost"
    broker_port = 8000
    cap = cv2.VideoCapture(0)
    client = mqtt.Client(transport="websockets")
    client.on_message = on_message # Callback function executed when a message is received
    client.max_queued_messages_set(1)
    client.max_inflight_messages_set(1)
    client.connect(broker_address, broker_port)
    client.subscribe('+/imageService/Connect')
    print('Waiting connection')
    client.loop_start()

    x = threading.Thread(target=process_queue())
    x.start()


if __name__ == '__main__':
    ImageService()
