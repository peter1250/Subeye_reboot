import cv2, glob, dlib

age_list = [2,5,10,18,28,40,50,80]
gender_list = ['Male', 'Female']

detector = dlib.get_frontal_face_detector()

age_net = cv2.dnn.readNetFromCaffe(
          'models/deploy_age.prototxt', 
          'models/age_net.caffemodel')


def guess_age(frame):


    faces = detector(frame)
    age=0

    for face in faces:
        x1, y1, x2, y2 = face.left(), face.top(), face.right(), face.bottom()

        face_img = frame[y1:y2, x1:x2].copy()

        blob = cv2.dnn.blobFromImage(face_img, scalefactor=4, size=(227, 227),
                                     mean=(78.4263377603, 87.7689143744, 114.895847746),
                                     swapRB=False, crop=False)

        # predict age
        age_net.setInput(blob)
        age_preds = age_net.forward()
        age = age_list[age_preds[0].argmax()]

        # visualize
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)

    return frame,int(age)


