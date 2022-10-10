from deepface import DeepFace
import cv2  


vid = cv2.VideoCapture(0, cv2.CAP_DSHOW) 

haarcascade = cv2.CascadeClassifier('assets/frontalface.xml')

cnt = 1

f = open('assets/mood.txt', 'w')

while(True):
    ret, frame = vid.read()
    
    cv2.imshow('frame', frame)
    faces_rect = haarcascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=6)

    if len(faces_rect) > 0: 
        cv2.putText(frame, 'face detected', (100, 100), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1, color=(0, 0, 255), thickness=2)
        for (x, y, w, h) in faces_rect: 
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.imshow('frame', frame)
    if cnt % 75 == 0:
        try: 
            predict = DeepFace.analyze(frame)
            cv2.putText(frame, predict['dominant_emotion'], (50, 50), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1, color=(0, 0, 255), thickness=2)
            f.write(predict['dominant_emotion'])
            break
        except ValueError:
            f.write('no face detected')
    
    cnt += 1
    
    if cv2.waitKey(20) & 0xFF == ord('q'):
        f.write('x')
        break

f.close()