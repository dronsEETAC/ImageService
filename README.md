# ImageService for DEE
## Introduction
The image service is a ground module that receives images from the rest of modules of the ecosystem to perform some image analysis and then send the results back.
Dashboard or mobile applications will requiere the image service to analyze the frames of a video to know the pose that a user is doing on the video, having three modalities, "Fingers", "Poses" and "Faces". This module can be expandable to house other analysis.

## Installations
In order to run and contribute you must install Python 3.7. We recomend to use PyCharm as IDE for developments.
In order to contribute you must follow the contribution protocol described in the main repo of the Drone Engineering Ecosystem.
[![DroneEngineeringEcosystem Badge](https://img.shields.io/badge/DEE-MainRepo-brightgreen.svg)](https://github.com/dronsEETAC/DroneEngineeringEcosystemDEE)



## Commands
In order to send a command to the image service, a module must publish a message in the external broker. The topic of the message must be in the form:
```
"XXX/imageService/YYY"
```
where XXX is the name of the module requiring the service and YYY is the name of the service that is required. Some of the commands may require additional data that must be include in the payload of the message to be published.
In some cases, after completing the service requiered the image service publish a message as an answer. The topic of the answer has the format:
```
"imageService/XXX/ZZZ"
```
where XXX is the name of the module requiring the service and ZZZ is the answer. The message can include data in the message payload.

The table bellow indicates all the commands that are accepted by the image service in the current version.

Command | Description | Payload | Answer | Answer payload
--- | --- | --- | --- |---
*Connect* | The image service subscribes to the messages from the origin | No | No | No
*parameters* | Receives a series of parameters to set the Drone Circus Game modality | Yes (see Note 1) | No | No 
*stopVideoStream* | Stop sending pictures | No | No | No
*videoFrame* | Receives a video frame to be detected | Yes (see Note 2) | *videoFrame* | Yes (see Note 3)
 " | " | " | *code* | The code detected from 0 to 6.

**Note 1**

The JSON received must contain the following parameters.

The parameter 'mode' can be 'fingers', 'faces' or 'poses'. The parameter level can be 'easy' or 'difficult'. And the parameter 'selected_level' can be 'case1', 'case2' or 'case3'. While 'width' and 'height' correspond to the size of the video frames that will be receiving.

```
  {
    'mode': 'fingers',
    'level': 'easy',
    'selected_level': 'case1',
    'width': 400,
    'height': 300
}

```
**Note 2**

The video frame received is inside a JSON encoded in base64 with the index corresponding to that image in the Drone Circus Game:

```
  {
    'image': ' ',
    'index': 1
}

```

**Note 3**

The vector of landmarks resulting from the detection are inside a JSON with the index corresponding to the image being detected. Each landmark contains the positions x, y and z to position it on the image.

```
  {
    'landmarks': {
      {
        'x': 0.1,
        'y': 0.3,
        'z': 0.9
      },
      {
        'x': 0.1,
        'y': 0.3,
        'z': 0.9
      },
      ....        
    },
    'index': 1
}

```
