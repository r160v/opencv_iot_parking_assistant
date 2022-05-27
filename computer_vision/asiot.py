import cv2
import numpy as np
from time import sleep
import datetime
import redis



min_length = 100  
min_height = 150  

offset = 20  

line_position = 550 

fps = 100  

time_offset = 700

detected = []
cars_in = 0
cars_out = 0
capacity = 100
free_spots = 2

r = redis.Redis()
r.mset({"cars_in": cars_in, "cars_out": cars_out, "free_spots": free_spots})


def attach_centroid(xx, yy, ww, hh):
    x1 = int(ww / 2)
    y1 = int(hh / 2)
    cx = xx + x1
    cy = yy + y1
    return cx, cy


url = "http://192.168.1.128:8080/video"
# cap = cv2.VideoCapture(url)  remove comment to use video stream from camera and comment the following line

cap = cv2.VideoCapture('test_video/joined.mp4')


substraction = cv2.bgsegm.createBackgroundSubtractorMOG()

last_counted = None
last_counted_x = 0
already_counted = False

while True:
    ret, frame1 = cap.read()
    tempo = float(1/fps)
    sleep(tempo)
    grey = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey, (3, 3), 5)
    img_sub = substraction.apply(blur)
    dilate = cv2.dilate(img_sub, np.ones((5, 5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilated = cv2.morphologyEx(dilate, cv2.MORPH_CLOSE, kernel)
    dilated = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)
    contour, h = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


    cv2.line(frame1, (line_position, 150), (line_position, 900), (255, 127, 0), 3)

    for (i, c) in enumerate(contour):
        (x, y, w, h) = cv2.boundingRect(c)
        validate_contour = (w >= min_length) and (h >= min_height) and 500000 < abs(x + w) * abs(y + h) < 550000
        if not validate_contour:
            continue

        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        centroid = attach_centroid(x, y, w, h)
        detected.append(centroid)
        cv2.circle(frame1, centroid, 4, (0, 0, 255), -1)

        for (x, y) in detected:
            if (line_position + offset) > y > (line_position - offset):
                if last_counted and (datetime.datetime.now() - last_counted).microseconds / 1000 < time_offset:
                    if x > last_counted_x and not already_counted:
                        cars_in += 1
                        r.set("cars_in", cars_in)
                        free_spots -= 1
                    if x <= last_counted_x and not already_counted:
                        cars_out += 1
                        r.set("cars_out", cars_out)
                        if free_spots < capacity:
                            free_spots += 1

                    r.set("free_spots", free_spots)
                    
                    already_counted = True
                    continue
                else:
                    already_counted = False
                    last_counted = datetime.datetime.now()
                    last_counted_x = x
                    cv2.line(frame1, (line_position, 150), (line_position, 900), (0, 127, 255), 3)
                    # print(str(abs(x+w)*abs(y+h)))
                    detected.remove((x, y))
                    # print("car is detected : " + str(cars))

    if free_spots < 0:
        cv2.putText(frame1, "Sitios disponibles: 0", (1050, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
    else:
        cv2.putText(frame1, "Sitios disponibles: " + str(free_spots), (1050, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
    # cv2.putText(frame1, "VEHICLE IN COUNT: " + str(cars_in), (100, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
    # cv2.putText(frame1, "VEHICLE OUT COUNT: " + str(cars_out), (100, 1050), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
    cv2.imshow("OpenCV Parking Assistant", frame1)

    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
cap.release()
