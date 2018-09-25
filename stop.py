import cv2
stop_sign = cv2.CascadeClassifier('cascade\\stop_sign.xml')
car_detect =cv2.CascadeClassifier('cascade\\cas4.xml')

def detect_sign(img):
    mid = 0
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    cascade_obj = stop_sign.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE)
    for (x_pos, y_pos, width, height) in cascade_obj:
        cv2.rectangle(img, (x_pos + 5, y_pos + 5), (x_pos + width - 5, y_pos + height - 5), (0, 255, 0), 2)
        mid = (x_pos+width)-x_pos
        print(mid)
        if mid >=50:
            cv2.putText(img, 'STOP', (x_pos, y_pos - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    return img,mid
def detect_car(img):
    mid = 0
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    cascade_obj = car_detect.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=25,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE)
    for (x_pos, y_pos, width, height) in cascade_obj:
        cv2.rectangle(img, (x_pos + 5, y_pos + 5), (x_pos + width - 5, y_pos + height - 5), (0, 255, 0), 2)
        mid = (x_pos+width)-x_pos
        print("Car ",mid)
        if mid >=150:
            cv2.putText(img, 'Car Ahead STOP', (x_pos, y_pos - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    return img,mid


