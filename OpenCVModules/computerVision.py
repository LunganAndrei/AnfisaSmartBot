import OpenCVModules.handTrackingModule as htm
import cv2
import mediapipe

def countFingers(imgName):
    detector = htm.handDetector(detectionCon=0.5)

    img = cv2.imread(f"{imgName}")


    tipIds = [4, 8, 12, 16, 20]    # degete ID

    totalFingers=0
    for i in range(1):

        img = detector.findHands(img,draw=False)
        lmList = detector.findPosition(img, draw=False)

        if len(lmList) != 0:
            fingers = []

            if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            # 4 Fingers
            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            totalFingers = fingers.count(1)



        # cv2.imshow("Image", img)
        cv2.waitKey(1)
        return totalFingers