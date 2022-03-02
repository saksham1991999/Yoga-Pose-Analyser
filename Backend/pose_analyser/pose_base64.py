import cv2 as cv
import numpy as np
import base64

from .config import POSE_ANALYSIS_MAPPER

# BODY_PARTS = { "Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
#                "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
#                "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
#                "LEye": 15, "REar": 16, "LEar": 17, "Background": 18 }

# POSE_PAIRS = [ ["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
#                ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
#                ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"],
#                ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", "Nose"], ["Nose", "REye"],
#                ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"] ]

BODY_PARTS = { "Head": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
                   "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
                   "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "Chest": 14,
                   "Background": 15 }

POSE_PAIRS = [ ["Head", "Neck"], ["Neck", "RShoulder"], ["RShoulder", "RElbow"],
                   ["RElbow", "RWrist"], ["Neck", "LShoulder"], ["LShoulder", "LElbow"],
                   ["LElbow", "LWrist"], ["Neck", "Chest"], ["Chest", "RHip"], ["RHip", "RKnee"],
                   ["RKnee", "RAnkle"], ["Chest", "LHip"], ["LHip", "LKnee"], ["LKnee", "LAnkle"] ]


def imgkeypoints(pose_name, input_img):
    inWidth = 368
    inHeight = 368

    # Specify the paths for the 2 files
    protoFile = "pose_analyser/pose/mpi/pose_deploy_linevec_faster_4_stages.prototxt"
    weightsFile = "pose_analyser/pose/mpi/pose_iter_160000.caffemodel"

    # Read the network into Memory
    net = cv.dnn.readNetFromCaffe(protoFile, weightsFile)

    # ## reading network stored in tensorflow format
    # net = cv.dnn.readNetFromTensorflow("graph_opt.pb")

    # capture video using webcam is input argument is not present
    # cap = cv.VideoCapture(input_img if input_img != ' ' else 0)
    im_bytes = base64.b64decode(input_img)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
    cap = cv.imdecode(im_arr, flags=cv.IMREAD_COLOR)

    frame = cap
    frameWidth = frame.shape[1]
    frameHeight = frame.shape[0]
    net.setInput(cv.dnn.blobFromImage(frame, 1.0 / 255, (inWidth, inHeight), (0, 0, 0), swapRB=False, crop=False))
    out = net.forward()


    points = []
    for i in range(len(BODY_PARTS)):
        # Slice heatmap of corresponging body's part.
        heatMap = out[0, i, :, :]

        # Originally, we try to find all the local maximums. To simplify a sample
        # we just find a global one. However only a single pose at the same time
        # could be detected this way.
        _, conf, _, point = cv.minMaxLoc(heatMap)
        x = (frameWidth * point[0]) / out.shape[3]
        y = (frameHeight * point[1]) / out.shape[2]
        # Add a point if it's confidence is higher than threshold.
        points.append((int(x), int(y)) if conf > 0.2 else None)
    # print(dict(zip(list(BODY_PARTS.keys()),points)))

    for pair in POSE_PAIRS:
        partFrom = pair[0]
        partTo = pair[1]
        assert (partFrom in BODY_PARTS)
        assert (partTo in BODY_PARTS)

        idFrom = BODY_PARTS[partFrom]
        idTo = BODY_PARTS[partTo]

        if points[idFrom] and points[idTo]:
            # print(idFrom, idTo)
            cv.line(frame, points[idFrom], points[idTo], (0, 255, 0), 3)
            cv.ellipse(frame, points[idFrom], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)
            cv.ellipse(frame, points[idTo], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)

    # print()
    # print(goddess(dict(zip(list(BODY_PARTS.keys()),points))))

    t, _ = net.getPerfProfile()
    freq = cv.getTickFrequency() / 1000
    cv.putText(frame, '%.2fms' % (t / freq), (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
    frame = cv.resize(frame, (960, 800))
    cv.imwrite('upload.jpg', frame)
    # cv.imshow('OpenPose using OpenCV', frame)
    _, im_arr = cv.imencode('.jpg', frame)  # im_arr: image in Numpy one-dim array format.
    im_bytes = im_arr.tobytes()
    im_b64 = base64.b64encode(im_bytes)

    if pose_name.lower() in POSE_ANALYSIS_MAPPER:
        evaluate = POSE_ANALYSIS_MAPPER.get(pose_name.lower())
        analysis = evaluate(dict(zip(list(BODY_PARTS.keys()), points)))
        return str(im_b64), analysis